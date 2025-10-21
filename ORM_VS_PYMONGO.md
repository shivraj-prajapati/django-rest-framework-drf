# Django ORM vs PyMongo Comparison

## Overview

This document illustrates the key differences between using Django's ORM and PyMongo for database operations in a Django REST Framework application.

## Architecture Comparison

### Django ORM Architecture
```
Client Request → Django View → Django Model (ORM) → Database Driver → SQL Database
```

### PyMongo Architecture (This Project)
```
Client Request → Django View → PyMongo Client → MongoDB
```

## Code Comparison

### 1. Model Definition

#### Django ORM Approach
```python
# models.py
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    category = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'products'
```

#### PyMongo Approach (This Project)
```python
# No models.py needed!
# Data structure is defined in serializers for validation only

# serializers.py
from rest_framework import serializers

class ProductSerializer(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=200, required=True)
    description = serializers.CharField(required=False, allow_blank=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField(min_value=0)
    category = serializers.CharField(max_length=100, required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
```

### 2. Database Connection

#### Django ORM Approach
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

#### PyMongo Approach (This Project)
```python
# settings.py
MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DB_NAME = 'drf_pymongo_db'

# mongo_client.py
from pymongo import MongoClient
from django.conf import settings

class MongoDBClient:
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBClient, cls).__new__(cls)
            cls._client = MongoClient(settings.MONGO_URI)
            cls._db = cls._client[settings.MONGO_DB_NAME]
        return cls._instance

    def get_collection(self, collection_name):
        return self._db[collection_name]

mongo_client = MongoDBClient()
```

### 3. CREATE Operation

#### Django ORM Approach
```python
# views.py
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Or using APIView:
def post(self, request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # ORM handles the database insert
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
```

#### PyMongo Approach (This Project)
```python
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from .mongo_client import mongo_client
from .serializers import ProductSerializer

def post(self, request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        collection = mongo_client.get_collection('products')
        
        # Prepare document with timestamps
        product_data = serializer.validated_data
        product_data['created_at'] = datetime.utcnow()
        product_data['updated_at'] = datetime.utcnow()
        
        # Direct MongoDB insert
        result = collection.insert_one(product_data)
        
        # Retrieve inserted document
        inserted_product = collection.find_one({'_id': result.inserted_id})
        inserted_product['_id'] = str(inserted_product['_id'])
        
        return Response(inserted_product, status=201)
    return Response(serializer.errors, status=400)
```

### 4. READ Operation (List All)

#### Django ORM Approach
```python
def get(self, request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
```

#### PyMongo Approach (This Project)
```python
def get(self, request):
    collection = mongo_client.get_collection('products')
    products = list(collection.find())
    
    # Convert ObjectId to string for JSON serialization
    for product in products:
        product['_id'] = str(product['_id'])
    
    return Response({
        'count': len(products),
        'results': products
    })
```

### 5. READ Operation (Get One)

#### Django ORM Approach
```python
from django.shortcuts import get_object_or_404

def get(self, request, product_id):
    product = get_object_or_404(Product, id=product_id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)
```

#### PyMongo Approach (This Project)
```python
from bson import ObjectId
from bson.errors import InvalidId

def get(self, request, product_id):
    try:
        collection = mongo_client.get_collection('products')
        product = collection.find_one({'_id': ObjectId(product_id)})
        
        if product:
            product['_id'] = str(product['_id'])
            return Response(product)
        else:
            return Response({'error': 'Product not found'}, status=404)
    except InvalidId:
        return Response({'error': 'Invalid product ID format'}, status=400)
```

### 6. UPDATE Operation

#### Django ORM Approach
```python
def put(self, request, product_id):
    product = get_object_or_404(Product, id=product_id)
    serializer = ProductSerializer(product, data=request.data)
    if serializer.is_valid():
        serializer.save()  # ORM handles the update
        return Response(serializer.data)
    return Response(serializer.errors, status=400)
```

#### PyMongo Approach (This Project)
```python
def put(self, request, product_id):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        collection = mongo_client.get_collection('products')
        
        # Check if product exists
        existing = collection.find_one({'_id': ObjectId(product_id)})
        if not existing:
            return Response({'error': 'Product not found'}, status=404)
        
        # Prepare update data
        update_data = serializer.validated_data
        update_data['updated_at'] = datetime.utcnow()
        
        # Direct MongoDB update
        collection.update_one(
            {'_id': ObjectId(product_id)},
            {'$set': update_data}
        )
        
        # Retrieve updated document
        updated_product = collection.find_one({'_id': ObjectId(product_id)})
        updated_product['_id'] = str(updated_product['_id'])
        
        return Response(updated_product)
    return Response(serializer.errors, status=400)
```

### 7. DELETE Operation

#### Django ORM Approach
```python
def delete(self, request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()  # ORM handles the deletion
    return Response({'message': 'Product deleted successfully'})
```

