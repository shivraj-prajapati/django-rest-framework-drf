"""
API Views for Product management using PyMongo without Django ORM.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime
from .mongo_client import mongo_client
from .serializers import ProductSerializer


class ProductListCreateView(APIView):
    """
    API View to list all products or create a new product.
    GET: List all products
    POST: Create a new product
    """

    def get(self, request):
        """
        Retrieve all products from MongoDB.
        """
        try:
            collection = mongo_client.get_collection('products')
            products = list(collection.find())
            
            # Convert ObjectId to string for JSON serialization
            for product in products:
                product['_id'] = str(product['_id'])
            
            return Response({
                'count': len(products),
                'results': products
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': f'Failed to retrieve products: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        Create a new product in MongoDB.
        """
        serializer = ProductSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                collection = mongo_client.get_collection('products')
                
                # Prepare document with timestamps
                product_data = serializer.validated_data
                product_data['created_at'] = datetime.utcnow()
                product_data['updated_at'] = datetime.utcnow()
                
                # Insert into MongoDB
                result = collection.insert_one(product_data)
                
                # Retrieve the inserted document
                inserted_product = collection.find_one({'_id': result.inserted_id})
                inserted_product['_id'] = str(inserted_product['_id'])
                
                return Response(inserted_product, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    'error': f'Failed to create product: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    """
    API View to retrieve, update, or delete a specific product.
    GET: Retrieve a product by ID
    PUT: Update a product by ID
    DELETE: Delete a product by ID
    """

    def get(self, request, product_id):
        """
        Retrieve a single product by ID.
        """
        try:
            collection = mongo_client.get_collection('products')
            product = collection.find_one({'_id': ObjectId(product_id)})
            
            if product:
                product['_id'] = str(product['_id'])
                return Response(product, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Product not found'
                }, status=status.HTTP_404_NOT_FOUND)
        except InvalidId:
            return Response({
                'error': 'Invalid product ID format'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': f'Failed to retrieve product: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, product_id):
        """
        Update a product by ID.
        """
        serializer = ProductSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                collection = mongo_client.get_collection('products')
                
                # Check if product exists
                existing_product = collection.find_one({'_id': ObjectId(product_id)})
                if not existing_product:
                    return Response({
                        'error': 'Product not found'
                    }, status=status.HTTP_404_NOT_FOUND)
                
                # Prepare update data
                update_data = serializer.validated_data
                update_data['updated_at'] = datetime.utcnow()
                
                # Update in MongoDB
                collection.update_one(
                    {'_id': ObjectId(product_id)},
                    {'$set': update_data}
                )
                
                # Retrieve updated document
                updated_product = collection.find_one({'_id': ObjectId(product_id)})
                updated_product['_id'] = str(updated_product['_id'])
                
                return Response(updated_product, status=status.HTTP_200_OK)
            except InvalidId:
                return Response({
                    'error': 'Invalid product ID format'
                }, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({
                    'error': f'Failed to update product: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        """
        Delete a product by ID.
        """
        try:
            collection = mongo_client.get_collection('products')
            
            # Check if product exists
            existing_product = collection.find_one({'_id': ObjectId(product_id)})
            if not existing_product:
                return Response({
                    'error': 'Product not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Delete from MongoDB
            collection.delete_one({'_id': ObjectId(product_id)})
            
            return Response({
                'message': 'Product deleted successfully'
            }, status=status.HTTP_200_OK)
        except InvalidId:
            return Response({
                'error': 'Invalid product ID format'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': f'Failed to delete product: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

