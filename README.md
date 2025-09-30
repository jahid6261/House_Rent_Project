#  House Rent Project

A **House Rent Management System** built with **Django REST Framework**.  
This project allows users to post rent advertisements, request to rent a house, add reviews, manage favorites, and more.  
Admins can manage all products, categories, and user activities.

---

##  Features

-  **User Authentication**
  - Registration, Login, Logout
  - Email verification
  - Role-based access (Admin / User)

-  **Rent Advertisement**
  - Create, update, delete, approve advertisements
  - Upload multiple product images

-  **User Interactions**
  - Review system
  - Favorite system
  - Rent request system

-  **Extra Features**
  - Filtering, searching, and ordering products
  - Pagination support
  - Swagger API documentation

---

##  Tech Stack

- **Backend:** Django, Django REST Framework  
- **Database:** SQLite / PostgreSQL  
- **Authentication:** dj-rest-auth, JWT / Session  
- **Other Packages:** Django Filters, drf-yasg (Swagger), Pillow  

---

##  Installation

1. Clone the repository
   ```bash
   git clone https://github.com/your-username/house_rent_project.git
   cd house_rent_project
Create and activate virtual environment

bash
Copy code
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
Install dependencies

bash
Copy code
pip install -r requirements.txt
Run migrations

bash
Copy code
python manage.py migrate
Start the server

bash
Copy code
python manage.py runserver
Visit API root
 http://127.0.0.1:8000/api/v1/

🔗 API Endpoints (Examples)
Authentication
POST /api/v1/auth/register/ → Register User

POST /api/v1/auth/login/ → Login User

POST /api/v1/auth/logout/ → Logout User

Products
GET /api/v1/products/ → List all products

POST /api/v1/products/ → Create a product (Admin only)

GET /api/v1/products/{id}/ → Retrieve product details

Reviews
GET /api/v1/products/{id}/reviews/ → List product reviews

POST /api/v1/products/{id}/reviews/ → Create a review

Favorites
GET /api/v1/products/{id}/favorites/ → List favorites

POST /api/v1/products/{id}/favorites/ → Add to favorites

Rent Requests
GET /api/v1/products/{id}/rent-requests/ → List rent requests

POST /api/v1/products/{id}/rent-requests/ → Send rent request

 Project Structure
bash
Copy code
house_rent_project/
├── api/
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── product/
│   ├── models.py
│   ├── views.py
│   └── filters.py
├── users/
│   ├── models.py
│   ├── views.py
│   └── serializers.py
├── requirements.txt
├── manage.py
└── README.md