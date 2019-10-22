from django.shortcuts import render
from rest_framework import viewsets ,status
from .models import User,Name
from .serializer import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action,permission_classes
from .token import get_tokens_for_user
import re
from bson import json_util
import json
from .backend import authenticate

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = UserSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return User.objects.all()

    def create(self, request):
        # first_name = request.data.get("name.first_name")
        # last_name = request.data.get("name.last_name")#optional
        print(request.data)
        first_name = request.data.get("name").get("first_name")
        last_name = request.data.get("name").get("last_name")#optional
        
        email = request.data.get("email")
        password = request.data.get("password")
        mobile_no = request.data.get("mobile_no")
        gender = request.data.get("gender")#optional
        print(len(mobile_no)!=10)
        if not first_name:
            return Response({"error":"Missing First Name"},status=status.HTTP_400_BAD_REQUEST)
        if not email:    
            return Response({"error":"Missing Email"},status=status.HTTP_400_BAD_REQUEST)
        if not re.search("^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$",email):
            return Response({"error":"Provide a Valid Email"},status=status.HTTP_400_BAD_REQUEST)
        if not password:    
            return Response({"error":"Missing password"},status=status.HTTP_400_BAD_REQUEST)
        if not mobile_no:    
            return Response({"error":"Missing Mobile No"},status=status.HTTP_400_BAD_REQUEST)
        if not len(mobile_no) == 10:
            return Response({"error":"Provide a Valid Mobile No"},status=status.HTTP_400_BAD_REQUEST)
        
        name=Name()
        name["first_name"]=first_name
        if last_name:
            name["last_name"]=last_name

        user = User()
        user["name"] = name 
        user["email"] = email
        user["password"] = password
        user["mobile_no"] = mobile_no

        if gender:
            user["gender"] = gender
        user.save()
        return Response({"id":json.dumps(user.id, indent=4, default=json_util.default)})

    #detail is True because this action is intended for single user object not whole collection
    @action(detail=False, methods=['POST'])
    def login(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        if not email or not password :
            return Response({'error': 'Please provide both username and password'},
                        status=status.HTTP_400_BAD_REQUEST)
        if not re.search("^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$",email):
            return Response({"error":"Provide a Valid Email"},status=status.HTTP_400_BAD_REQUEST)                
        try:
            user = User.objects.get(email=email)
            if user.email == request.data.get("email") and user.password == request.data.get("password"):
                token = get_tokens_for_user(user)
                user.token = token["access"]
                print("saving token")
                user.save()
                print("token saved")
                return Response({"access":user.token,"id":json.dumps(user.id, indent=4, default=json_util.default)}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({
                'error':"No Such User Found"
            },status=status.HTTP_404_NOT_FOUND)          


    # @action(detail=True, methods=['put'])
    # def updateName(self, request, id=None):
    #     # print(pk)
    #     user = User.objects.get(id=id)
    #     print(request.data)
    #     user.name=request.data["name"]
    #     # serializer = UserSerializer(user)
    #     # if serializer.is_valid():
    #     user.save()
    #     return Response("ok")
    #     # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # @action(detail=False,methods=['GET'])
    # def hello(self,request):
    #     print(authenticate(request))
    #     if authenticate(request):
    #         return Response("hello")
    #     return Response("Forbidden", status=status.HTTP_403_FORBIDDEN)  
        