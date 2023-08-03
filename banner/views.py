from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from .serializers import *
from rest_framework.decorators import api_view


        
        
@api_view(['GET'])
def bannerView(request):
    parser_classes = (MultiPartParser, FormParser)
    banners = Banner.objects.all()
    serializer=BannerSerializer(banners,many=True)
    return Response({'status':200,'payload':serializer.data})
    
         


@api_view(['POST'])
def bannerAdd(request):
    data=request.data
    print('dataaaaaa',data)
    serializer=BannerSerializer(data=data)
    if not serializer.is_valid():
        print(serializer.errors)
        return Response({'status':403,'errors':serializer.errors,'message':'something wrong'})
    serializer.save()
    return Response({'status':200,'payload':serializer.data,'message':'data saved'})

@api_view(['PUT'])
def update_banner(request,id):
    try:
        banner=Banner.objects.get(id=id)
        serializer=BannerSerializer(banner,data=request.data,partial=True)
        if not serializer.is_valid():
          print(serializer.errors)
          return Response({'status':403,'errors':serializer.errors,'message':'something wrong'})
        serializer.save()
        return Response({'status':200,'payload':serializer.data,'message':'data saved'})

    except Exception as e:
       return Response({'status':403,'message':'invalid id'})         

@api_view(['DELETE'])
def delete_banner(request,id):
    try:
        city_obj=Banner.objects.get(id=id)  
        city_obj.delete()
        return Response({'status':200,'message':'deleted'})

    except Exception as e:
       return Response({'status':403,'message':'invalid id'})        
   
   

# class bannerView(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     def get(self, request, *args, **kwargs):
#         banners = Banner.objects.all()
#         serializer = BannerSerializer(banners, many=True)
#         return Response(serializer.data)
    
# class bannerAdd(APIView):
#     def post(self, request, *args, **kwargs):
#         banner_serializer = BannerSerializer(data=request.data)
#         if banner_serializer.is_valid():
#             banner_serializer.save()
#             return Response(banner_serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             print('error', banner_serializer.errors)
#             return Response(banner_serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
   
   
   
   


        
        
            
    
            
