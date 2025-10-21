"""
Example script to test the Products API endpoints.
This script demonstrates how to interact with the API using Python requests library.

Note: Make sure the Django server is running before executing this script:
    python manage.py runserver

Usage:
    pip install requests
    python test_api.py
"""

import requests
import json
from decimal import Decimal

# Base URL for the API
BASE_URL = 'http://127.0.0.1:8000/api/products/'

class DecimalEncoder(json.JSONEncoder):
    """Custom JSON encoder for Decimal objects."""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


def create_product(product_data):
    """Create a new product."""
    print("\n=== Creating a new product ===")
    response = requests.post(BASE_URL, json=product_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()


def list_products():
    """List all products."""
    print("\n=== Listing all products ===")
    response = requests.get(BASE_URL)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()


def get_product(product_id):
    """Get a specific product."""
    print(f"\n=== Getting product {product_id} ===")
    response = requests.get(f"{BASE_URL}{product_id}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()


def update_product(product_id, product_data):
    """Update a product."""
    print(f"\n=== Updating product {product_id} ===")
    response = requests.put(f"{BASE_URL}{product_id}/", json=product_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()


def delete_product(product_id):
    """Delete a product."""
    print(f"\n=== Deleting product {product_id} ===")
    response = requests.delete(f"{BASE_URL}{product_id}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()


def main():
    """Main function to test all API endpoints."""
    
    print("=" * 60)
    print("Testing Django REST API with PyMongo")
    print("=" * 60)
    
    # Test data
    product1 = {
        "name": "Laptop",
        "description": "High-performance laptop for developers",
        "price": 1299.99,
        "quantity": 25,
        "category": "Electronics"
    }
    
    product2 = {
        "name": "Wireless Mouse",
        "description": "Ergonomic wireless mouse",
        "price": 29.99,
        "quantity": 100,
        "category": "Accessories"
    }
    
    try:
        # Create products
        created_product1 = create_product(product1)
        created_product2 = create_product(product2)
        
        # Get product IDs
        product1_id = created_product1.get('_id')
        product2_id = created_product2.get('_id')
        
        # List all products
        list_products()
        
        # Get specific product
        if product1_id:
            get_product(product1_id)
        
        # Update product
        if product1_id:
            updated_data = {
                "name": "Gaming Laptop",
                "description": "High-performance gaming laptop with RGB",
                "price": 1599.99,
                "quantity": 20,
                "category": "Electronics"
            }
            update_product(product1_id, updated_data)
        
        # List products after update
        list_products()
        
        # Delete a product
        if product2_id:
            delete_product(product2_id)
        
        # List products after deletion
        list_products()
        
        print("\n" + "=" * 60)
        print("All tests completed successfully!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the API server.")
        print("Make sure the Django server is running:")
        print("    python manage.py runserver")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
