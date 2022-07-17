import pandas as pd
from django.shortcuts import render
# Create your views here.
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action

from common.models import Province, City
from other_files.response_serialzer import ProvinceResponseSerializer, CityResponseSerializer


class CommonView(viewsets.ModelViewSet):
    @action(methods=["post"], detail=False)
    def create_data(self, request):
        data = pd.read_excel(r'other_files/province_list.xlsx')
        data_obj = pd.DataFrame(data,).values
        for city_name,province_name in data_obj:
            obj_province,_=Province.objects.get_or_create(name=province_name)
            obj_province,_=City.objects.get_or_create(name=city_name,province=obj_province)
        return Response({"message":"done"},status=status.HTTP_200_OK)


    @action(methods=["get"], detail=False)
    def province(self,request):
        instances=Province.objects.all()
        serializer=ProvinceResponseSerializer(instances)
        return Response(serializer.data,)

    @action(methods=["get"], detail=False)
    def city(self,request):
        instances=City.objects.all()
        serializer=CityResponseSerializer(instances)
        return Response(serializer.data,)