from fastapi import FastAPI
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .auth import router as auth_router, hash_password
from .reports import router as reports_router
from . import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(reports_router)

def create_admin():
    db: Session = next(get_db())
    admin = db.query(models.User).filter_by(username="admin").first()
    if not admin:
        admin_user = models.User(
            username="admin",
            password=hash_password("admin123"),
            role="admin"
        )
        db.add(admin_user)
        db.commit()
        print("Admin user created (username: admin, password: admin123)")
    else:
        print("Admin already exists")

create_admin()
