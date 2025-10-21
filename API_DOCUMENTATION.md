# API Documentation

## Overview

This API provides CRUD operations for managing products using MongoDB as the database. All operations use PyMongo directly without Django ORM.

## Base URL

```
http://127.0.0.1:8000/api/products/
```

## Authentication

Currently, this API does not require authentication. For production use, implement authentication mechanisms like:
- Token Authentication (DRF Token Auth)
- JWT (JSON Web Tokens)
- OAuth 2.0
- Session Authentication

## Data Model

### Product Schema

```json
{
  "_id": "string (MongoDB ObjectId)",
  "name": "string (required, max 200 characters)",
  "description": "string (optional)",
  "price": "decimal (required, must be positive)",
  "quantity": "integer (required, must be >= 0)",
  "category": "string (optional, max 100 characters)",
  "created_at": "datetime (auto-generated)",
  "updated_at": "datetime (auto-updated)"
}
```

## Endpoints

### 1. List All Products

**Endpoint:** `GET /api/products/`

**Description:** Retrieve a list of all products from the database.

**Request:**
```bash
curl -X GET http://127.0.0.1:8000/api/products/
```

**Response (200 OK):**
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
    },
    {
      "_id": "507f1f77bcf86cd799439012",
      "name": "Mouse",
      "description": "Wireless mouse",
      "price": "29.99",
      "quantity": 100,
      "category": "Accessories",
      "created_at": "2024-01-15T11:00:00.000Z",
      "updated_at": "2024-01-15T11:00:00.000Z"
    }
  ]
}
```

**Error Response (500 Internal Server Error):**
```json
{
  "error": "Failed to retrieve products: connection timeout"
}
```

---

### 2. Create a Product

**Endpoint:** `POST /api/products/`

**Description:** Create a new product in the database.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Laptop",
  "description": "High-performance laptop for developers",
  "price": 1299.99,
  "quantity": 25,
  "category": "Electronics"
}
```

**cURL Example:**
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

**Response (201 Created):**
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

**Error Response (400 Bad Request):**
```json
{
  "name": ["This field is required."],
  "price": ["Price must be a positive value."]
}
```

**Error Response (500 Internal Server Error):**
```json
{
  "error": "Failed to create product: database connection error"
}
```

**Field Validations:**
- `name`: Required, cannot be empty
- `description`: Optional
- `price`: Required, must be positive
- `quantity`: Required, must be >= 0
- `category`: Optional

---

### 3. Get a Specific Product

**Endpoint:** `GET /api/products/{product_id}/`

**Description:** Retrieve a specific product by its MongoDB ObjectId.

**URL Parameters:**
- `product_id` (required): MongoDB ObjectId (24-character hexadecimal string)

**Request:**
```bash
curl -X GET http://127.0.0.1:8000/api/products/507f1f77bcf86cd799439011/
```

**Response (200 OK):**
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

**Error Response (404 Not Found):**
```json
{
  "error": "Product not found"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Invalid product ID format"
}
```

**Error Response (500 Internal Server Error):**
```json
{
  "error": "Failed to retrieve product: database error"
}
```

---

### 4. Update a Product

**Endpoint:** `PUT /api/products/{product_id}/`

**Description:** Update an existing product by its MongoDB ObjectId.

**URL Parameters:**
- `product_id` (required): MongoDB ObjectId

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Gaming Laptop",
  "description": "High-performance gaming laptop with RGB",
  "price": 1599.99,
  "quantity": 20,
  "category": "Electronics"
}
```

**cURL Example:**
```bash
curl -X PUT http://127.0.0.1:8000/api/products/507f1f77bcf86cd799439011/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Gaming Laptop",
    "description": "High-performance gaming laptop",
    "price": 1599.99,
    "quantity": 20,
    "category": "Electronics"
  }'
