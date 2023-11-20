from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate



#This Serializer is used to convert the python data types to Json and Send back to the React FrontEnd


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for converting Python User model instances to JSON and vice versa.

    This serializer is used for creating and updating user instances.
    """
    
    password = serializers.CharField(write_only = True)    
    
    def create(self, validated_data):
        """
        Creates and retursn a new user instance.

        param validated_data:  Validated data containing user information.
        type validated_data:   dict
        return: Created user   instance.
        return type:           User
        """
        user = get_user_model().objects.create_user(
            email = validated_data['email'],
            password = validated_data['password'],
            
            #returns an empty string if firstname not found
            first_name = validated_data.get("first_name",""),
            last_name = validated_data.get("last_name", "")
        )
        return user
    
    class Meta:
        model = get_user_model()
        fields = ["id","email","password", "first_name", "last_name"]
        extra_kwargs = {'password': {'write_only' : True}}
        
        
class LoginSerializer(serializers.Serializer):
    
    """
    Serializer for user login.

    This serializer is used for validating user login credentials.
    """
    
    email = serializers.EmailField()
    id = serializers.CharField(max_length=15, read_only=True) 
    password = serializers.CharField(max_length=255,write_only=True)
    first_name = serializers.CharField(max_length=64, read_only=True)
    last_name = serializers.CharField(max_length=64, read_only=True)
    
    
    def validate(self, data):
        
        """
        Validate user login credentials.

        param data:                         Input data containing email and password.
        type data:                          dict
        return:                             Validated user data.
        return type:                        dict
        raises serializers.ValidationError: If email or password is missing, or if authentication fails.
        """
        
        email = data.get("email", None)
        print(email)
        password = data.get("password", None)
        
        
        
        if email is None:
            raise serializers.ValidationError("An Email Address is required!! ")
        
        if password is None:
            raise serializers.ValidationError("A password is required!! ")
        
        print(f"UserModel:  {get_user_model()}")
        
        
        user = authenticate(email=email, password=password)

        print(f"\n {user} \n")

        if user is None:
            raise serializers.ValidationError("Invalid Email or Password!! user is NONE")
        
        if not user.is_active:
            raise serializers.ValidationError("User is inactive")
        
        return {
            "email" : user.email,
            "id" : user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            
        }
