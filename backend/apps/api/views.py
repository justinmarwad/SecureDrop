from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import SecureDropUser
from .serializers import SecureDropUserSerializer

class UserRegister(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''List user details given unique user email'''

        users = SecureDropUser.objects.all()
        serializer = SecureDropUserSerializer(users, many=True)
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

    # def get(self, request, *args, **kwargs):
    #     '''List user details given unique user email'''

    #     email = self.request.query_params.get("email")
    #     print("email: ", email)

    #     if email: 
    #         users = SecureDropUser.objects.filter(email=email)            
            
    #         if users: 
    #             serializer = SecureDropUserSerializer(users, many=True)
    #             return Response(serializer.data, status=status.HTTP_200_OK)
        
    #     return Response({"res": "The email provided could not be looked up."}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        '''List user details given unique user email'''

        email = request.data.get("email")

        if email: 
            users = SecureDropUser.objects.filter(email=email)            
            
            if users: 
                serializer = SecureDropUserSerializer(users, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"res": "The email provided could not be looked up."}, status=status.HTTP_400_BAD_REQUEST)