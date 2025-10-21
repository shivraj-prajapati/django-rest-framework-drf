# Django REST Framework with PyMongo (No ORM)

A RESTful API built with Django REST Framework that uses PyMongo to interact directly with MongoDB, bypassing Django's ORM completely. This project demonstrates how to build a modern API without using traditional Django models.

## Features

- ✅ Django REST Framework for API development
- ✅ PyMongo for direct MongoDB integration
- ✅ No Django ORM - Pure MongoDB operations
- ✅ Complete CRUD operations
- ✅ Request validation using DRF serializers
- ✅ Clean architecture with separation of concerns
- ✅ RESTful API design principles

## Project Structure

```
django-rest-framework-drf/
├── drf_pymongo_project/          # Django project settings
│   ├── settings.py               # Configuration including MongoDB settings
│   ├── urls.py                   # Main URL configuration
│   └── wsgi.py
├── products/                     # Products API app
│   ├── views.py                  # API views with CRUD operations
│   ├── serializers.py            # DRF serializers for validation
│   ├── urls.py                   # App URL configuration
│   └── mongo_client.py           # MongoDB connection utility
├── manage.py                     # Django management script
└── requirements.txt              # Python dependencies
```

## Prerequisites

- Python 3.8 or higher
- MongoDB server running (locally or remote)
- pip (Python package manager)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/shivraj-prajapati/django-rest-framework-drf.git
cd django-rest-framework-drf
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure MongoDB

Edit `drf_pymongo_project/settings.py` and update the MongoDB connection settings:

```python
MONGO_DB_NAME = 'drf_pymongo_db'  # Your database name
MONGO_URI = 'mongodb://localhost:27017/'  # Your MongoDB URI
```

For MongoDB Atlas (cloud), use:
```python
MONGO_URI = 'mongodb+srv://username:password@cluster.mongodb.net/'
```

### 4. Run migrations (for Django admin and sessions only)

```bash
python manage.py migrate
```

### 5. Start the development server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## API Endpoints

### Products API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products/` | List all products |
| POST | `/api/products/` | Create a new product |
| GET | `/api/products/<id>/` | Get a specific product |
| PUT | `/api/products/<id>/` | Update a product |
| DELETE | `/api/products/<id>/` | Delete a product |

## API Usage Examples

### 1. Create a Product (POST)

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

**Response:**
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

### 2. List All Products (GET)

```bash
curl http://127.0.0.1:8000/api/products/
```

**Response:**
```json
{
  "count": 2,
  "results": [
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
  ]
}
```

### 3. Get a Specific Product (GET)

```bash
curl http://127.0.0.1:8000/api/products/507f1f77bcf86cd799439011/
```

### 4. Update a Product (PUT)

```bash
curl -X PUT http://127.0.0.1:8000/api/products/507f1f77bcf86cd799439011/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Gaming Laptop",
    "description": "High-performance gaming laptop",
    "price": 1299.99,
    "quantity": 45,
    "category": "Electronics"
  }'
```

### 5. Delete a Product (DELETE)

```bash
curl -X DELETE http://127.0.0.1:8000/api/products/507f1f77bcf86cd799439011/
```

**Response:**
```json
{
  "message": "Product deleted successfully"
}
```

## Architecture Overview

### MongoDB Connection (`products/mongo_client.py`)

- Singleton pattern for MongoDB client management
- Centralized database connection
- Easy access to collections throughout the application

### Serializers (`products/serializers.py`)

- Data validation without Django models
- Field-level validation
- Custom validation methods
- Automatic data type conversion

### Views (`products/views.py`)

- Class-based API views using DRF's `APIView`
- Direct PyMongo operations (find, insert_one, update_one, delete_one)
- Proper error handling
- RESTful response formatting

## Key Differences from Django ORM

| Feature | Django ORM | This Project (PyMongo) |
|---------|------------|------------------------|
| Models | Required | Not used |
| Queries | `Model.objects.filter()` | `collection.find()` |
| Create | `Model.objects.create()` | `collection.insert_one()` |
| Update | `instance.save()` | `collection.update_one()` |
| Delete | `instance.delete()` | `collection.delete_one()` |
| Validation | Model validators | Serializer validators |
| Database | SQL databases | MongoDB |

## Benefits of Using PyMongo Directly

1. **Flexibility**: Direct access to MongoDB's full feature set
2. **Performance**: No ORM overhead
3. **Schema-less**: True MongoDB document flexibility
4. **Learning**: Better understanding of MongoDB operations
5. **Control**: Fine-grained control over queries and operations

## Testing the API

You can use the Django REST Framework's browsable API by visiting:
```
http://127.0.0.1:8000/api/products/
```

Or use tools like:
- **Postman**: Import endpoints and test
- **curl**: Command-line testing (examples above)
- **httpie**: Modern CLI HTTP client
- **Thunder Client**: VS Code extension

## Troubleshooting

### MongoDB Connection Issues

1. **Ensure MongoDB is running:**
   ```bash
   # For local MongoDB
   sudo systemctl start mongodb  # Linux
   brew services start mongodb-community  # macOS
   ```

2. **Check connection string:** Verify `MONGO_URI` in `settings.py`

3. **Network access:** For MongoDB Atlas, whitelist your IP address

### Common Errors

- **"ServerSelectionTimeoutError"**: MongoDB server is not accessible
- **"InvalidId"**: Invalid MongoDB ObjectId format in request
- **"ValidationError"**: Request data doesn't match serializer requirements

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open-source and available under the MIT License.

## Contact

For questions or support, please open an issue in the GitHub repository.

## Future Enhancements

- [ ] Add authentication and authorization
- [ ] Implement pagination for list endpoints
- [ ] Add filtering and search capabilities
- [ ] Create unit and integration tests
- [ ] Add API documentation using drf-spectacular or Swagger
- [ ] Implement rate limiting
- [ ] Add caching layer (Redis)
- [ ] Docker containerization

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)
- [MongoDB Documentation](https://docs.mongodb.com/)
