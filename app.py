from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from typing import Optional

API_VERSION = "/api/v1"


class UserModel(BaseModel):
    username: str
    password: str
    city: str


class UpdateUser(BaseModel):
    username: Optional[str]
    password: Optional[str]
    city: Optional[str]


app = FastAPI()

db = {
    "users": [
        {"default": {"password": "default", "city": "Coimbatore"}},
        {"default_1": {"password": "default_1", "city": "Chennai"}},
        {"default_2": {"password": "default_2", "city": "Bangalore"}},
        {"default_4": {"password": "default", "city": "Coimbatore"}},
        {"default_5": {"password": "default_1", "city": "Chennai"}},
        {"default_6": {"password": "default_2", "city": "Bangalore"}},
        {"default_7": {"password": "default", "city": "Coimbatore"}},
        {"default_8": {"password": "default_1", "city": "Chennai"}},
        {"default_9": {"password": "default_2", "city": "Bangalore"}},
        {"default_10": {"password": "default", "city": "Coimbatore"}},
        {"default_11": {"password": "default_1", "city": "Chennai"}},
        {"default_12": {"password": "default_2", "city": "Bangalore"}},
    ]
}


# @app.get(API_VERSION + "/users")
# async def user():
#     return db


@app.post(API_VERSION + "/users", status_code=201)
async def post_user(user: UserModel):
    username = user.username
    password = user.password
    city = user.city
    db["users"].append({username: {"password": password, "city": city}})
    return {"message": "User created successfully"}


@app.get(API_VERSION + "/users/{username}")
async def get_user_by_username(username: str):
    found = False
    for user in db["users"]:
        if user.get(username):
            found = True
            break
    if found:
        return JSONResponse(
            content={"message": f"User: {username} found in the db"},
            status_code=200,
        )
    return JSONResponse(
        content={"message": f"User: {username} not found in the db"},
        status_code=404,
    )


@app.patch(API_VERSION + "/users", status_code=200)
async def update_user(user: UpdateUser):
    username = user.username
    new_password = user.password
    found = False
    for user in db["users"]:
        if user.get(username):
            found = True
            user[username]["password"] = new_password
            break

    if found:
        return JSONResponse(
            content={"message": f"User {username}'s data successfully updated."},
            status_code=200,
        )
    return JSONResponse(
        content={"message": f"User: {username} not found in the db"},
        status_code=404,
    )


@app.delete(API_VERSION + "/users/{username}")
async def delete_user_by_username(username: str):
    found = False
    for user in db["users"]:
        if user.get(username):
            found = True
            db["users"].pop(db["users"].index(user))
            break
    if found:
        return JSONResponse(
            content={"message": f"User: {username} has been successfully deleted"},
            status_code=200,
        )
    return JSONResponse(
        content={"message": f"User: {username} not found in the db"},
        status_code=404,
    )

@app.get(API_VERSION + "/users")
async def filter_users(city: Optional[str]= None ,limit: Optional[int] = 3, offset: Optional[int] = 0):
    found = False
    username = ""
    if city:
        for user in db["users"]:
            if list(user.values())[0].get("city") == city:
                found = True
                username = list(user.keys())[0]
                break
        if found:
            return JSONResponse(
                content={"message": f"User: {username} found in the db"},
                status_code=200,
            )
        return JSONResponse(
            content={"message": f"User: not found in the db"},
            status_code=404,
        )
    results = []
    for i in range(offset,offset+limit):
        print(offset,limit)
        results.append(db["users"][i])

    return JSONResponse(
            content={"users": results},
            status_code=200,
        )
