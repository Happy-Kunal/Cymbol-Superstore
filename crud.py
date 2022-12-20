from pydantic import HttpUrl
from sqlalchemy.orm import Session

import models, schemas
from security import get_password_hash

## Create ##

def create_bank_account(db: Session, account: schemas.AccountIn, seller_id):
    new_account = models.Product(
        **account.dict(), seller_id=seller_id
    )

    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account


def create_card(db: Session, card: schemas.CardIn, customer_id: int):
    new_card = models.Product(
        **card.dict(), customer_id=customer_id
    )

    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return new_card


def creater_customer(db: Session, customer: schemas.CustomerIn, password: str):
    new_customer = models.Customer(
        **customer.dict(),
        hashed_password=get_password_hash(password=password)
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer


def create_image(db: Session, url: HttpUrl, product_id: int, desc: str = ""):
    new_image = models.Product(
        img=url, desc=desc, product_id=product_id
    )

    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    return new_image


def create_order(db: Session, order: schemas.OrderIn):
    new_order = models.Product(**order.dict())

    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


def create_product(db: Session, product: schemas.ProductIn, seller_id: int):
    new_product = models.Product(
        **product.dict(), seller_id=seller_id
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def creater_seller(db: Session, seller: schemas.SellerIn, password: str):
    new_seller = models.Customer(
        **seller.dict(),
        hashed_password=get_password_hash(password=password)
    )

    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller



## Retrieve ##

def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()


def get_customer_by_email(db: Session, email: str):
    return db.query(models.Customer).filter(models.Customer.email == email).first()


def get_image(db: Session, image_id: int):
    return db.query(models.Image).filter(models.Image.id == image_id).first()


def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_seller(db: Session, seller_id: int):
    return db.query(models.Seller).filter(models.Seller.id == seller_id).first()


def get_seller_by_email(db: Session, email: str):
    return db.query(models.Seller).filter(models.Seller.email == email).first()


## Update ##
# TODO: email updates in customer and seller
# TODO: add update product, image, order


## Delete ##

def delete_bank_account(db: Session, acc_number: str):
    account = db.query(models.Account).filter(models.Account.acc_number == acc_number).first()
    if account:
        to_return = schemas.AccountDB(**account)
        account.delete(synchronize_session=False)
        db.commit()
        return to_return
    else:
        return -1

def delete_card(db: Session, card_number: str):
    card = db.query(models.Card).filter(models.Card.card_number == card_number).first()
    if card:
        to_return = schemas.CardDB(**card)
        card.delete(synchronize_session=False)
        db.commit()
        return to_return
    else:
        return -1

def delete_customer(db: Session, customer_id: int):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if customer:
        to_return = schemas.CustomerDB(**customer)
        customer.delete(synchronize_session=False)
        db.commit()
        return to_return
    else:
        return -1

def delete_image(db: Session, image_id: int):
    image = db.query(models.Image).filter(models.Image.id == image_id).first()
    if image:
        to_return = schemas.Image(**image)
        image.delete(synchronize_session=False)
        db.commit()
        return to_return
    else:
        return -1

def delete_order(db: Session, order_id: int):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order:
        to_return = schemas.OrderDB(**order)
        order.delete(synchronize_session=False)
        db.commit()
        return to_return
    else:
        return -1

def delete_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        to_return = schemas.ProductDB(**product)
        product.delete(synchronize_session=False)
        db.commit()
        return to_return
    else:
        return -1

def delete_seller(db: Session, seller_id: int):
    seller = db.query(models.Seller).filter(models.Seller.id == seller_id).first()
    if seller:
        to_return = schemas.SellerDB(**seller)
        seller.delete(synchronize_session=False)
        db.commit()
        return to_return
    else:
        return -1
