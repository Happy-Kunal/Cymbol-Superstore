from datetime import date

from pydantic import EmailStr, HttpUrl
from fastapi import FastAPI
from fastapi import Depends, HTTPException, status
from fastapi import Query, Form, Body
from sqlalchemy.orm import Session

from database import engine, get_db
import crud
import models, schemas, security, extras

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(
    security.router,
    prefix="/auth",
    tags=["auth"],
)



#####################################################################
#                           get methods                             #
#####################################################################

@app.get("/customers/id/{id}", response_model=schemas.CustomeOut)
async def get_customer_by_id(id: int, db: Session = Depends(get_db)):
    customer = crud.get_customer(db=db, customer_id=id)
    if customer:
        return customer
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested Data Isn't Available at server"
        )


@app.get("/customers/email/{email}", response_model=schemas.CustomeOut)
async def get_customer_by_email(email: EmailStr, db: Session = Depends(get_db)):
    customer = crud.get_customer_by_email(db=db, email=email)
    if customer:
        return customer
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested Data Isn't Available at server"
        )

@app.get("/customers/me", response_model=schemas.CustomeOut)
async def get_current_customer(
    db: Session = Depends(get_db),
    user: schemas.TokenData = Depends(security.decode_access_token_if_valid_else_throw_401)
):
    if (not user.isSeller):
        return crud.get_customer(db, customer_id=user.id)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="For the time being Sellers Account aren't "
                    "associate Corresponding Customer Accounts\n"
                    "Try creating a customer account or /sellers/me"
        )

@app.get("/customers/me/orders", response_model=list[schemas.OrderOut], include_in_schema=False)
async def get_orders_of_current_customer_by_date(
    start: date = Query(),
    end: date = Query(),
    db: Session = Depends(get_db),
    user: schemas.TokenData = Depends(security.decode_access_token_if_valid_else_throw_401)
):
    if (not user.isSeller):
        orders = db.query(models.Order).filter(models.Order.customer_id == user.id).all()
    else:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="try using /sellers/me/orders instead"
        )
    
    if orders:
        return orders
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested Data Isn't Available at server"
        )


@app.get("/customers/me/orders/all", response_model=list[schemas.OrderOut])
async def get_all_orders_of_current_customer(
    db: Session = Depends(get_db),
    user: schemas.TokenData = Depends(security.decode_access_token_if_valid_else_throw_401)
):
    if (not user.isSeller):
        orders = db.query(models.Order).filter(models.Order.customer_id == user.id).all()
    else:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="try using /sellers/me/orders/all instead"
        )
    
    if orders:
        return orders
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested Data Isn't Available at server"
        )


@app.get("/cutomers/me/cards", response_model=list[schemas.CardOut])
async def get_my_cards(
    db: Session = Depends(get_db),
    user: schemas.TokenData = Depends(security.decode_access_token_if_valid_else_throw_401)
):
    if (not user.isSeller):
        cards = crud.get_cards(db, customer_id=user.id)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Customers are allowed to have bank cards\n"
                    "Instead try fetching your Bank Account details"
        )

    if cards:
        return cards
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested Data Isn't Available at server"
        )


@app.get("/images/{image_id}", response_model=schemas.ImageOut)
async def get_image_by_id(image_id: int, db: Session = Depends(get_db)):
    image = crud.get_image(db=db, image_id=image_id)
    if image:
        return image
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested Data Isn't Available at server"
        )


@app.get("/orders/{id}", response_model=schemas.OrderOut)
async def get_order(id: int, db: Session = Depends(get_db)):
    order = crud.get_order(db=db, order_id=id)
    if order:
        return order
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested Data Isn't Available at server"
        )


@app.get("/products", response_model=list[schemas.ProductOut])
async def get_products(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = db.query(models.Product).offset(offset=offset).limit(limit=limit).all()
    if products:
        return products
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested Data Isn't Available at server"
        )

@app.get("/products/seller/{seller_id}", response_model=list[schemas.ProductOut])
async def get_product_by_seller_id(
    seller_id: int,
    offset: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    products = db.query(models.Product)\
                    .filter(models.Product.seller_id == seller_id)\
                    .offset(offset=offset).limit(limit=limit).all()
    if products:
        return products
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested Data Isn't Available at server"
        )


@app.get("/products/{id}", response_model=schemas.ProductOut)
async def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db=db, product_id=id)
    if product:
        return product
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested Data Isn't Available at server"
        )


@app.get("/sellers/id/{id}", response_model=schemas.SellerOut)
async def get_seller(id: int, db: Session = Depends(get_db)):
    seller = crud.get_seller(db=db, seller_id=id)
    if seller:
        return seller
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested Data Isn't Available at server"
        )


@app.get("/sellers/email/{email}", response_model=schemas.SellerOut)
async def get_seller_by_email(email: EmailStr, db: Session = Depends(get_db)):
    seller = crud.get_seller_by_email(db=db, email=email)
    if seller:
        return seller
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested Data Isn't Available at server"
        )


@app.get("/sellers/me", response_model=schemas.SellerOut)
async def get_current_seller(
    db: Session = Depends(get_db),
    user: schemas.TokenData = Depends(security.decode_access_token_if_valid_else_throw_401)
):
    if (user.isSeller):
        return crud.get_seller(db, seller_id=user.id)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="For the time being Customer Account aren't "
                    "associate Corresponding Seller Accounts\n"
                    "Try creating a Seller account"
        )


