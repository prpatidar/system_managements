import stripe
import smtplib
from smtplib import SMTPException
from email.mime.text import MIMEText

from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import render , redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import ( REDIRECT_FIELD_NAME, get_user_model, login as auth_login, logout as auth_logout, update_session_auth_hash)
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics ,viewsets
from rest_framework.views import APIView

from users.models import User
from users.api.serializers import UserSerializer ,LoginSerializer ,ChangePasswordSerializer ,ForgetPasswordSerializer ,EmployeeSerializer ,EditEmployeeSerializer, ClientSerializer


# view for allmanagers in application
class AllManagersView(generics.ListAPIView):
    
    queryset = User.objects.filter(role="manager")
    serializer_class = UserSerializer

# view for all employees

class AllEmployeesView(generics.ListAPIView):
    
    queryset = User.objects.filter(role="employee")
    serializer_class = UserSerializer

# view to list all clients
class AllClientsView(generics.ListAPIView):
    
    queryset = User.objects.filter(role="client")
    serializer_class = UserSerializer

    
# view to list a particular employee by its id
class EmployeeView(generics.ListAPIView):
    
    queryset = User.objects.filter(role="employee")
    serializer_class = UserSerializer
    
    def get(self, request,employee_id):
        queryset = User.objects.filter(role="employee",id=employee_id)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

# view to list particular client by its unique id
class ClientView(generics.ListAPIView):
    
    queryset = User.objects.filter(role="client")
    serializer_class = UserSerializer
    
    def get(self, request,client_id):
        queryset = User.objects.filter(role="client",id=client_id)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

class CreateApiView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self,request):
        data=request.data
        user_serializer = UserSerializer(data=request.data,context={'request': request})
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'status': False,'message': msgs.INVALID_EMAIL_OR_PASSWORD},
                                status=status.HTTP_400_BAD_REQUEST)

class CreateEmployeeApiView(generics.CreateAPIView):
    serializer_class = EmployeeSerializer

    def post(self,request):
        data=request.data
        manager = User.objects.get(email=request.user)
        if manager.role != 'manager':
            return Response({'status': False,'message': 'you are not a Authorized manager to create Employees'},
                                status=status.HTTP_400_BAD_REQUEST) 
        # import pdb; pdb.set_trace()
        mutable = data._mutable
        data._mutable = True
        data['role'] = "employee"
        data['createdby'] = manager.id
        data._mutable = mutable
        user_serializer = EmployeeSerializer(data=data,context={'request': request})
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            print data
            print user_serializer.save().__dict__
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'status': False,'message': msgs.INVALID_EMAIL_OR_PASSWORD},
                                status=status.HTTP_400_BAD_REQUEST)

class CreateClientApiView(generics.CreateAPIView):
    serializer_class = ClientSerializer

    def post(self,request):
        data=request.data
        manager = User.objects.get(email=request.user)
        if manager.role != 'manager':
            return Response({'status': False,'message': 'you are not a Authorized manager to create clients'},
                                status=status.HTTP_400_BAD_REQUEST) 
        # import pdb; pdb.set_trace()
        stripe.api_key = "sk_test_6NXzQP1ksrl4ApeJn5TdJ9SW"
        stripetoken = stripe.Customer.create(description=data['email'])
        mutable = data._mutable
        data._mutable = True
        data['role'] = "client"
        data['createdby'] = manager.id
        data['stripetoken'] = stripetoken['id']
        data._mutable = mutable
        user_serializer = ClientSerializer(data=data,context={'request': request})
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            print data
            print user_serializer.save().__dict__
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'status': False,'message': msgs.INVALID_EMAIL_OR_PASSWORD},
                                status=status.HTTP_400_BAD_REQUEST)

class EditClientsApiView(generics.ListAPIView):
    
    queryset = User.objects.filter(role='client')
    serializer_class = EmployeeSerializer

    def get(self, request):
        manager = User.objects.get(email=request.user.email)
        queryset = User.objects.filter(createdby=manager.id,role='client')
        serializer = EmployeeSerializer(queryset, many=True)
        return Response(serializer.data)

