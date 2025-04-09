🛒 E-commerce Django Project

This is a full-featured e-commerce web application built using Django.

##  Features

- User registration and authentication
- Product listing and detail pages
- Shopping cart functionality
- Order management
- Admin panel for managing products and orders
- Responsive design
- Users
Register and log in with JWT authentication
Update and retrieve user profiles
Admin-only: List all users, delete users, update user details
-Products
Retrieve all products (with keyword search) and individual products
Admin-only: Create, update, and delete products; upload product images
Authenticated users: Add product reviews
-Orders
Authenticated users: Create orders with items, retrieve personal orders, mark orders as paid
Admin-only: List all orders, mark orders as delivered
-Prerequisites
Python 3.13.1 (or compatible version)
Git (optional, for version control)


### 1. Clone the Repository

```bash
git clone https://github.com/mohammednabil23/django-graduation-project-amit.git
cd ecommerce-django
2. Create and Activate Virtual Environment
venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. Run Migrations
python manage.py makemigrations
python manage.py migrate
5. Run the Server
python manage.py runserver
6. Create Superuser (for admin access)
python manage.py createsuperuser
## Environment Variables
Create a .env file to store secret keys and environment settings:
env
SECRET_KEY=your-secret-key
DEBUG=True
## screens from project:
![home](https://github.com/user-attachments/assets/d77a830c-6e82-4bb6-a6f8-0371f0ea4917)
![orders](https://github.com/user-attachments/assets/a7ee6f88-877e-4087-b18f-a885b3af6163)
![user profile](https://github.com/user-attachments/assets/ccf643b1-f1bd-4823-bccb-fa108fde1fa6)
![authintication](https://github.com/user-attachments/assets/28473a16-1128-4923-b1b0-7b68cb7ea3b2)
![products](https://github.com/user-attachments/assets/f11fec55-a213-48f8-9a6a-03f620266972)

API Endpoints
-Users
POST /api/users/register/ - Register a new user
POST /api/users/login/ - Log in and get JWT
PUT /api/users/profile/update/ - Update user profile (authenticated)
GET /api/users/profile/ - Get user profile (authenticated)
GET /api/users/ - List all users (admin)
DELETE /api/users/<pk>/delete/ - Delete a user (admin)
GET /api/users/<pk>/ - Get user by ID (admin)
PUT /api/users/<pk>/update/ - Update user by ID (admin)
-Products
GET /api/products/ - List all products (optional ?keyword=<search>)
GET /api/products/<pk>/ - Get product by ID
DELETE /api/products/<pk>/delete/ - Delete product (admin)
POST /api/products/create/ - Create product (admin)
PUT /api/products/<pk>/update/ - Update product (admin)
POST /api/products/<pk>/upload/ - Upload product image (admin)
POST /api/products/<pk>/review/ - Add product review (authenticated)
-Orders
POST /api/orders/add/ - Create an order (authenticated)
GET /api/orders/<pk>/ - Get order by ID (authenticated, owner or admin)
PUT /api/orders/<pk>/pay/ - Mark order as paid (authenticated, owner)
GET /api/orders/myorders/ - List user’s orders (authenticated)
GET /api/orders/ - List all orders (admin)
PUT /api/orders/<pk>/deliver/ - Mark order as delivered (admin)

