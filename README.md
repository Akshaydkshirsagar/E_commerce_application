# E-Commerce API Testing Project

## 1. Project Overview

The **E-Commerce API QA Testing Project** is a Python-based REST API application developed using FastAPI to practice and demonstrate manual API testing, functional testing, negative testing, authentication, authorization, and API automation using Postman.

The project simulates core e-commerce backend functionality, including user registration, login, JWT authentication, role-based access control (RBAC), and product management.

The primary objective is to validate API functionality, verify HTTP status codes and response payloads, test security controls, and maintain a structured QA test suite.

## 2. Objectives

* Perform functional and negative API testing.
* Validate request payloads, response bodies, and HTTP status codes.
* Test user registration and login functionality.
* Verify JWT-based authentication.
* Validate role-based access control for admin and customer users.
* Test product CRUD operations and product search.
* Automate API assertions using Postman test scripts.
* Maintain test cases and execution results in Excel.
* Practice defect identification, reporting, retesting, and regression testing.

## 3. Technology Stack

| Technology / Tool | Purpose                                        |
| ----------------- | ---------------------------------------------- |
| Python            | Backend programming language                   |
| FastAPI           | REST API framework                             |
| SQLAlchemy        | Database ORM                                   |
| SQLite            | Database                                       |
| Pydantic          | Request validation and response schemas        |
| JWT               | Token-based authentication                     |
| bcrypt            | Password hashing                               |
| Swagger UI        | Interactive API exploration and testing        |
| Postman           | API execution and automated assertions         |
| Excel             | Test case documentation and execution tracking |
| Git               | Version control                                |

## 4. Application Features

### Authentication

* User registration
* User login
* Password hashing
* JWT access token generation
* Current-user details endpoint
* Invalid credential validation

### Authorization and RBAC

The application supports two roles:

* **Admin:** Can create, update, and delete products.
* **Customer:** Can access authenticated user functionality but cannot perform admin-only product operations.

Unauthorized admin operations return HTTP `403 Forbidden`.

Missing, invalid, or expired authentication tokens are handled through authentication validation.

### Product Management

* Create a product
* Retrieve all products
* Retrieve a product by ID
* Search products by name or category
* Update product details
* Delete a product
* Validate nonexistent product IDs and invalid request data

## 5. Project Structure

```text
ecommerce-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── security.py
│   └── dependencies.py
├── venv/
├── create_admin.py
├── ecommerce.db
└── README.md
```

### Key Files

* `main.py` — API routes and endpoint logic.
* `database.py` — SQLite database connection and session management.
* `models.py` — SQLAlchemy database models.
* `schemas.py` — Request validation and response schemas.
* `auth.py` — Password hashing and verification.
* `security.py` — JWT token creation and verification.
* `dependencies.py` — Authentication and role-based authorization dependencies.
* `create_admin.py` — Script to create the initial admin account.
* `ecommerce.db` — Local SQLite database.

## 6. Setup and Installation

### Prerequisites

* Python installed
* pip package manager
* Postman
* Git (optional)

### Step 1: Navigate to the Project

```bash
cd "C:\Akshay Work\Python\ecommerce-api"
```

### Step 2: Create and Activate a Virtual Environment

If the virtual environment already exists, activate it:

```bash
venv\Scripts\activate
```

### Step 3: Install Dependencies

Install the required packages used by the application:

```bash
pip install fastapi uvicorn sqlalchemy pydantic[email] python-jose bcrypt
```

### Step 4: Start the API Server

```bash
python -m uvicorn app.main:app --reload
```

The server should start at `http://127.0.0.1:8000`.

## 7. API Documentation

After starting the server, use the following URLs:

| URL                                  | Purpose               |
| ------------------------------------ | --------------------- |
| `http://127.0.0.1:8000/`             | API home endpoint     |
| `http://127.0.0.1:8000/health`       | Health check          |
| `http://127.0.0.1:8000/docs`         | Swagger UI            |
| `http://127.0.0.1:8000/openapi.json` | OpenAPI specification |

Swagger UI can be used to explore endpoints, submit requests, inspect responses, and test authenticated operations.

## 8. API Endpoints

