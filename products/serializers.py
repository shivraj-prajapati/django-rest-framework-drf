"""
Serializers for Product API.
These serializers handle validation and data transformation without using Django ORM.
"""

from rest_framework import serializers


class ProductSerializer(serializers.Serializer):
    """
    Serializer for Product data.
    Does not use Django models - designed for MongoDB documents.
    """
    _id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=200, required=True)
    description = serializers.CharField(required=False, allow_blank=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    quantity = serializers.IntegerField(required=True, min_value=0)
    category = serializers.CharField(max_length=100, required=False, allow_blank=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate_price(self, value):
        """Validate that price is positive."""
        if value < 0:
            raise serializers.ValidationError("Price must be a positive value.")
        return value

    def validate_name(self, value):
        """Validate that name is not empty after stripping whitespace."""
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty.")
        return value.strip()
