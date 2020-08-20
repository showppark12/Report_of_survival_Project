import jwt
import json

from account.models import Account
from mysite.settings import SECRET_KEY
from django.http import JsonResponse

class LoginConfirm:
    def __init__(self,original_function):
        self.original_function = original_function
    
    def __call__(self, request, *args, **kwargs):
        token = request.headers.get("Authorization", None)
        try:
            if token:
                token_payload = jwt.decode(token, SECRET_KEY, algorithm="HS256")
                user = Account.objects.get(id=token_payload['user'])
                request.user = user
                return self.original_function(self, request, *args, **kwargs)
            
            return JsonResponse({'message':'NEED_LOGIN'}, status=401)
        
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message':'EXPIRED_TOKEN'}, status =401)
        
        except jwt.DecodeError:
            return JsonResponse({'message':'INVALID_USER'}, status=401)

        except Account.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status = 401)