```

**Response (200 OK):**
```json
{
  "_id": "507f1f77bcf86cd799439011",
  "name": "Gaming Laptop",
  "description": "High-performance gaming laptop with RGB",
  "price": "1599.99",
  "quantity": 20,
  "category": "Electronics",
  "created_at": "2024-01-15T10:30:00.000Z",
  "updated_at": "2024-01-15T14:30:00.000Z"
}
```

**Error Response (404 Not Found):**
```json
{
  "error": "Product not found"
}
```

**Error Response (400 Bad Request):**
```json
{
  "name": ["This field is required."],
  "price": ["Price must be a positive value."]
}
```

**Error Response (500 Internal Server Error):**
```json
{
  "error": "Failed to update product: database error"
}
```

**Note:** All fields must be provided in the update request (full update, not partial).

---

### 5. Delete a Product

**Endpoint:** `DELETE /api/products/{product_id}/`

**Description:** Delete a product by its MongoDB ObjectId.

**URL Parameters:**
- `product_id` (required): MongoDB ObjectId

**Request:**
```bash
curl -X DELETE http://127.0.0.1:8000/api/products/507f1f77bcf86cd799439011/
```

**Response (200 OK):**
```json
{
  "message": "Product deleted successfully"
}
```

**Error Response (404 Not Found):**
```json
{
  "error": "Product not found"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Invalid product ID format"
}
```

**Error Response (500 Internal Server Error):**
```json
{
  "error": "Failed to delete product: database error"
}
```

---

## HTTP Status Codes

The API uses the following HTTP status codes:

| Code | Description |
|------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid request data or parameters |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error - Server-side error |

## Rate Limiting

Currently, there is no rate limiting implemented. For production:
- Consider implementing rate limiting using Django REST Framework throttling
- Use Redis for distributed rate limiting
- Implement per-user or per-IP rate limits

## Pagination

Pagination is not currently implemented. Future implementation could include:

```json
{
  "count": 100,
  "next": "http://api.example.com/products/?page=2",
  "previous": null,
  "results": [...]
}
```

## Filtering and Search

Not currently implemented. Future enhancements:

**Filter by category:**
```
GET /api/products/?category=Electronics
```

**Search by name:**
```
GET /api/products/?search=laptop
```

**Price range:**
```
GET /api/products/?min_price=100&max_price=1000
```

## CORS (Cross-Origin Resource Sharing)

For frontend applications running on different domains:

1. Install django-cors-headers:
   ```bash
   pip install django-cors-headers
   ```

2. Update settings.py:
   ```python
   INSTALLED_APPS = [
       ...
       'corsheaders',
   ]
   
   MIDDLEWARE = [
       'corsheaders.middleware.CorsMiddleware',
       ...
   ]
   
   CORS_ALLOWED_ORIGINS = [
       "http://localhost:3000",
       "http://localhost:8080",
   ]
   ```

## Error Handling

The API provides consistent error responses:

### Validation Errors (400)
```json
{
  "field_name": ["Error message"],
  "another_field": ["Another error message"]
}
```

### Not Found Errors (404)
```json
{
  "error": "Resource not found"
}
```

### Server Errors (500)
```json
{
  "error": "Detailed error message"
}
```

## MongoDB ObjectId Format

MongoDB ObjectIds are 24-character hexadecimal strings, for example:
- Valid: `507f1f77bcf86cd799439011`
- Invalid: `123`, `invalid-id`, `507f1f77`

## Testing with Different Tools

### Using curl
```bash
# List products
curl http://127.0.0.1:8000/api/products/

# Create product
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","price":10.99,"quantity":5}'
```

### Using Python requests
```python
import requests

# List products
response = requests.get('http://127.0.0.1:8000/api/products/')
print(response.json())

# Create product
data = {"name": "Test", "price": 10.99, "quantity": 5}
response = requests.post('http://127.0.0.1:8000/api/products/', json=data)
print(response.json())
```

### Using httpie
```bash
# List products
http GET http://127.0.0.1:8000/api/products/

# Create product
http POST http://127.0.0.1:8000/api/products/ \
  name="Test" price:=10.99 quantity:=5
```

## Best Practices

1. **Always validate input data** - Use serializers for validation
2. **Handle errors gracefully** - Provide meaningful error messages
3. **Use proper HTTP methods** - GET, POST, PUT, DELETE
4. **Secure your API** - Implement authentication and authorization
5. **Version your API** - Use URL versioning (e.g., /api/v1/products/)
6. **Log requests and errors** - For debugging and monitoring
7. **Implement rate limiting** - Prevent abuse
8. **Use HTTPS in production** - Secure data transmission

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check the README.md for setup instructions
- Review the code in the repository

## License

This API is open-source and available under the MIT License.
