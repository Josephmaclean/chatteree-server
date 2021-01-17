import uvicorn
from fastapi import FastAPI
from app.api.routes import users
from app.db.session import SessionLocal, engine
from app.models import user_model

user_model.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)