| Method | Endpoint                             | Description                            |
| ------ | ------------------------------------ | -------------------------------------- |
| POST   | `/api/auth/register`                 | Register a customer                    |
| POST   | `/api/auth/login`                    | Authenticate a user and generate a JWT |
| GET    | `/api/auth/me`                       | Retrieve current authenticated user    |
| POST   | `/api/products`                      | Create a product — admin only          |
| GET    | `/api/products`                      | Retrieve all products                  |
| GET    | `/api/products/search?keyword=phone` | Search products by name or category    |
| GET    | `/api/products/{product_id}`         | Retrieve a product by ID               |
| PUT    | `/api/products/{product_id}`         | Update a product — admin only          |
| DELETE | `/api/products/{product_id}`         | Delete a product — admin only          |

## 9. Authentication and Authorization Testing

The login endpoint returns an access token after successful authentication.

The token is supplied in the HTTP authorization header:

```http
Authorization: Bearer <access_token>
```

The application uses JWT authentication and role-based authorization to protect admin-only operations.

Test scenarios include:

* Valid and invalid login credentials
* Missing or malformed request fields
* Successful token generation
* Access to authenticated endpoints
* Admin access to product management
* Customer attempts to perform admin-only operations
* Missing, invalid, and expired tokens

## 10. Test Approach

The project uses a combination of manual API testing and Postman-based automated assertions.

### Functional Testing

Validate successful execution of registration, login, product retrieval, product creation, update, deletion, and search operations.

### Negative Testing

Validate invalid credentials, missing fields, invalid input formats, nonexistent resources, and unauthorized requests.

### Validation Testing

Check mandatory fields, data types, field length restrictions, and business validation rules.

### Security Testing

Verify password hashing, token validation, role-based access control, and that sensitive information is not exposed in API responses.

### Regression Testing

Re-execute previously validated test scenarios after application changes to identify unintended impact.

### Response Validation

Verify HTTP status codes, response JSON structure, error messages, and important response fields.

## 11. Postman Test Suite

Postman is used to execute API requests and validate responses using JavaScript test scripts.

The collection is organized into functional folders:

* Authentication
* Authorization
* Products
* Cart
* Payment
* Orders

**Current implementation status:** Authentication, authorization, and product management are implemented. Cart, payment, and order functionality are planned collection areas and should not be considered implemented until their endpoints are developed and verified.

Postman environment variables are used to manage values such as:

* `base_url`
* `token`
* `admin_token`
* `customer_token`
* `product_id`

Example automated assertion:

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response contains access token", function () {
    pm.expect(pm.response.json().access_token).to.exist;
});
```

## 12. Test Case Management and Reporting

Test cases are maintained in an Excel workbook with test scenarios, test steps, expected results, actual results, execution status, and related test data.

The test suite covers registration, login, JWT authorization, and product APIs.

Test execution results are tracked using statuses such as:

* Passed
* Failed
* Blocked
* Not Executed

Defects identified during execution can be documented with reproduction steps, expected and actual results, severity, and supporting evidence.

## 13. Key QA Skills Demonstrated

* REST API testing
* HTTP methods and status codes
* JSON request and response validation
* Positive and negative testing
* Boundary-value and input-validation testing
* JWT authentication
* Role-based access control
* Postman collection development
* JavaScript assertions and environment variables
* SQL and database fundamentals
* Defect reporting and regression testing
* Test case design and execution reporting

## 14. Future Enhancements

* Implement shopping cart APIs.
* Implement order creation and tracking.
* Implement payment simulation.
* Add automated API regression tests using Python and `pytest`.
* Integrate API tests into a CI/CD pipeline using GitLab CI or GitHub Actions.
* Deploy the application to a cloud environment.
* Add pagination, filtering, and sorting for product listings.
* Improve configuration and secret management for production readiness.

## 15. Important Notes

This project is intended for QA learning and demonstration. It currently uses a local SQLite database and a development configuration. The JWT secret key and credentials must be replaced with secure configuration before deployment.

The payment functionality is not implemented merely because a Postman folder exists for it. Do not use real payment credentials or real customer data in this practice project.