class EditClientApiView(generics.CreateAPIView):
    
    queryset = User.objects.filter(role='client')
    serializer_class = EditEmployeeSerializer

    def get(self, request, client_id):
        manager = User.objects.get(email=request.user.email)
        queryset = User.objects.filter(createdby=manager.id,role='client',id=client_id)
        serializer = EditEmployeeSerializer(queryset, many=True)
        return Response(serializer.data)
   
    def put(self,request, client_id):
        data=request.data
        # import pdb; pdb.set_trace()
        try:
            manager = User.objects.get(email=request.user)
            if manager.role != "manager" :
                return Response({'status': False, 'message': 'yoy are not Authorized Manager to Update client'}, status=status.HTTP_404_NOT_FOUND)
            user = User.objects.get(id=client_id)
            if data['username']:
                user.username = data['username']
            if data['first_name']:
                user.first_name = data['first_name']
            if data['last_name']:
                user.last_name = data['last_name']
            if data['password']:
                user.password = data['password']
            user.save()
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print e
            return Response({'status': False, 'message': 'Can Not Update client'}, status=status.HTTP_404_NOT_FOUND)



class EditEmployeesApiView(generics.ListAPIView):
    
    queryset = User.objects.filter(role='employee')
    serializer_class = EmployeeSerializer

    def get(self, request):
        manager = User.objects.get(email=request.user.email)
        queryset = User.objects.filter(createdby=manager.id,role='employee')
        serializer = EmployeeSerializer(queryset, many=True)
        return Response(serializer.data)

class EditEmployeeApiView(generics.CreateAPIView):
    
    queryset = User.objects.filter(role='employee')
    serializer_class = EditEmployeeSerializer

    def get(self, request, employee_id):
        manager = User.objects.get(email=request.user.email)
        queryset = User.objects.filter(createdby=manager.id,role='employee',id=employee_id)
        serializer = EditEmployeeSerializer(queryset, many=True)
        return Response(serializer.data)
   
    def put(self,request, employee_id):
        data=request.data
        # import pdb; pdb.set_trace()
        try:
            manager = User.objects.get(email=request.user)
            if manager.role != "manager" :
                return Response({'status': False, 'message': 'yoy are not Authorized Manager to Update Employee'}, status=status.HTTP_404_NOT_FOUND)
            user = User.objects.get(id=employee_id)
            if data['username']:
                user.username = data['username']
            if data['first_name']:
                user.first_name = data['first_name']
            if data['last_name']:
                user.last_name = data['last_name']
            if data['password']:
                user.password = data['password']
            user.save()
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print e
            return Response({'status': False, 'message': 'Can Not Update Employee'}, status=status.HTTP_404_NOT_FOUND)


class LoginApiView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self,request):
        email=request.data.get('email')
        password =request.data.get('password')
        print email,password
        try :
            user = User.objects.get(email=email)
            if user :
                auth_login(request, user)
                return Response({
                    'status': True,
                    'message': 'Succesfully Login to Api'
                }, status=status.HTTP_200_OK)  
            else:
                return Response({
                    'status': False,
                    'message':"Inavlid Email And Password"
                }, status=status.HTTP_400_BAD_REQUEST)
        except (AttributeError, ObjectDoesNotExist):
            return Response({'status': False,
                             'message': "No Such User Found"},
                            status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.CreateAPIView):
    serializer_class = ChangePasswordSerializer

    def post(self,request):
        current_password=request.data.get('current_password')
        new_password =request.data.get('new_password')
        try :
            print request.user,current_password,new_password
            user = User.objects.get(email=request.user,password=current_password)
            if user :
                print user.email,user.password
                user.password = new_password
                user.save()
                return Response({
                    'status': True,
                    'message': 'Password Succesfully changed '
                }, status=status.HTTP_200_OK)  
            else:
                return Response({
                    'status': False,
                    'message':"Inavlid Email And Password"
                }, status=status.HTTP_400_BAD_REQUEST)
        except (AttributeError, ObjectDoesNotExist):
            return Response({'status': False,
                             'message': "First Login to Change your Password"},
                            status=status.HTTP_400_BAD_REQUEST)