#### PyMongo Approach (This Project)
```python
def delete(self, request, product_id):
    collection = mongo_client.get_collection('products')
    
    # Check if product exists
    existing = collection.find_one({'_id': ObjectId(product_id)})
    if not existing:
        return Response({'error': 'Product not found'}, status=404)
    
    # Direct MongoDB delete
    collection.delete_one({'_id': ObjectId(product_id)})
    
    return Response({'message': 'Product deleted successfully'})
```

### 8. Advanced Queries

#### Django ORM Approach
```python
# Filter by category
products = Product.objects.filter(category='Electronics')

# Filter by price range
products = Product.objects.filter(price__gte=100, price__lte=1000)

# Search by name
products = Product.objects.filter(name__icontains='laptop')

# Order by price
products = Product.objects.order_by('-price')

# Aggregate
from django.db.models import Avg, Sum
stats = Product.objects.aggregate(
    avg_price=Avg('price'),
    total_quantity=Sum('quantity')
)
```

#### PyMongo Approach
```python
# Filter by category
products = collection.find({'category': 'Electronics'})

# Filter by price range
products = collection.find({
    'price': {'$gte': 100, '$lte': 1000}
})

# Search by name (case-insensitive regex)
products = collection.find({
    'name': {'$regex': 'laptop', '$options': 'i'}
})

# Order by price
products = collection.find().sort('price', -1)

# Aggregate
pipeline = [
    {
        '$group': {
            '_id': None,
            'avg_price': {'$avg': '$price'},
            'total_quantity': {'$sum': '$quantity'}
        }
    }
]
stats = list(collection.aggregate(pipeline))
```

## Feature Comparison Table

| Feature | Django ORM | PyMongo (This Project) |
|---------|------------|------------------------|
| **Schema** | Rigid (defined in models) | Flexible (schema-less) |
| **Migrations** | Required | Not required |
| **Database** | SQL (PostgreSQL, MySQL, SQLite) | NoSQL (MongoDB) |
| **Query Language** | Django QuerySet API | MongoDB Query Language |
| **Relationships** | Built-in (ForeignKey, ManyToMany) | Manual implementation |
| **Transactions** | Built-in | Manual with sessions |
| **Validation** | Model-level + Serializer | Serializer only |
| **Admin Interface** | Automatic | Manual implementation needed |
| **Learning Curve** | Moderate | Steeper (need to know MongoDB) |
| **Performance** | Good (with optimizations) | Excellent (no ORM overhead) |
| **Flexibility** | Limited to SQL databases | Full MongoDB features |
| **Type Safety** | Enforced by database schema | Application-level only |

## Pros and Cons

### Django ORM

**Pros:**
- ✅ Automatic admin interface
- ✅ Built-in migrations
- ✅ Type safety at database level
- ✅ Easy relationship handling
- ✅ Transaction support
- ✅ Works with multiple SQL databases
- ✅ Large ecosystem and community

**Cons:**
- ❌ Limited to SQL databases
- ❌ ORM overhead
- ❌ Complex queries can be inefficient
- ❌ Rigid schema
- ❌ Migrations can be complex

### PyMongo (This Project)

**Pros:**
- ✅ Direct database access
- ✅ No ORM overhead
- ✅ Schema flexibility
- ✅ Full MongoDB feature access
- ✅ Better performance for some operations
- ✅ No migrations needed
- ✅ Easy to scale horizontally

**Cons:**
- ❌ No automatic admin interface
- ❌ Manual validation
- ❌ More boilerplate code
- ❌ Relationships require manual implementation
- ❌ Less type safety
- ❌ Steeper learning curve

## When to Use Each Approach

### Use Django ORM When:
- You need a SQL database
- You want automatic admin interface
- You need complex relationships
- You prefer Django's conventions
- You want built-in transaction support
- Your team is familiar with SQL

### Use PyMongo When:
- You need MongoDB's flexibility
- You want maximum performance
- You need MongoDB-specific features
- You have unstructured data
- You want to avoid migrations
- You need horizontal scaling

## Migration Path

### From Django ORM to PyMongo

1. **Remove model definitions** from `models.py`
2. **Create serializers** for validation
3. **Set up MongoDB connection** utility
4. **Rewrite views** to use PyMongo operations
5. **Update tests** to work with MongoDB
6. **Export data** from SQL to MongoDB

### From PyMongo to Django ORM

1. **Create model definitions** in `models.py`
2. **Run migrations** to create tables
3. **Update serializers** to use models
4. **Rewrite views** to use ORM operations
5. **Import data** from MongoDB to SQL
6. **Update tests** to work with ORM

## Conclusion

Both approaches have their place:

- **Django ORM** is ideal for traditional web applications with structured data and complex relationships
- **PyMongo** is perfect for applications requiring flexibility, performance, and MongoDB-specific features

This project demonstrates the **PyMongo approach**, showing how to build a fully functional REST API without Django ORM, giving you complete control over MongoDB operations while still leveraging Django REST Framework's powerful features.

## Additional Resources

- [Django ORM Documentation](https://docs.djangoproject.com/en/stable/topics/db/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)
- [MongoDB Query Language](https://docs.mongodb.com/manual/tutorial/query-documents/)
- [Django REST Framework](https://www.django-rest-framework.org/)
