# Product Processor System

## Overview

The Product Processor System automates the integration of new product entries into your database, streamlining the process of updating product listings with efficiency and accuracy. By leveraging advanced matching algorithms and automated workflows, this system significantly reduces manual labor while ensuring data integrity.

## Workflow and Methods

The system follows a structured workflow, utilizing several key methods to process new product entries:

### Initialization

**Method**: `__init__`

The initialization method sets up database connections and file paths for logs and reports, pulling configuration from environment variables.

**Example**:

```python
def __init__(self, db_connection_params, markdown_file_path, sql_log_path):
    self.db_connection_params = db_connection_params
    ...
```

**Environment Variables**:

The `.env` file contains critical settings, ensuring easy configuration and adaptability:

```
DB_HOST=localhost
DB_USER=user
DB_PASSWORD=pass
DB_NAME=mydatabase
MARKDOWN_FILE_PATH=./logs/markdown_log.md
SQL_LOG_PATH=./logs/sql_log.md
```

### Database Connection

**Method**: Integrated within `__init__`

Utilizes SQLAlchemy ORM for database connectivity, enhancing security and simplifying queries.

**Example**:

```python
self.engine = create_engine(f"mysql+pymysql://{self.db_connection_params['user']}:...")
```

### Fetching New Products

**Method**: `fetch_new_products`

Queries the `NewProduct` table to retrieve entries pending processing.

**Example**:

```python
def fetch_new_products(self):
    session = self.Session()
    return session.query(NewProduct).all()
```

### Entity Matching

**Method**: `find_best_match`

Automatically matches product details to existing entities (e.g., categories, suppliers) using the Levenshtein distance for similarity measurement.

**Example**:

```python
def find_best_match(self, session, model, column, value):
    ...
```

### Thumbnail Generation

**Method**: `resize_image`

Generates a thumbnail for product images, maintaining aspect ratio and ensuring a max height of 200px.

**Example**:

```python
def resize_image(self, image_path):
    ...
    img.save(thumbnail_path)
```

### SQL Insert Statement Generation

**Method**: `generate_insert_statement`

Constructs and logs SQL insert statements for new products, facilitating easy integration into the database.

**Example**:

```python
def generate_insert_statement(self, product):
    return f"INSERT INTO products (...)"
```

### Markdown Report Generation

**Method**: `construct_markdown_content`

Creates a detailed markdown report for each processed product, including thumbnails, product details, and matched entities.

**Example**:

```python
def construct_markdown_content(self, product, number, ...):
    markdown_content = f"""
    ## {number}. {product.title}
    ![Thumbnail](path/to/thumbnail)
    ...
    """
    return markdown_content.strip()
```

### Comprehensive Logging

**Methods**: `add_to_markdown_file`, `generate_unmatched_categories_report`

These methods log detailed information about processed products and categories requiring attention.

**Example**:

```python
def add_to_markdown_file(self, markdown_content):
    with open(self.markdown_file_path, 'a') as file:
        file.write(markdown_content + "\n\n")
```

## System Capabilities

- **Automated Entity Matching**: Reduces errors and saves significant time by automating the categorization process.
- **Thumbnail Generation**: Enhances the visual appeal of product listings without manual image editing.
- **Efficient Database Updates**: Streamlines the addition of new products with auto-generated SQL statements.
- **Easy Configuration**: Utilizes environment variables for flexible system settings.
- **Scalability and Maintainability**: Written in clean, object-oriented Python following best practices, fully commented for ease of future development.

## Setup and Operation

1. Ensure Python 3.6+ and required packages (SQLAlchemy, Pillow, PyMySQL) are installed.
2. Configure your `.env` file with database and path settings.
3. Run `python app.py` to process new products and generate reports.

## Future Extensions

The modular design allows for easy extension, whether adding new matching criteria, supporting additional databases, or customizing reports.

By following this detailed guide, developers and system administrators can effectively utilize the Product Processor System, leveraging its full capabilities to enhance productivity and data accuracy in product management.
```

This README provides a deep dive into the application's functionality, method-by-method explanations, examples of critical operations, and insights into the system's design and extendibility. It serves as a comprehensive manual for understanding and working with the system.