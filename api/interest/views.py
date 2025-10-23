from rest_framework import status
from rest_framework.decorators import api_view
from core.database import db
from core.response import success_response, error_response
from datetime import datetime
from bson import ObjectId

interest_collection = db['interest']

def serialize_interest(interest):
    """Convert MongoDB interest document to dict with string _id."""
    interest = dict(interest)
    interest['_id'] = str(interest['_id'])
    return interest

@api_view(['GET', 'POST'])
def InterestAPI(request):
    if request.method == 'GET':
        try:
            interests = list(interest_collection.find({}))
            interests = [serialize_interest(i) for i in interests]
            return success_response(
                message="Interests retrieved successfully",
                data=interests,
                code=status.HTTP_200_OK
            )
        except Exception as e:
            return error_response(
                message=f"Failed to retrieve interests: {str(e)}",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    elif request.method == 'POST':
        data = request.data
        name = data.get('name')

        if not name:
            return error_response(
                message="Field 'name' is required",
                code=status.HTTP_400_BAD_REQUEST
            )

        try:
            now = datetime.now()
            doc = {'name': name, 'createdAt': now, 'updatedAt': now}
            result = interest_collection.insert_one(doc)
            interest = interest_collection.find_one({'_id': result.inserted_id})
            interest = serialize_interest(interest)
            return success_response(
                message="Interest inserted successfully",
                data=interest,
                code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return error_response(
                message=f"Failed to insert interest: {str(e)}",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['GET', 'PATCH', 'DELETE'])
def InterestDetailAPI(request, id):
    try:
        obj_id = ObjectId(id)
    except Exception:
        return error_response(
            message="Invalid interest id",
            code=status.HTTP_400_BAD_REQUEST
        )

    if request.method == 'GET':
        interest = interest_collection.find_one({'_id': obj_id})
        if not interest:
            return error_response(
                message="Interest not found",
                code=status.HTTP_404_NOT_FOUND
            )
        interest = serialize_interest(interest)
        return success_response(
            message="Interest retrieved successfully",
            data=interest,
            code=status.HTTP_200_OK
        )

    elif request.method == 'PATCH':
        data = request.data
        update_data = {}
        if 'name' in data:
            update_data['name'] = data['name']
        if not update_data:
            return error_response(
                message="No valid fields to update",
                code=status.HTTP_400_BAD_REQUEST
            )
        update_data['updatedAt'] = datetime.now()
        
        result = interest_collection.update_one({'_id': obj_id}, {'$set': update_data})
        if result.matched_count == 0:
            return error_response(
                message="Interest not found",
                code=status.HTTP_404_NOT_FOUND
            )
        interest = interest_collection.find_one({'_id': obj_id})
        interest = serialize_interest(interest)
        return success_response(
            message="Interest updated successfully",
            data=interest,
            code=status.HTTP_200_OK
        )

    elif request.method == 'DELETE':
        result = interest_collection.delete_one({'_id': obj_id})
        if result.deleted_count == 0:
            return error_response(
                message="Interest not found",
                code=status.HTTP_404_NOT_FOUND
            )
        return success_response(
            message="Interest deleted successfully",
            data={"_id": id},
            code=status.HTTP_200_OK
        )
