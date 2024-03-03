# src/models.py-1-A+
from sqlalchemy import Column, Integer, String, Float, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    supplier_id = Column(Integer)
    product_category_id = Column(Integer)
    product_subcategory_id = Column(Integer)
    product_range_id = Column(Integer)
    title = Column(String(255))  # Specify length here
    product_slug = Column(String(255))  # And for any other String columns
    description = Column(String(1024))  # Example with a different length
    code = Column(String(100))
    barcode = Column(String(100))
    price = Column(Float)
    supplier = Column(String(255))
    product_image = Column(String(255))
    product_order = Column(Integer)
    product_featured = Column(String(50))
    product_special = Column(String(50))
    product_new = Column(String(50))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    status_id = Column(Integer)

class NewProduct(Base):
    __tablename__ = 'new_products'
    Barcode = Column(String(255), primary_key=True)  # Updated to String with length
    Category = Column(String(255))
    Subcategory = Column(String(255))
    Range = Column(String(255))
    DETAIL = Column(String(1024))  # Assuming detail might be longer
    Name = Column(String(255))
    Supplier = Column(String(255))
    Pricing = Column(Float)

class ProductCategory(Base):
    __tablename__ = 'product_categories'
    id = Column(Integer, primary_key=True)
    category_name = Column(String(255))
    category_slug = Column(String(255))
    seo_category_keywords = Column(String(255))  # Adjust length as needed
    seo_category_description = Column(String(1024))  # Adjust length as needed for descriptions
    category_image = Column(String(255))
    category_order = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    status_id = Column(Integer)

class ProductSubcategory(Base):
    __tablename__ = 'product_subcategories'
    id = Column(Integer, primary_key=True)
    product_category_id = Column(Integer)
    subcategory_name = Column(String(255))
    subcategory_slug = Column(String(255))
    seo_subcategory_keywords = Column(String(255))
    seo_subcategory_description = Column(String(1024))
    subcategory_image = Column(String(255))
    subcategory_order = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    status_id = Column(Integer)
    
class ProductRange(Base):
    __tablename__ = 'product_ranges'
    id = Column(Integer, primary_key=True)
    product_category_id = Column(Integer)
    product_subcategory_id = Column(Integer)
    range_name = Column(String(255))
    range_slug = Column(String(255))
    seo_range_keywords = Column(String(255))
    seo_range_description = Column(String(1024))
    range_image = Column(String(255))
    range_order = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class Supplier(Base):
    __tablename__ = 'suppliers'
    id = Column(Integer, primary_key=True)
    supplier_name = Column(String(255))
    supplier_slug = Column(String(255))
    supplier_image = Column(String(255))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    status_id = Column(Integer)
