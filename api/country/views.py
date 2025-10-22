from core.database import db
from core.response import success_response, error_response
from rest_framework.decorators import api_view
from rest_framework import status 
from bson import ObjectId
from datetime import datetime

country_collection = db["countries"]

def serialize_country(country):
    """Convert MongoDB country document to dict with string _id."""
    country = dict(country)
    country['_id'] = str(country['_id'])
    return country

@api_view(['GET', 'POST'])
def CountryAPI(request):
    if request.method == 'GET':
        try:
            countries = list(country_collection.find({}))
            countries = [serialize_country(c) for c in countries]
            return success_response(
                message="Countries retrieved successfully",
                data=countries,
                code=status.HTTP_200_OK
            )
        except Exception as e:
            return error_response(
                message=f"Failed to retrieve countries: {str(e)}",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    elif request.method == 'POST':
        data = request.data
        name = data.get('name')
        code_ = data.get('code')

        if not name or not code_:
            return error_response(
                message="Both 'name' and 'code' fields are required",
                code=status.HTTP_400_BAD_REQUEST
            )

        try:
            now = datetime.now()            
            doc = {'name': name, 'code': code_, 'createdAt': now, 'updatedAt': now}
            result = country_collection.insert_one(doc)

            country = country_collection.find_one({'_id': result.inserted_id})
            country = serialize_country(country)

            return success_response(
                message="Country inserted successfully",
                data=country,
                code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return error_response(
                message=f"Failed to insert country: {str(e)}",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['GET', 'PATCH', 'DELETE'])
def CountryDetailAPI(request, id):
    try:
        obj_id = ObjectId(id)
    except Exception:
        return error_response(
            message="Invalid country id",
            code=status.HTTP_400_BAD_REQUEST
        )

    if request.method == 'GET':
        country = country_collection.find_one({'_id': obj_id})
        if not country:
            return error_response(
                message="Country not found",
                code=status.HTTP_404_NOT_FOUND
            )
        country = serialize_country(country)
        return success_response(
            message="Country retrieved successfully",
            data=country,
            code=status.HTTP_200_OK
        )

    elif request.method == 'PATCH':
        data = request.data
        update_data = {}
        if 'name' in data:
            update_data['name'] = data['name']
        if 'code' in data:
            update_data['code'] = data['code']
        if not update_data:
            return error_response(
                message="No valid fields to update",
                code=status.HTTP_400_BAD_REQUEST
            )
        update_data['updatedAt'] = datetime.now()
        
        result = country_collection.update_one({'_id': obj_id}, {'$set': update_data})
        if result.matched_count == 0:
            return error_response(
                message="Country not found",
                code=status.HTTP_404_NOT_FOUND
            )
        country = country_collection.find_one({'_id': obj_id})
        country = serialize_country(country)
        return success_response(
            message="Country updated successfully",
            data=country,
            code=status.HTTP_200_OK
        )

    elif request.method == 'DELETE':
        result = country_collection.delete_one({'_id': obj_id})
        if result.deleted_count == 0:
            return error_response(
                message="Country not found",
                code=status.HTTP_404_NOT_FOUND
            )
        return success_response(
            message="Country deleted successfully",
            data={"_id": id},
            code=status.HTTP_200_OK
        )