from pydantic import HttpUrl, EmailStr
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

import models, schemas
from security import get_password_hash

## Create ##

def create_bank_account(db: Session, account: schemas.AccountIn, seller_id):
    new_account = models.Account(
        **account.dict(), seller_id=seller_id
    )

    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account


def create_card(db: Session, card: schemas.CardIn, customer_id: int):
    new_card = models.Card(
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


def create_image(db: Session, new_image: schemas.ImageIn):
    new_image = models.Image(**new_image.dict())

    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    return new_image


def create_order(db: Session, order: schemas.OrderIn):
    new_order = models.Order(**order.dict())

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
    new_seller = models.Seller(
        **seller.dict(),
        hashed_password=get_password_hash(password=password)
    )

    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller



## Retrieve ##

def get_bank_accounts(db: Session, seller_id: int):
    return db.query(models.Account).filter(models.Account.seller_id == seller_id).all()


def get_cards(db: Session, customer_id: int):
    return db.query(models.Card).filter(models.Card.customer_id == customer_id).all()

def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()


def get_customer_by_email(db: Session, email: EmailStr):
    return db.query(models.Customer).filter(models.Customer.email == email).first()


def get_image(db: Session, image_id: int):
    return db.query(models.Image).filter(models.Image.id == image_id).first()


def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def get_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if (product):
        return product
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Such Product With Product id = {product_id} exists"
        )


def get_seller(db: Session, seller_id: int):
    return db.query(models.Seller).filter(models.Seller.id == seller_id).first()


def get_seller_by_email(db: Session, email: EmailStr):
    return db.query(models.Seller).filter(models.Seller.email == email).first()


## Update ##

def update_customer_email(db: Session, customer_id: int, new_email: str):
    update_query = db.query(models.Customer).filter(models.Customer.id == customer_id)
    if (update_query.first()):
        update_query.update({"email": new_email}, synchronize_session=False)
        db.commit()
        return update_query.first()


def update_customer_by_id(db: Session, customer_id: int, new_details: schemas.CustomerIn):
    update_query = db.query(models.Customer).filter(models.Customer.id == customer_id)
    if (update_query.first()):
        update_query.update(new_details.dict(), synchronize_session=False)
        db.commit()
        return update_query.first()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer NOT FOUND in Database"
        )



def update_customer_password(db: Session, customer_id: int, new_password: str):
    update_query = db.query(models.Customer).filter(models.Customer.id == customer_id)
    if (update_query.first()):
        update_query.update({"hashed_password": get_password_hash(new_password)}, synchronize_session=False)
        db.commit()
        return update_query.first()



def update_image(db: Session, image_id: int, **details):
    update_query = db.query(models.Image).filter(models.Image.id == image_id)
    if (update_query.first()):
        try:
            update_query.update(details, synchronize_session=False)
            db.commit()
            return update_query.first()
        except:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid Fields for updating models.Image"
            )
            


def update_order(db: Session, order_id: int, new_details: schemas.OrderIn):
    update_query = db.query(models.Order).filter(models.Order.id == order_id)
    if (update_query.first()):
        update_query.update(new_details.dict(), synchronize_session=False)
        db.commit()
        return update_query.first()
    else:
        return -1


def update_product(db: Session, product_id: int, new_details: schemas.ProductIn):
    update_query = db.query(models.Product).filter(models.Product.id == product_id)
    if (update_query.first()):
        update_query.update(new_details.dict(), synchronize_session=False)
        db.commit()
        return update_query.first()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Product with product_id = {product_id} in database"
        )


def update_seller_email(db: Session, seller_id: int, new_email: str):
    update_query = db.query(models.Seller).filter(models.Seller.id == seller_id)
    if (update_query.first()):
        update_query.update({"email": new_email}, synchronize_session=False)
        db.commit()
        return update_query.first()
    else:
        return -1


def update_seller_by_id(db: Session, seller_id: int, new_details: schemas.SellerIn):
    update_query = db.query(models.Seller).filter(models.Seller.id == seller_id)
    if (update_query.first()):
        update_query.update(new_details.dict(), synchronize_session=False)
        db.commit()
        return update_query.first()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seller NOT FOUND in Database"
        )


def update_seller_password(db: Session, seller_id: int, new_password: str):
    update_query = db.query(models.Seller).filter(models.Seller.id == seller_id)
    if (update_query.first()):
        update_query.update({"hashed_password": get_password_hash(new_password)}, synchronize_session=False)
        db.commit()
        return update_query.first()
    else:
        return -1



## Delete ##

def delete_bank_account(db: Session, acc_number: str):
    account = db.query(models.Account).filter(models.Account.acc_number == acc_number).first()
    if account:
        to_return = schemas.AccountDB(**account)
        db.delete(account)
        db.commit()
        return to_return
    else:
        return -1

def delete_card(db: Session, card_number: str):
    card = db.query(models.Card).filter(models.Card.card_number == card_number).first()
    if card:
        to_return = schemas.CardDB(**card)
        db.delete(card)
        db.commit()
        return to_return
    else:
        return -1

def delete_customer(db: Session, customer_id: int):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if customer:
        to_return = schemas.CustomerDB(**customer)
        db.delete(customer)
        db.commit()
        return to_return
    else:
        return -1

def delete_image(db: Session, image_id: int):
    image = db.query(models.Image).filter(models.Image.id == image_id).first()
    if image:
        to_return = schemas.ImageOut(**image)
        db.delete(image)
        db.commit()
        return to_return
    else:
        return -1

def delete_order(db: Session, order_id: int):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order:
        to_return = schemas.OrderDB(**order)
        db.delete(order)
        db.commit()
        return to_return
    else:
        return -1

def delete_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        to_return = schemas.ProductDB(**product)
        db.delete(product)
        db.commit()
        return to_return
    else:
        return -1

def delete_seller(db: Session, seller_id: int):
    seller = db.query(models.Seller).filter(models.Seller.id == seller_id).first()
    if seller:
        to_return = schemas.SellerDB(**seller)
        db.delete(seller)
        db.commit()
        return to_return
    else:
        return -1
