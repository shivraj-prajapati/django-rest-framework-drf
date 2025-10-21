# Quick Start Guide

## Setup Instructions

Follow these steps to get the Django REST API with PyMongo up and running:

### 1. Prerequisites

Ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package manager)
- MongoDB server (local or cloud)

### 2. MongoDB Setup

#### Option A: Local MongoDB

**Install MongoDB:**

- **Ubuntu/Debian:**
  ```bash
  sudo apt-get update
  sudo apt-get install -y mongodb
  sudo systemctl start mongodb
  sudo systemctl enable mongodb
  ```

- **macOS:**
  ```bash
  brew tap mongodb/brew
  brew install mongodb-community
  brew services start mongodb-community
  ```

- **Windows:**
  Download and install from [MongoDB Download Center](https://www.mongodb.com/try/download/community)

**Verify MongoDB is running:**
```bash
mongosh  # or mongo (for older versions)
```

#### Option B: MongoDB Atlas (Cloud)

1. Sign up at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free cluster
3. Create a database user
4. Whitelist your IP address (or use 0.0.0.0/0 for development)
5. Get your connection string (looks like: `mongodb+srv://username:password@cluster.mongodb.net/`)

### 3. Project Setup

**Clone and navigate to the project:**
```bash
git clone https://github.com/shivraj-prajapati/django-rest-framework-drf.git
cd django-rest-framework-drf
```

**Install Python dependencies:**
```bash
pip install -r requirements.txt
```

**Configure MongoDB connection:**

Edit `drf_pymongo_project/settings.py` and update:
```python
MONGO_DB_NAME = 'drf_pymongo_db'  # Your database name
MONGO_URI = 'mongodb://localhost:27017/'  # Your MongoDB URI
```

**Run Django migrations (for admin and sessions):**
```bash
python manage.py migrate
```

**Create a superuser (optional, for Django admin):**
```bash
python manage.py createsuperuser
```

### 4. Start the Server

```bash
python manage.py runserver
```

The API will be available at: `http://127.0.0.1:8000/`

## Testing the API

### Method 1: Using cURL

**Create a product:**
```bash
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "description": "High-performance laptop",
    "price": 999.99,
    "quantity": 50,
    "category": "Electronics"
  }'
```

**List all products:**
```bash
curl http://127.0.0.1:8000/api/products/
```

### Method 2: Using Python Script

We've included a test script for your convenience:

```bash
pip install requests
python test_api.py
```

### Method 3: Using the Browsable API

Visit `http://127.0.0.1:8000/api/products/` in your web browser to use Django REST Framework's interactive API interface.

### Method 4: Using Postman

1. Open Postman
2. Import the endpoints:
   - GET: `http://127.0.0.1:8000/api/products/`
   - POST: `http://127.0.0.1:8000/api/products/`
   - GET: `http://127.0.0.1:8000/api/products/<id>/`
   - PUT: `http://127.0.0.1:8000/api/products/<id>/`
   - DELETE: `http://127.0.0.1:8000/api/products/<id>/`

## Verifying MongoDB Data

You can verify data is being stored in MongoDB:

```bash
# Connect to MongoDB
mongosh  # or mongo

# Switch to the database
use drf_pymongo_db

# List all products
db.products.find().pretty()

# Count products
db.products.countDocuments()
```

## Project Structure Explained

```
django-rest-framework-drf/
│
├── drf_pymongo_project/           # Main Django project
│   ├── __init__.py
│   ├── settings.py               # Django settings with MongoDB config
│   ├── urls.py                   # Main URL routing
│   ├── asgi.py                   # ASGI configuration
│   └── wsgi.py                   # WSGI configuration
│
├── products/                      # Products API application
│   ├── __init__.py
│   ├── admin.py                  # Django admin (not used)
│   ├── apps.py                   # App configuration
│   ├── models.py                 # Django models (not used)
│   ├── mongo_client.py          # ⭐ MongoDB connection utility
│   ├── serializers.py           # ⭐ DRF serializers for validation
│   ├── urls.py                  # ⭐ Products URL routing
│   ├── views.py                 # ⭐ API views with CRUD operations
│   └── tests.py                 # Unit tests
│
├── manage.py                     # Django management script
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
├── test_api.py                   # API testing script
├── README.md                     # Main documentation
└── SETUP.md                      # This file
```

## Common Issues and Solutions

### Issue 1: MongoDB Connection Error

**Error:** `ServerSelectionTimeoutError`

**Solution:**
- Ensure MongoDB is running: `sudo systemctl status mongodb`
- Check the connection string in `settings.py`
- For MongoDB Atlas, ensure your IP is whitelisted

### Issue 2: Port Already in Use

**Error:** `Error: That port is already in use.`

**Solution:**
Run the server on a different port:
```bash
python manage.py runserver 8080
```

### Issue 3: Module Not Found

**Error:** `ModuleNotFoundError: No module named 'rest_framework'`

**Solution:**
Install all dependencies:
```bash
pip install -r requirements.txt
```

### Issue 4: Invalid ObjectId

**Error:** `Invalid product ID format`

**Solution:**
Ensure you're using a valid MongoDB ObjectId (24-character hex string) when accessing specific products.

## API Response Formats

### Success Responses

**Create/Update Product:**
```json
{
  "_id": "507f1f77bcf86cd799439011",
  "name": "Laptop",
  "description": "High-performance laptop",
  "price": "999.99",
  "quantity": 50,
  "category": "Electronics",
  "created_at": "2024-01-15T10:30:00.000Z",
  "updated_at": "2024-01-15T10:30:00.000Z"
}
```

**List Products:**
```json
{
  "count": 2,
  "results": [...]
}
```

### Error Responses

**Validation Error (400):**
```json
{
  "name": ["This field is required."],
  "price": ["Price must be a positive value."]
}
```

**Not Found (404):**
```json
{
  "error": "Product not found"
}
```

**Server Error (500):**
```json
{
  "error": "Failed to create product: connection timeout"
}
```

## Environment Variables

For production, use environment variables:

1. Install python-decouple:
   ```bash
   pip install python-decouple
   ```

2. Create a `.env` file (see `.env.example`)

3. Update `settings.py`:
   ```python
   from decouple import config
   
   MONGO_URI = config('MONGO_URI')
   MONGO_DB_NAME = config('MONGO_DB_NAME')
   SECRET_KEY = config('SECRET_KEY')
   DEBUG = config('DEBUG', default=False, cast=bool)
   ```

## Next Steps

After successfully setting up the project:

1. **Explore the code:** Understand how PyMongo is used without Django ORM
2. **Add features:** Implement pagination, filtering, or search
3. **Secure the API:** Add authentication (JWT, OAuth)
4. **Write tests:** Create unit and integration tests
5. **Deploy:** Deploy to Heroku, AWS, or other cloud platforms

## Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Review the code comments in `products/views.py` and `products/mongo_client.py`
- Open an issue on GitHub if you encounter problems

## Useful Commands

```bash
# Run development server
python manage.py runserver

# Check for project issues
python manage.py check

# Create migrations (not needed for MongoDB, but useful for Django admin)
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Open Python shell with Django context
python manage.py shell

# Run tests
python manage.py test
```

Happy coding! 🚀
