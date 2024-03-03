# src/app.py-1-A+
import os
from datetime import datetime
import Levenshtein as lev
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, NewProduct, ProductCategory, ProductSubcategory, ProductRange, Supplier, Product
from dotenv import load_dotenv
from PIL import Image

load_dotenv()  # Load environment variables from .env file

# Use environment variables
db_connection_params = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'db': os.getenv('DB_NAME')
}

markdown_file_path = os.getenv('MARKDOWN_FILE_PATH')
sql_log_path = os.getenv('SQL_LOG_PATH')
unmatched_categories_report_path = os.getenv('UNMATCHED_CATEGORIES_REPORT_PATH')

class ProductProcessor:
    """
    Processes new products from the 'NewProduct' table by matching entities based on Levenshtein distance,
    generates SQL insert statements for the 'Products' table, and logs detailed information in markdown format.
    """
    def __init__(self, db_connection_params):
        self.markdown_file_path = markdown_file_path
        self.sql_log_path = sql_log_path
        self.unmatched_categories_report_path = unmatched_categories_report_path
        self.db_connection_params = db_connection_params
        self.engine = create_engine(f"mysql+pymysql://{db_connection_params['user']}:{db_connection_params['password']}@{db_connection_params['host']}/{db_connection_params['db']}")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def generate_unmatched_categories_report(self, mismatched_entities):
        """
        Generates a report for unmatched categories and sub-categories.
        """
        with open(self.unmatched_categories_report_path, 'w') as report_file:
            for entity in set(mismatched_entities):  # Ensure unique entries
                report_file.write(f"- {entity}\n")

    def calculate_similarity(self, a, b):
        max_len = max(len(a), len(b))
        if max_len == 0:
            return 100
        distance = lev.distance(a.lower(), b.lower())
        return (1 - distance / max_len) * 100

    def find_best_match(self, session, model, column, value):
        best_match_id = 1
        highest_similarity = 0
        is_matched = False
        best_entity = None
        for instance in session.query(model).all():
            instance_value = getattr(instance, column, "")
            similarity = self.calculate_similarity(value, instance_value)
            if similarity >= 85 and similarity > highest_similarity:
                best_match_id = instance.id
                highest_similarity = similarity
                is_matched = True
                best_entity = instance
        return best_match_id, is_matched, best_entity

    def get_entity_name_by_id(self, session, model, entity_id):
        entity = session.query(model).filter(model.id == entity_id).first()
        return getattr(entity, 'name', 'Default') if entity else 'Default'

    def escape_sql_value(self, value):
        """Escape single quotes in a string value for SQL insertion."""
        if isinstance(value, str):
            return value.replace("'", "''")
        return value

    def generate_insert_statement(self, product):
        # Escaping single quotes by replacing them with two single quotes
        title = product.title.replace("'", "''")
        product_slug = product.product_slug.replace("'", "''")
        description = product.description.replace("'", "''")
        code = product.code.replace("'", "''")
        barcode = product.barcode.replace("'", "''")
        supplier = product.supplier.replace("'", "''")
        product_image = product.product_image if os.path.exists(os.path.join("data", "images", product.product_image)) else "image_not_found.jpg"
        product_image = product_image.replace("'", "''")
        
        insert_statement = f"""INSERT INTO products (
            supplier_id, product_category_id, product_subcategory_id, product_range_id, 
            title, product_slug, description, code, barcode, price, supplier, 
            product_image, product_order, product_featured, product_special, 
            product_new, created_at, status_id
        ) VALUES (
            {product.supplier_id}, {product.product_category_id}, {product.product_subcategory_id}, 
            {product.product_range_id}, '{title}', '{product_slug}', 
            '{description}', '{code}', '{barcode}', {product.price}, 
            '{supplier}', '{product_image}', {product.product_order}, 
            '{product.product_featured}', '{product.product_special}', '{product.product_new}', 
            '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}', {product.status_id}
        );"""
    
        with open(self.sql_log_path, 'a') as f:
            f.write(insert_statement + "\n")
        
        return insert_statement

    def resize_image(self, image_path, max_height=200):
        """
        Resizes an image, maintaining aspect ratio, to a maximum height of 200px.
        Saves the resized image as a thumbnail with '_thumb' appended to the filename.
        Returns the path to the thumbnail.
        """
        with Image.open(image_path) as img:
            original_width, original_height = img.size
            if original_height > max_height:
                # Calculate new dimensions
                height_percent = (max_height / float(original_height))
                new_width = int((float(original_width) * float(height_percent)))
                new_height = max_height
                # Resize image using Image.Resampling.LANCZOS for high-quality downsampling
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Create thumbnail filename
            base, extension = os.path.splitext(image_path)
            thumbnail_path = f"{base}_thumb{extension}"
            
            # Save thumbnail
            img.save(thumbnail_path)
            return thumbnail_path

    def construct_markdown_content(self, product, number, category_name, subcategory_name, range_name, supplier_name, matched_entities, mismatched_entities):
        """
        Constructs and returns markdown content for a processed product, including detailed information,
        matched and mismatched entities, and the SQL insert statement.
        """
        product_image_path = os.path.join("data", "images", product.product_image)
        image_exists = os.path.exists(product_image_path)  # Directly use boolean value for condition checks

        # Using the boolean value of image_exists to conditionally set image info and thumbnail
        if image_exists:
            thumbnail_path = self.resize_image(product_image_path)
            thumbnail = f"![Thumbnail]({thumbnail_path})"
            image_info = f"- **Product Image:** {product.product_image}"
        else:
            # Define the path for the "image_not_found.jpg"
            default_thumbnail_path = "data/images/image_not_found.jpg"  # Ensure this path is correct
            thumbnail = f"![Thumbnail]({default_thumbnail_path})"
            
            image_not_found_path = "image_not_found.jpg"  # Ensure this path is correct
            image_info = "- **Product Image:** image_not_found.jpg"
            thumbnail = f"![Thumbnail](data/images/{image_not_found_path})"
            
        insert_statement = self.generate_insert_statement(product)

        markdown_content = f"""
## {product.title}
{thumbnail}
- **Description:** {product.description}
- **Category:** {category_name}
- **Sub-Category:** {subcategory_name}
- **Range:** {range_name}
- **Slug:** {product.product_slug}
- **Barcode:** {product.barcode}
- **Supplier:** {supplier_name}
- **Price:** {product.price}
{image_info}
- **Product Image Found:** {'Yes' if image_exists else 'No'}
- **Product Order:** {product.product_order}
- **Product Featured:** {product.product_featured}
- **Product Special:** {product.product_special}
- **Product New:** {product.product_new}
- **Created At:** {product.created_at.strftime('%Y-%m-%d %H:%M:%S')}
- **Status:** {product.status_id}
- **Insert Statement**: {insert_statement}
- **Entities Matched:** {', '.join([f'{name}: {value}' for name, value in matched_entities])}
- **Entities Mismatched:** {', '.join([f'{name}: Default Used' for name in mismatched_entities])}
"""
        return markdown_content.strip()


    def add_to_markdown_file(self, markdown_content):
        with open(self.markdown_file_path, 'a') as md_file:
            md_file.write(markdown_content + "\n\n")

    def process_new_products(self):
        """
        Processes all new products from the 'NewProduct' table. For each new product, it performs the following operations:
        1. Matches the product's supplier, category, subcategory, and range to existing entities using Levenshtein distance.
        2. Fetches names for matched entities to use in logging.
        3. Creates a new Product instance with detailed entity information.
        4. Commits the new Product to the database.
        5. Generates a detailed markdown log for each processed product.
        """
        session = self.Session()
        try:
            new_products = session.query(NewProduct).all()
            for index, new_product in enumerate(new_products, 1):
                matched_entities = []
                mismatched_entities = []

                # Match Supplier and fetch name
                supplier_id, supplier_matched, supplier_entity = self.find_best_match(session, Supplier, 'supplier_name', new_product.Supplier)
                supplier_name = supplier_entity.supplier_name if supplier_matched else "Default"
                if supplier_matched:
                    matched_entities.append(('Supplier', supplier_entity.supplier_name))
                else:
                    mismatched_entities.append('Supplier')

                # Match ProductCategory and fetch name
                category_id, category_matched, category_entity = self.find_best_match(session, ProductCategory, 'category_name', new_product.Category)
                category_name = category_entity.category_name if category_matched else "Default"
                if category_matched:
                    matched_entities.append(('Category', category_entity.category_name))
                else:
                    mismatched_entities.append('Category')

                # Match ProductSubcategory and fetch name
                subcategory_id, subcategory_matched, subcategory_entity = self.find_best_match(session, ProductSubcategory, 'subcategory_name', new_product.Subcategory)
                subcategory_name = subcategory_entity.subcategory_name if subcategory_matched else "Default"
                if subcategory_matched:
                    matched_entities.append(('Subcategory', subcategory_entity.subcategory_name))
                else:
                    mismatched_entities.append('Subcategory')

                # Match ProductRange and fetch name
                range_id, range_matched, range_entity = self.find_best_match(session, ProductRange, 'range_name', new_product.Range)
                range_name = range_entity.range_name if range_matched else "Default"
                if range_matched:
                    matched_entities.append(('Range', range_entity.range_name))
                else:
                    mismatched_entities.append('Range')

                # Creating the new Product instance with the gathered information
                product = Product(
                    supplier_id=supplier_id,
                    product_category_id=category_id,
                    product_subcategory_id=subcategory_id,
                    product_range_id=range_id,
                    title=new_product.Name,
                    product_slug=new_product.Name.replace(' ', '-').lower(),
                    description=new_product.DETAIL,
                    code=str(new_product.Barcode),
                    barcode=str(new_product.Barcode),
                    price=new_product.Pricing,
                    supplier=supplier_name,
                    product_image=f"{new_product.Barcode}.jpg",
                    product_order=0,
                    product_featured="No",
                    product_special="No",
                    product_new="No",
                    created_at=datetime.now(),
                    status_id=1
                )
                session.add(product)
                session.commit()

                # Generate and log markdown content for the processed product
                markdown_content = self.construct_markdown_content(
                    product, index, category_name, subcategory_name, range_name, supplier_name,
                    matched_entities, mismatched_entities
                )
                self.add_to_markdown_file(markdown_content)
        finally:
            session.close()
            self.generate_unmatched_categories_report(set(mismatched_entities))


    def add_product(self, session, product):
        """Adds a product to the database and commits the transaction."""
        session.add(product)
        session.commit()

processor = ProductProcessor(db_connection_params)
processor.process_new_products()



