"""
Example demonstrating how to work with the MongoDB client directly.
This script shows how to perform various MongoDB operations using PyMongo.

Note: This requires a running MongoDB instance.
"""

from products.mongo_client import mongo_client
from datetime import datetime
from bson import ObjectId


def example_basic_operations():
    """Demonstrate basic MongoDB operations."""
    
    print("=" * 60)
    print("MongoDB Direct Operations Example")
    print("=" * 60)
    
    # Get the products collection
    collection = mongo_client.get_collection('products')
    
    # 1. Insert a document
    print("\n1. Inserting a product...")
    product = {
        "name": "Mechanical Keyboard",
        "description": "RGB mechanical keyboard with blue switches",
        "price": 89.99,
        "quantity": 150,
        "category": "Accessories",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    result = collection.insert_one(product)
    print(f"   Inserted product with ID: {result.inserted_id}")
    
    # 2. Find documents
    print("\n2. Finding products...")
    products = collection.find({"category": "Accessories"})
    print(f"   Found {collection.count_documents({'category': 'Accessories'})} accessories:")
    for prod in products:
        print(f"   - {prod['name']}: ${prod['price']}")
    
    # 3. Find one document
    print("\n3. Finding one product by ID...")
    found_product = collection.find_one({"_id": result.inserted_id})
    if found_product:
        print(f"   Found: {found_product['name']}")
    
    # 4. Update a document
    print("\n4. Updating product price...")
    collection.update_one(
        {"_id": result.inserted_id},
        {"$set": {"price": 79.99, "updated_at": datetime.utcnow()}}
    )
    updated_product = collection.find_one({"_id": result.inserted_id})
    print(f"   Updated price to: ${updated_product['price']}")
    
    # 5. Find with filters
    print("\n5. Finding products with price < $100...")
    cheap_products = collection.find({"price": {"$lt": 100}})
    for prod in cheap_products:
        print(f"   - {prod['name']}: ${prod['price']}")
    
    # 6. Count documents
    print("\n6. Counting all products...")
    total_count = collection.count_documents({})
    print(f"   Total products in database: {total_count}")
    
    # 7. Delete a document
    print("\n7. Deleting the test product...")
    delete_result = collection.delete_one({"_id": result.inserted_id})
    print(f"   Deleted {delete_result.deleted_count} document(s)")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


def example_advanced_queries():
    """Demonstrate advanced MongoDB queries."""
    
    print("\n" + "=" * 60)
    print("Advanced MongoDB Queries")
    print("=" * 60)
    
    collection = mongo_client.get_collection('products')
    
    # Insert sample data
    print("\n1. Inserting sample products...")
    sample_products = [
        {"name": "Mouse", "price": 25.99, "quantity": 200, "category": "Accessories"},
        {"name": "Monitor", "price": 299.99, "quantity": 50, "category": "Electronics"},
        {"name": "Webcam", "price": 59.99, "quantity": 75, "category": "Electronics"},
        {"name": "Headphones", "price": 79.99, "quantity": 100, "category": "Audio"},
    ]
    
    result = collection.insert_many(sample_products)
    print(f"   Inserted {len(result.inserted_ids)} products")
    
    # Query with multiple conditions
    print("\n2. Finding Electronics with price < $200...")
    electronics = collection.find({
        "category": "Electronics",
        "price": {"$lt": 200}
    })
    for prod in electronics:
        print(f"   - {prod['name']}: ${prod['price']}")
    
    # Sorting
    print("\n3. Finding products sorted by price (descending)...")
    sorted_products = collection.find().sort("price", -1).limit(3)
    for prod in sorted_products:
        print(f"   - {prod['name']}: ${prod['price']}")
    
    # Aggregation
    print("\n4. Aggregating: Average price by category...")
    pipeline = [
        {
            "$group": {
                "_id": "$category",
                "avg_price": {"$avg": "$price"},
                "total_quantity": {"$sum": "$quantity"}
            }
        }
    ]
    results = collection.aggregate(pipeline)
    for result in results:
        print(f"   - {result['_id']}: Avg ${result['avg_price']:.2f}, Total Qty: {result['total_quantity']}")
    
    # Cleanup
    print("\n5. Cleaning up sample data...")
    collection.delete_many({"_id": {"$in": result.inserted_ids}})
    print("   Sample data removed")
    
    print("\n" + "=" * 60)


def example_error_handling():
    """Demonstrate error handling with MongoDB operations."""
    
    print("\n" + "=" * 60)
    print("Error Handling Examples")
    print("=" * 60)
    
    collection = mongo_client.get_collection('products')
    
    # 1. Handling invalid ObjectId
    print("\n1. Attempting to find with invalid ObjectId...")
    try:
        invalid_id = "invalid_id"
        product = collection.find_one({"_id": ObjectId(invalid_id)})
    except Exception as e:
        print(f"   Error caught: {type(e).__name__}")
    
    # 2. Handling non-existent document
    print("\n2. Attempting to find non-existent document...")
    fake_id = ObjectId()
    product = collection.find_one({"_id": fake_id})
    if product is None:
        print(f"   No product found with ID: {fake_id}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    try:
        # Run basic operations
        example_basic_operations()
        
        # Run advanced queries
        example_advanced_queries()
        
        # Run error handling examples
        example_error_handling()
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nMake sure:")
        print("1. MongoDB is running")
        print("2. Connection settings in settings.py are correct")
        print("3. You've set up the Django project correctly")
