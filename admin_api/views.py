from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework import status

class AdminLoginView(APIView):
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.check_admin(serializer.validated_data)
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Serialize admin details
        admin_serializer = AdminSerializer(user)

        return Response({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'admin': admin_serializer.data
        })
        
        
# class UserLogin(APIView):
#     def post(self, request):
#         data = request.data
#         serializer = UserLoginSerializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         user = authenticate(
#             request,
#             email=serializer.validated_data['email'],
#             password=serializer.validated_data['password']
#         )
#         if user is None:
#             raise AuthenticationFailed('Invalid email or password.')

#         # User authentication successful
#         login(request, user)
#         access_token = AccessToken.for_user(user)
#         access_token['email'] = user.email
#         access_token['is_active'] = user.is_active
#         access_token['is_superuser'] = user.is_superuser
#         access_token['is_res_admin'] = user.is_res_admin

#         access_token = str(access_token)
#         refresh_token = str(RefreshToken.for_user(user))
#         return Response({
#             "access_token": access_token,
#             "refresh_token": refresh_token,
#             "email": user.email
#         })            
        

    
class city(APIView):
    def get(self, request, *args, **kwargs):
         city_objs=City.objects.all()
         serializer=CitySerializer(city_objs,many=True)
         return Response(serializer.data)         


@api_view(['POST'])
def CityAdd(request):
    data=request.data
    print('dataaaaaa',data)
    serializer=CitySerializer(data=data)
    if not serializer.is_valid():
        print(serializer.errors)
        return Response({'status':403,'errors':serializer.errors,'message':'something wrong'})
    serializer.save()
    return Response({'status':200,'payload':serializer.data,'message':'data saved'})

@api_view(['PUT'])
def update_city(request,id):
    try:
        city_obj=City.objects.get(id=id)
        serializer=CitySerializer(city_obj,data=request.data,partial=True)
        if not serializer.is_valid():
          print(serializer.errors)
          return Response({'status':403,'errors':serializer.errors,'message':'something wrong'})
        serializer.save()
        return Response({'status':200,'payload':serializer.data,'message':'data saved'})

    except Exception as e:
       return Response({'status':403,'message':'invalid id'})   
   
@api_view(['GET'])
def get_city(request, id):
    try:
        city_obj = City.objects.get(id=id)
        serializer = CitySerializer(city_obj)
        return Response({'status': 200, 'payload': serializer.data, 'message': 'City details retrieved'})

    except City.DoesNotExist:
        return Response({'status': 404, 'message': 'City not found'})

    except Exception as e:
        return Response({'status': 500, 'message': 'Internal server error'})         

@api_view(['DELETE'])
def delete_city(request,id):
    try:
        city_obj=City.objects.get(id=id)  
        city_obj.delete()
        return Response({'status':200,'message':'deleted'})

    except Exception as e:
       return Response({'status':403,'message':'invalid id'})    
   
   
class cuisines(APIView):
    def get(self, request, *args, **kwargs):
         cuisine_objs=CuisineType.objects.all()
         serializer=CuisineSerializer(cuisine_objs,many=True)
         return Response(serializer.data)         


@api_view(['POST'])
def cuisineAdd(request):
    data=request.data
    print('dataaaaaa',data)
    serializer=CuisineSerializer(data=data)
    if not serializer.is_valid():
        print(serializer.errors)
        return Response({'status':403,'errors':serializer.errors,'message':'something wrong'})
    serializer.save()
    return Response({'status':200,'payload':serializer.data,'message':'data saved'})
       
       
class TimeSlotList(APIView):
    def get(self, request):
        timeslots = Times.objects.all()
        serializer = TimeSlotSerializer(timeslots, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TimeSlotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

       
# class TimeSlotEditDelete(APIView):
#     def get(self, request, pk):
#         timeslot = TimeSlot.objects.get(pk=pk)
#         serializer = TimeSlotSerializer(timeslot)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         timeslot = TimeSlot.objects.get(pk=pk)
#         serializer = TimeSlotSerializer(timeslot, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         timeslot = TimeSlot.objects.get(pk=pk)
#         timeslot.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)   
    
    
class TableListAdd(APIView):
    def get(self, request):
        tables = Table.objects.all()
        serializer = TableSerializer(tables, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TableEditDelete(APIView):
    def get(self, request, pk):
        table = Table.objects.get(pk=pk)
        serializer = TableSerializer(table)
        return Response(serializer.data)

    def put(self, request, pk):
        table = Table.objects.get(pk=pk)
        serializer = TableSerializer(table, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        table = Table.objects.get(pk=pk)
        table.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 


        
        
            
    

 
