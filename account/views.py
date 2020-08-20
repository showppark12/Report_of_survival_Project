import json
import bcrypt
import jwt

from .models import Account
from .token import account_activation_token
from .text import message
from mysite.my_settings import EMAIL
from mysite.settings import SECRET_KEY

from django.views import View
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

class AccountView(View):
    def get(self, request):
        Account_data = Account.objects.values()
        return JsonResponse({'accounts': list(Account_data)}, status=200)

class SignView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if Account.objects.filter(name= data['name']).exist():
                user = Account.objects.get(name =data['name'])

                if user.password == data['password']:
                    return HttpResponse(status =200)
                return HttpResponse(status=401)
            return HttpResponse(status=400)
        
        except KeyError:
            return JsonResponse({'message': "INVALID_KEYS"}, status =400)

class SignUp(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if Account.objects.filter(email = data['email']).exists():
                return JsonResponse({"message" : "EXISTS_EMAIL"}, status =400)

            Account.objects.create(
                email = data['email'],
                name = data['name'],
                password = bcrypt.hashpw(data["password"].encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8")
            ).save()

            return HttpResponse(status=200)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)

### 이 아래로 쓰는 뷰

class SignIn(View):
    def post(self,request):
        data = json.loads(request.body)

        try:
            if Account.objects.filter(email=data["email"]).exists():
                user = Account.objects.get(email=data["email"])

                if bcrypt.checkpw(data['password'].encode('UTF-8'), user.password.encode('UTF-8')):
                    print("int가오는게 맞지않나",data['password'],"이건뭔데",user.password)
                    token = jwt.encode({'user':user.id}, SECRET_KEY, algorithm = 'HS256').decode('UTF-8')
                    return JsonResponse({"token":token},status=200)
                return HttpResponse(status=401)
            return HttpResponse(status=400)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            validate_email(data["email"])
            


            if Account.objects.filter(email=data["email"]).exists():
                return JsonResponse({"message": "EXIST_EMAIL"}, status =400)

            user = Account.objects.create(
                email = data['email'],
                name = data['name'],
                password = bcrypt.hashpw(data["password"].encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8"),
                is_active = False
            )

            current_site = get_current_site(request)
            domain = current_site.domain
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            message_data = message(domain, uidb64, token)

            mail_title = "멋사 생존신고 회원가입 이메일 인증을 완료해주세요"
            mail_to = data['email']
            email = EmailMessage(mail_title, message_data, to =[mail_to])
            email.send()

            return JsonResponse({"message": "SUCCESS"}, status = 200)

        except KeyError:
            return JsonResponse({"message" : "INVALID_KEY"}, status = 400)
        except TypeError:
            return JsonResponse({"message" : "INVALID_TYPE"}, status = 400)
        except ValidationError:
            return JsonResponse({"message" : "VALIDATION_ERROR"}, status= 400)

class Activate(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=uid)

            if account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()
                
                return redirect(EMAIL['REDIRECT_PAGE'])
            return JsonResponse({"message" : "AUTH FAIL"}, status= 400)
        
        except ValidationError:
            return JsonResponse({"message": "TYPE_ERROR"}, status= 400)
        except KeyError:
            return JsonResponse({"message": "INVALID_KEY"}, status = 400)