@app.get("/sellers/me/accounts", response_model=list[schemas.AccountOut])
async def get_my_bank_accounts(
    db: Session = Depends(get_db),
    user: schemas.TokenData = Depends(security.decode_access_token_if_valid_else_throw_401)
):
    if (user.isSeller):
        accounts = crud.get_bank_accounts(db, seller_id=user.id)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Sellers are allowed to have bank accounts\n"
                    "Instead try fetching your Cards details"
        )

    if accounts:
        return accounts
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested Data Isn't Available at server"
        )


@app.get("/sellers/me/orders", response_model=list[schemas.OrderOut], include_in_schema=False)
async def get_orders_of_current_seller_by_date(
    start: date = Query() , end: date = Query(),
    db: Session = Depends(get_db),
    user: schemas.TokenData = Depends(security.decode_access_token_if_valid_else_throw_401)
):
    if (user.isSeller):
        orders = db.query(models.Order).filter(models.Order.seller_id == user.id).all()
    else:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="try using /customers/me/orders instead"
        )
    
    if orders:
        return orders
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested Data Isn't Available at server"
        )


@app.get("/sellers/me/orders/all", response_model=list[schemas.OrderOut])
async def get_all_orders_of_current_seller(
    db: Session = Depends(get_db),
    user: schemas.TokenData = Depends(security.decode_access_token_if_valid_else_throw_401)
):
    if (user.isSeller):
        orders = db.query(models.Order).filter(models.Order.seller_id == user.id).all()
    else:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="try using /customers/me/orders/all instead"
        )
    
    if orders:
        return orders
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested Data Isn't Available at server"
        )

@app.get("/sellers/me/products", response_model=list[schemas.ProductOut])
async def get_product_of_current_seller(
    offset: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    user: schemas.TokenData = Depends(security.decode_access_token_if_valid_else_throw_401)
):
    products = db.query(models.Product)\
                    .filter(models.Product.seller_id == user.id)\
                    .offset(offset=offset).limit(limit=limit).all()
    if products:
        return products
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested Data Isn't Available at server"
        )




#####################################################################
#                           post methods                            #
#####################################################################

# TODO: change body fields to form fields
# https://github.com/tiangolo/fastapi/issues/5588
# if above issue isn't fix soon do work arround with
# openAPI schemas

@app.post("/customers/create", response_model=schemas.CustomeOut)
async def create_customer(
    db: Session = Depends(get_db),
    new_customer: schemas.CustomerIn = Body(),
    #password: str = Form() #TODO
):
    return crud.creater_customer(
                                    db=db,
                                    customer=new_customer,
                                    password="fakepassword@" + new_customer.email
                                )


@app.post("/customer/add/card", response_model=schemas.CardOut)
async def add_card(
    db: Session = Depends(get_db),
    new_card: schemas.CardIn = Body(),
    user: schemas.TokenData = Depends(security.decode_access_token_if_valid_else_throw_401)
):
    if (not user.isSeller):
        return crud.create_card(db, new_card, user.id)
    else:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="For the time being Only Customers Are allowed to have cards"
        )


@app.post("/orders/place", response_model=schemas.OrderOut)
async def place_order(
    db: Session = Depends(get_db),
    new_order: schemas.OrderIn = Body(),
    user: schemas.TokenData = Depends(security.decode_access_token_if_valid_else_throw_401)
):
    if (not user.isSeller):
        product = crud.get_product(db, new_order.product_id)
        if (product):
            if (product.seller_id == new_order.seller_id):
                return crud.create_order(db=db, order=new_order)
            else:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    detail="Seller Passed In new Order isn't same as"
                            "the seller of product passed in new Order"
                )

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id: {new_order.product_id}, Doesn't Exists"
            )

    else:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="For the time being Only Customers can buy products"
        )


@app.post("/sellers/create", response_model=schemas.SellerOut)
async def create_seller(
    db: Session = Depends(get_db),
    new_seller: schemas.SellerIn = Body(),
    # password: str = Form() # TODO
):
    return crud.creater_seller(db, new_seller, "fakepassword@" + new_seller.email)


@app.post("/sellers/add/account", response_model=schemas.AccountOut)
async def add_account(
    db: Session = Depends(get_db),
    new_account: schemas.AccountIn = Body(),
    user: schemas.TokenData = Depends(security.decode_access_token_if_valid_else_throw_401)
):
    if (user.isSeller):
        return crud.create_bank_account(db, new_account, user.id)
    else:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="For the time being Only Sellers Are allowed to have Account"
        )


@app.post("/products/create", response_model=schemas.ProductOut)
async def create_product(
    db: Session = Depends(get_db),
    new_product: schemas.ProductIn = Body(),
    user: schemas.TokenData = Depends(security.decode_access_token_if_valid_else_throw_401)
):
    if (user.isSeller):
        return crud.create_product(db, new_product, user.id)
    else:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="For the time being Only Sellers Are allowed to have Account"
        )


@app.post("/products/{id}/addImage", response_model=schemas.ImageOut)
async def add_image_to_product(
    id: int,
    new_image: schemas.ImageIn = Body(),
    db: Session = Depends(get_db),
    user: schemas.TokenData = Depends(security.decode_access_token_if_valid_else_throw_401)
):
    product = crud.get_product(db, id)
    if (user.isSeller):
        if (product):
            if (product.seller_id == user.id):
                return crud.create_image(db, new_image)
            else:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    detail=f"Product with id: {id}, isn't owned by Current Seller"
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id: {id}, Doesn't Exists"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Only Sellers Can Edit/Add Product Details"
        )


                


#####################################################################
#                           put methods                             #
#####################################################################

# TODO after reading about OAuth and JWT tokens

#####################################################################
#                           delete methods                          #
#####################################################################

# TODO after reading about OAuth and JWT tokens
