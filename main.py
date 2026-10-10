from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import User, Product
from .schemas import (
    UserRegister,
    UserResponse,
    UserLogin,
    ProductCreate,
    ProductResponse
)
from .auth import hash_password, verify_password
from .security import create_access_token
from .dependencies import get_current_user, get_current_admin


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="E-Commerce API",
    description="E-Commerce API for Postman API Testing Practice",
    version="1.0.0"
)


# =========================================================
# HOME / HEALTH
# =========================================================

@app.get("/")
def home():
    return {
        "message": "E-Commerce API is running",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {
        "status": "UP"
    }


# =========================================================
# AUTHENTICATION - REGISTER
# =========================================================

@app.post(
    "/api/auth/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    # Check whether email already exists
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Create new customer
    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role="customer"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# =========================================================
# AUTHENTICATION - LOGIN
# =========================================================

@app.post("/api/auth/login")
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    # Find user by email
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    # User does not exist
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(
        user.password,
        existing_user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Create JWT with user ID and role
    access_token = create_access_token(
        data={
            "sub": str(existing_user.id),
            "role": existing_user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# =========================================================
# AUTHORIZATION - CURRENT USER
# =========================================================

@app.get(
    "/api/auth/me",
    response_model=UserResponse
)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user


# =========================================================
# PRODUCTS - CREATE
# ADMIN ONLY
# =========================================================

@app.post(
    "/api/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):

    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=product.quantity,
        category=product.category
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


# =========================================================
# PRODUCTS - GET ALL
# PUBLIC
# =========================================================

@app.get(
    "/api/products",
    response_model=list[ProductResponse]
)
def get_all_products(
    db: Session = Depends(get_db)
):

    products = db.query(Product).all()

    return products


# =========================================================
# PRODUCTS - SEARCH
# PUBLIC
# =========================================================

@app.get(
    "/api/products/search",
    response_model=list[ProductResponse]
)
def search_products(
    keyword: str,
    db: Session = Depends(get_db)
):

    products = db.query(Product).filter(
        (Product.name.ilike(f"%{keyword}%")) |
        (Product.category.ilike(f"%{keyword}%"))
    ).all()

    return products


# =========================================================
# PRODUCTS - GET BY ID
# PUBLIC
# =========================================================

@app.get(
    "/api/products/{product_id}",
    response_model=ProductResponse
)
def get_product_by_id(
    product_id: int,
    db: Session = Depends(get_db)
):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return product


# =========================================================
# PRODUCTS - UPDATE
# ADMIN ONLY
# =========================================================

@app.put(
    "/api/products/{product_id}",
    response_model=ProductResponse
)
def update_product(
    product_id: int,
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):

    existing_product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not existing_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    existing_product.name = product.name
    existing_product.description = product.description
    existing_product.price = product.price
    existing_product.quantity = product.quantity
    existing_product.category = product.category

    db.commit()
    db.refresh(existing_product)

    return existing_product


# =========================================================
# PRODUCTS - DELETE
# ADMIN ONLY
# =========================================================

@app.delete(
    "/api/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    db.delete(product)
    db.commit()

    return None