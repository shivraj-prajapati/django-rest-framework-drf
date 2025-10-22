from core.database import db
from core.response import success_response, error_response
from rest_framework.decorators import api_view
from rest_framework import status 
from bson import json_util
import json

country_collection = db["countries"]

@api_view(['GET', 'POST'])
def CountryAPI(request):
    try:
        if request.method == 'GET':
            countries = list(country_collection.find({}))
            json_data = json.loads(json_util.dumps(countries))
            return success_response(message="Countries retrieved successfully", data=json_data, code=status.HTTP_200_OK)
        elif request.method == 'POST':
            data = request.data
            if not data.get('name') and data.get('code'):
                return error_response(
                    message="Both 'name' and 'code' fields are required",
                    code=status.HTTP_400_BAD_REQUEST
                )
            result = country_collection.insert_one({'name': data['name'], 'code': data['code']})
            return success_response(
                message="Country inserted successfully",
                data={"id": str(result.inserted_id)},
                code=status.HTTP_201_CREATED
            )
    except Exception as e:
        return error_response(
            message=f"Internal Server Error: {str(e)}",
            code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )