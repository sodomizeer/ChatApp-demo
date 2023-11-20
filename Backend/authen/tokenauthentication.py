import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from django.conf import settings
from django.contrib.auth import get_user_model

from datetime import datetime, timedelta 

#will use the conf>settings>Secret Key to encrypt our token

##This will secure the login API


User = get_user_model()

class JWTAuthentication(BaseAuthentication):
    """
    JWT Authentication for securing the login API.

    This authentication class verifies the user's identity using a JWT (JSON Web Token).
    """
    
    #Authenticates user by userID
    def authenticate(self, request):
        
        """
        Authenticate the user using the provided JWT token.

        param request:                  The HTTP request.
        type request:                   rest_framework.request.Request
        return:                         Tuple (user, token) if authentication is successful, None otherwise.
        return type:                    tuple or None
        raises AuthenticationFailed:    If the token is invalid or expired.
        """
        
        token = self.extract_token(request=request)
        
        if token is None:
            # print("No token found in the request.")
            return None
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])    
            self.varify_token(payload=payload)


            user_id = payload["id"]
            user = User.objects.get(id = user_id)
            return user, token

        except(InvalidTokenError, ExpiredSignatureError, User.DoesNotExist) as e:
            # print(f"Authentication failed: {e}")
            raise AuthenticationFailed("Invalid Token! ")
        
    #Varifies the validity of token
    def varify_token(self, payload):
        
        """
        Verify the validity of the token.

        param payload:                  The decoded JWT payload.
        type payload:                   dict
        raises InvalidTokenError:       If the token has no expiration.
        raises ExpiredSignatureError:   If the token has expired.
        """
        
        if "exp" not in payload:
            raise InvalidTokenError("Token has no Expiration! ")

        exp_timestamp = payload["exp"]
        current_timestamp = datetime.utcnow().timestamp()
        
        if current_timestamp > exp_timestamp:
            raise ExpiredSignatureError("Token has Expired! ")
    
    #Decrypts the token
    def extract_token(self, request):
        
        """
        Extracts the JWT token from the request.

        param request:      The HTTP request.
        type request:       rest_framework.request.Request
        return:             The JWT token if found, None otherwise.
        return type:        str or None
        """
        all_headers = request.headers
        # print(f"All Headers: {all_headers}")
        
        #we are getting the authorization header first, This will be a string
        auth_header = request.headers.get("Authorization")
        # print("hello", auth_header)
        # Then it sill split the header and take the second part of the splitted String
        
        if auth_header and auth_header.startswith("Bearer "):
        
            #Example : "Bearer klasmdkmzxc23i413kj135n130iasfcj"
            # ["Bearer", "klasmdkmzxc23i413kj135n130iasfcj"]
            # token = auth_header.split(" ")[1]
            # print(f"Extracted Token: {token}")
            
            return auth_header.split(" ")[1]
        
        # print("No token found in the Authorization header.")
        return None
    
    
    @staticmethod       #doesn't modify the state of the instance or have access to them
    def generate_token(payload):
        
        """
        Generates a new JWT token.

        param payload:  The data to be encrypted in the token.
        type payload:   dict
        return:         The generated JWT token.
        return type:    str
        """
        
        #Payload will be all the data that we want to encrypt
        expiration = datetime.utcnow() + timedelta(hours=24)
        payload["exp"] = expiration
        token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm="HS256")
        # print("token:  ", token)
        return token