class ForgetPasswordView(generics.CreateAPIView):
    serializer_class = ForgetPasswordSerializer

    def post(self,request):
        email=request.data.get('email')
        try :
            print request.user,email
            user = User.objects.get(email=email)
            if user :
                print user.email,user.password
                try:
                    msg ='Your Password for System Managements Account '+email+' is '+ user.password + '<a href="http://127.0.0.1:8000/api/user/changepassword/">Click here</a> '
                    session = smtplib.SMTP('smtp.gmail.com',587)
                    session.ehlo()
                    session.starttls()
                    session.ehlo()
                    session.login('pradeeppatidar2018@gmail.com','ppatidar2018')
                    session.sendmail('pradeeppatidar2018@gmail.com', email, msg )         
                    session.quit()
                    user.save()
                    print "Successfully sent email"
                except SMTPException:
                    print "Error: unable to send email"
                return Response({
                    'status': True,
                    'message': 'Password Succesfully Send to Your Email '
                }, status=status.HTTP_200_OK)  
            else:
                return Response({
                    'status': False,
                    'message':"Inavlid Email"
                }, status=status.HTTP_400_BAD_REQUEST)
        except (AttributeError, ObjectDoesNotExist):
            return Response({'status': False,
                             'message': "No Such User Found"},
                            status=status.HTTP_400_BAD_REQUEST)



class LogoutApiView(APIView):

    def get(self,request):
        print self.request.user
        auth_logout(request)
        return Response({'message': "Succesfully Logout "},
                            status=status.HTTP_200_OK)


class DeleteEmployeesApiView(generics.ListAPIView):
    
    queryset = User.objects.filter(role='employee')
    serializer_class = EditEmployeeSerializer

    def get(self, request):
        manager = User.objects.get(email=request.user.email)
        queryset = User.objects.filter(createdby=manager.id,role='employee')
        serializer = EmployeeSerializer(queryset, many=True)
        return Response(serializer.data)


class DeleteEmployeeApiView(generics.ListAPIView):
    
    def get(self, request,employee_id):
        manager = User.objects.get(email=request.user.email)
        if manager.role != "manager" :
            return Response({'status': False, 'message': 'yoy are not Authorized Manager to Update Employee'}, status=status.HTTP_404_NOT_FOUND)
        user = User.objects.filter(id=employee_id,role='employee',createdby=manager.id).delete()
        if user :
            return Response({'status': True, 'message': 'Employee  Deleted Successfully'}, status=status.HTTP_200_OK)
        else :
            return Response({'status': False, 'message': 'No such Employee Found '}, status=status.HTTP_404_NOT_FOUND)
        

class DeleteClientsApiView(generics.ListAPIView):
    
    queryset = User.objects.filter(role='client')
    serializer_class = ClientSerializer

    def get(self, request):
        manager = User.objects.get(email=request.user.email)
        queryset = User.objects.filter(createdby=manager.id,role='client')
        serializer = ClientSerializer(queryset, many=True)
        return Response(serializer.data)


class DeleteClientApiView(generics.ListAPIView):
    
    def get(self, request,client_id):
        manager = User.objects.get(email=request.user.email)
        if manager.role != "manager" :
            return Response({'status': False, 'message': 'yoy are not Authorized Manager to Update Employee'}, status=status.HTTP_404_NOT_FOUND)
        user = User.objects.get(id=client_id,createdby=manager.id)
        if user :
            stripe.api_key = "sk_test_6NXzQP1ksrl4ApeJn5TdJ9SW"
            cu = stripe.Customer.retrieve(user.stripetoken)
            cu.delete()
            User.objects.filter(id=client_id,role='client',createdby=manager.id).delete()        
            return Response({'status': True, 'message': 'client  Deleted Successfully'}, status=status.HTTP_200_OK)
        else :
            return Response({'status': False, 'message': 'No such client Found '}, status=status.HTTP_404_NOT_FOUND)
        

