"""
MongoDB connection utility using PyMongo.
This module provides a singleton MongoDB client for the application.
"""

from pymongo import MongoClient
from django.conf import settings


class MongoDBClient:
    """
    Singleton class to manage MongoDB connection using PyMongo.
    """
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBClient, cls).__new__(cls)
            cls._client = MongoClient(settings.MONGO_URI)
            cls._db = cls._client[settings.MONGO_DB_NAME]
        return cls._instance

    @property
    def database(self):
        """Return the database instance."""
        return self._db

    def get_collection(self, collection_name):
        """
        Get a specific collection from the database.
        
        Args:
            collection_name (str): Name of the collection
            
        Returns:
            pymongo.collection.Collection: MongoDB collection
        """
        return self._db[collection_name]

    def close(self):
        """Close the MongoDB connection."""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            MongoDBClient._instance = None


# Create a singleton instance
mongo_client = MongoDBClient()
