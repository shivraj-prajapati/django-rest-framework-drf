"""
Unit tests for Products API using PyMongo.

Note: These tests require a running MongoDB instance.
For testing without MongoDB, consider using mongomock.
"""

from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import datetime
from bson import ObjectId
from products.mongo_client import mongo_client


class ProductAPITestCase(APITestCase):
    """Test case for Product API endpoints."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = APIClient()
        self.collection = mongo_client.get_collection('products_test')
        
        # Clear test collection
        self.collection.delete_many({})
        
        # Sample product data
        self.valid_product_data = {
            'name': 'Test Laptop',
            'description': 'A test laptop',
            'price': 999.99,
            'quantity': 10,
            'category': 'Electronics'
        }
        
        self.invalid_product_data = {
            'name': '',  # Empty name should fail validation
            'price': -10,  # Negative price should fail validation
            'quantity': -5  # Negative quantity should fail validation
        }
    
    def tearDown(self):
        """Clean up after tests."""
        # Clear test collection
        self.collection.delete_many({})
    
    def test_create_product_valid_data(self):
        """Test creating a product with valid data."""
        response = self.client.post('/api/products/', self.valid_product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('_id', response.data)
        self.assertEqual(response.data['name'], self.valid_product_data['name'])
    
    def test_create_product_invalid_data(self):
        """Test creating a product with invalid data."""
        response = self.client.post('/api/products/', self.invalid_product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_list_products(self):
        """Test listing all products."""
        # Create test products in test collection
        self.collection.insert_many([
            {
                'name': 'Product 1',
                'price': 10.99,
                'quantity': 5,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'name': 'Product 2',
                'price': 20.99,
                'quantity': 10,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
        ])
        
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_get_product_valid_id(self):
        """Test retrieving a product with valid ID."""
        # Insert a test product
        result = self.collection.insert_one({
            'name': 'Test Product',
            'price': 50.00,
            'quantity': 15,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        })
        
        product_id = str(result.inserted_id)
        response = self.client.get(f'/api/products/{product_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Product')
    
    def test_get_product_invalid_id(self):
        """Test retrieving a product with invalid ID."""
        response = self.client.get('/api/products/invalid_id/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_product_nonexistent_id(self):
        """Test retrieving a product that doesn't exist."""
        fake_id = str(ObjectId())
        response = self.client.get(f'/api/products/{fake_id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_product_valid_data(self):
        """Test updating a product with valid data."""
        # Insert a test product
        result = self.collection.insert_one({
            'name': 'Old Name',
            'price': 50.00,
            'quantity': 15,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        })
        
        product_id = str(result.inserted_id)
        updated_data = {
            'name': 'New Name',
            'price': 60.00,
            'quantity': 20
        }
        
        response = self.client.put(f'/api/products/{product_id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'New Name')
        self.assertEqual(float(response.data['price']), 60.00)
    
    def test_update_product_invalid_id(self):
        """Test updating a product with invalid ID."""
        response = self.client.put('/api/products/invalid_id/', self.valid_product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_product_nonexistent_id(self):
        """Test updating a product that doesn't exist."""
        fake_id = str(ObjectId())
        response = self.client.put(f'/api/products/{fake_id}/', self.valid_product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_product_valid_id(self):
        """Test deleting a product with valid ID."""
        # Insert a test product
        result = self.collection.insert_one({
            'name': 'To Delete',
            'price': 30.00,
            'quantity': 5,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        })
        
        product_id = str(result.inserted_id)
        response = self.client.delete(f'/api/products/{product_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        
        # Verify product is deleted
        deleted_product = self.collection.find_one({'_id': result.inserted_id})
        self.assertIsNone(deleted_product)
    
    def test_delete_product_invalid_id(self):
        """Test deleting a product with invalid ID."""
        response = self.client.delete('/api/products/invalid_id/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_delete_product_nonexistent_id(self):
        """Test deleting a product that doesn't exist."""
        fake_id = str(ObjectId())
        response = self.client.delete(f'/api/products/{fake_id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ProductSerializerTestCase(TestCase):
    """Test case for Product serializer."""
    
    def test_serializer_valid_data(self):
        """Test serializer with valid data."""
        from products.serializers import ProductSerializer
        
        data = {
            'name': 'Test Product',
            'description': 'Test description',
            'price': 99.99,
            'quantity': 10,
            'category': 'Test'
        }
        
        serializer = ProductSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_serializer_invalid_name(self):
        """Test serializer with invalid name."""
        from products.serializers import ProductSerializer
        
        data = {
            'name': '',  # Empty name
            'price': 99.99,
            'quantity': 10
        }
        
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
    
    def test_serializer_invalid_price(self):
        """Test serializer with invalid price."""
        from products.serializers import ProductSerializer
        
        data = {
            'name': 'Test Product',
            'price': -10,  # Negative price
            'quantity': 10
        }
        
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)
    
    def test_serializer_invalid_quantity(self):
        """Test serializer with invalid quantity."""
        from products.serializers import ProductSerializer
        
        data = {
            'name': 'Test Product',
            'price': 99.99,
            'quantity': -5  # Negative quantity
        }
        
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('quantity', serializer.errors)

