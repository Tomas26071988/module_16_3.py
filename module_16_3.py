from fastapi import FastAPI, Path, HTTPException
from typing import Dict, Any, Tuple, Annotated

app = FastAPI()

# Инициализация словаря пользователей
users: Dict[str, str] = {'1': 'NAME: Example, AGE: 18'}


@app.get("/users")
async def get_users() -> Dict[str, str]:
    return users


@app.post("/user/{username}/{age}")
async def create_user(
        username: Annotated[str, Path(description="Enter username", min_length=1, max_length=50)],
        age: Annotated[int, Path(ge=18, le=120, description="Enter age")]
) -> str:
    # Определение нового user_id
    new_user_id = str(max(map(int, users.keys())) + 1)
    users[new_user_id] = f'NAME: {username}, AGE: {age}'
    return f"User {new_user_id} is registered"


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(
        user_id: Annotated[str, Path(description="User ID", min_length=1, max_length=10)],
        username: Annotated[str, Path(description="Enter username", min_length=1, max_length=50)],
        age: Annotated[int, Path(ge=18, le=120, description="Enter age")]
) -> str:
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    users[user_id] = f'NAME: {username}, AGE: {age}'
    return f"User {user_id} has been updated"


@app.delete("/user/{user_id}")
async def delete_user(
        user_id: Annotated[str, Path(description="User ID", min_length=1, max_length=10)]
) -> str:
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    del users[user_id]
    return f"User {user_id} has been deleted"
