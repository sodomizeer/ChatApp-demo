from django.shortcuts import render



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from authen.tokenauthentication import JWTAuthentication
from .serializers import UserSerializer, LoginSerializer
# Create your views here.

#THis function only POST and doesnt GET
@api_view(["POST"])
def register_user(request):
    
    """
    View for user registration.

    This view handles the registration of a new user by processing a POST request.

    param request:      The HTTP request.
    type request:       rest_framework.request.Request
    return:             HTTP response containing user data or errors.
    return type:        rest_framework.response.Response
    """
    
    serializer = UserSerializer(data = request.data)
    
    if serializer.is_valid():
        serializer.save()
        
        #post request succesful/successfully inserted data into database by status code 201
        return Response(serializer.data, status=201)
    
    #not a success: 400       
    return Response(serializer.errors, status=400)

@api_view(["POST"])
def login(request):
    
    """
    View for user login.

    This view handles the login of a user by processing a POST request.

    param request:      The HTTP request.
    type request:       rest_framework.request.Request
    return: HTTP        response containing a success message, token, and user data or errors.
    retuwrn type:       rest_framework.response.Response
    """
    
    serializer = LoginSerializer(data = request.data)
    
    if serializer.is_valid():
        
        #triggers the generate_token function if the serializer is valid
        token = JWTAuthentication.generate_token(payload=serializer.data)
        return Response({
            "message" : "Login Successfull",
            "token" : token,
            "user" : serializer.data
        }, status=status.HTTP_201_CREATED)
    else:
        print("Failed!!!!")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)