from app.database import SessionLocal
from app.models import User
from app.auth import hash_password

db = SessionLocal()

admin = User(
    name="Admin User",
    email="admin@ecommerce.com",
    password=hash_password("Admin@123"),
    role="admin"
)

db.add(admin)
db.commit()

print("Admin created successfully")
print("Email: admin@ecommerce.com")
print("Password: Admin@123")

db.close()