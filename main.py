from fastapi import FastAPI

import cymbol_models
import cymbol_fields

app = FastAPI()


#####################################################################
#                           get methods                             #
#####################################################################

@app.get("/products")
async def get_products(offset: int = 0, limit: int = 10):
    return {"products": []}

@app.get("/products/{id}")
async def get_product_by_id(id: int):
    return {"id": id, "details": {}}

@app.get("/offers")
async def get_offers(offset: int = 0, limit: int = 10):
    return {"offers": []}

@app.get("/offers/tags")
async def get_offer_by_tags(tags: set[str] = cymbol_fields.Query_Tags):
    return {"tags": tags}

@app.get("/offers/{id}")
async def get_offer_by_id(id: int):
    return {"id": id, "offer": {}}

@app.get("/users/{id}")
async def get_user(id: int):
    return {"user": {"id": id}}

@app.get("/sellers/{id}")
async def get_seller(id: int):
    return {"seller": {"id": id}}

@app.get("/orders/{id}")
async def get_order(id: int):
    return {"order": {"id": id}}


#####################################################################
#                           post methods                            #
#####################################################################

# TODO after Reading about OAuth and JWT tokens

#####################################################################
#                           put methods                             #
#####################################################################

# TODO after reading about OAuth and JWT tokens

#####################################################################
#                           delete methods                          #
#####################################################################

# TODO after reading about OAuth and JWT tokens
