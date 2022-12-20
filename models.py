from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, CheckConstraint, DATE
from sqlalchemy import DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy import text

from database import Base



class Customer(Base):
    __tablename__ = "customers"
    __table_args__ = (
        CheckConstraint('age >= 10'),
        CheckConstraint('age <= 200'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=True)
    joined_on = Column(DATE, nullable = True)
    hashed_password = Column(String, nullable=False)
    # TODO: profile picture
    # foreign key on cards
    cards = relationship('Card', back_populates='customers')
    orders = relationship('Orders', back_populates='customers')


class Card(Base):
    __tablename__ = "cards"
    __table_args__ = (
        CheckConstraint('exp_month >= 1'),
        CheckConstraint('exp_month <= 12'),
        CheckConstraint('exp_year <= 2100'),
        CheckConstraint('exp_month <= 2000'),
    )

    card_number = Column(String(16), primary_key=True, index=True)
    card_holder_name = Column(String(255), nullable=False)
    exp_month = Column(Integer, nullable=False)
    exp_year = Column(Integer, nullable=False)
    
    # foreign key from customer
    customer_id = Column(Integer, ForeignKey('customers.id', ondelete='CASCADE'), nullable=False)




class Seller(Base):
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=True)
    joined_on = Column(DATE, server_default=text('now()'), nullable = True)
    hashed_password = Column(String, nullable=False)
    
    # foreign key on products
    products = relationship('Product', back_populates='sellers')
    # foreign key on account
    accounts = relationship('Account', back_populates='sellers')
    # foreign key on order
    orders = relationship('Order', back_populates='sellers')


class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        CheckConstraint('id >= 0'),
        CheckConstraint('price >= 0'),
    )

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price = Column(DECIMAL(10,2), nullable=False)
    desc = Column(String(500), server_default="\"\"")

    # foreign key from seller
    seller_id = Column(Integer, ForeignKey('sellers.id', ondelete='CASCADE'))
    #foreign key on images
    imgs = relationship('images', back_populates='product')


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    img = Column(String, unique=True, index=True, nullable=False)
    desc = Column(String(255), server_default="\"\"")

    # foreign key from product.id
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)


class Account(Base):
    __tablename__ = "bank_accounts"

    acc_number = Column(String, nullable=False, primary_key=True, index=True)
    acc_holder = Column(String(255), nullable=False)
    bank_name = Column(String(255), nullable=False)
    ifsc_code = Column(String(11), nullable=True)

    # foreign key from seller
    seller_id = Column(Integer, ForeignKey('sellers.id', ondelete='CASCADE'), nullable=False)
    



class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (
        CheckConstraint('id >= 0'),
        CheckConstraint('price >= 0'),
    )

    id = Column(Integer, primary_key=True)
    price = Column(Integer, nullable=False)
    is_cod = Column(Boolean, nullable = False, server_default="TRUE")
    is_cancled = Column(Boolean, nullable = False, server_default="FALSE")
    is_delivered = Column(Boolean, nullable = False, server_default="FALSE")
    status = Column(String(255), nullable=True)

    # foreign key from customer from customer, seller, products
    seller_id = Column(Integer, ForeignKey('sellers.id', ondelete='CASCADE'))
    customer_id = Column(Integer, ForeignKey('customers.id', ondelete='CASCADE'))
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'))
    



