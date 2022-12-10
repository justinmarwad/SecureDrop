from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import SecureDropUser
from .serializers import SecureDropUserSerializer, ListUserSerializer

class UserRegister(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # 1. List all users in the system - ONLY HERE FOR DEBUGGING PURPOSES
    def get(self, request, *args, **kwargs):
        '''List user details given unique user email'''

        users = SecureDropUser.objects.all()
        serializer = ListUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''Create the new user with the given information'''

        serializer = SecureDropUserSerializer(data={
            "name": request.data.get("name"), 
            "email": request.data.get("email"), 
            "passwd": request.data.get("passwd"),
            "pubkey": request.data.get("pubkey")
        }) 

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListSecureDropUsers(APIView):

    def post(self, request, *args, **kwargs):
        '''List user details given unique user email'''

        email = request.data.get("email")

        if email: 
            users = SecureDropUser.objects.filter(email=email)            
            
            if users: 
                serializer = ListUserSerializer(users, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"res": "The email provided could not be looked up."}, status=status.HTTP_400_BAD_REQUEST)

class LoginSecureDropUsers(APIView):

    def post(self, request, *args, **kwargs):
        '''Return true or false passed on whether the password is right for a given email.'''

        email  = request.data.get("email")
        passwd = request.data.get("passwd")

        if email: 
            user = SecureDropUser.objects.filter(email=email).first()            
            print(user)
            if user:
                if user.passwd == passwd: 
                    return Response({"login": "True"}, status=status.HTTP_200_OK)
                
        
        return Response({"login": "False"}, status=status.HTTP_400_BAD_REQUEST)