from django.db.models import F
from django.shortcuts import render
# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from product_app.models import Location, Product, WarehouseProductDescription
from product_app.serializers import LocationSerializer, ProductSerializer, WarehouseProductDescriptionSerializer


class LocationList(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class WarehouseProductDescriptionList(generics.ListCreateAPIView):
    queryset = WarehouseProductDescription.objects.all()
    serializer_class = WarehouseProductDescriptionSerializer


class ProductTransport(APIView):
    def post(self,request):
        try:
            product_id = 1  #request.data['product_id']
            to_location_id = 1  #request.data['to_location']
            quantity_add = 15  #request.data['quantity']
            try:
                from_location_id = 2  # request.data['from_location']
                print("dddddddddddddddddddddddddddd")
                if to_location_id == from_location_id:
                    return Response("Same Location Not Possible")
                print("dddddddddddddddddddddddddddd")
                data = WarehouseProductDescription.objects.get(product_id=product_id, location_id=to_location_id)
                print(data.quantity, "sssssssss")
                if int(data.quantity) < quantity_add:
                    return Response('quantity is not available')
                print("dddddddddddddddddddddddddddd")
                a = WarehouseProductDescription.objects.filter(product_id=product_id, location_id=to_location_id).\
                    update(quantity=F('quantity') - quantity_add)
                print("ddddddddd")
                c = WarehouseProductDescription.objects.filter(product_id=product_id, location_id=from_location_id). \
                    update(quantity=F('quantity') - quantity_add)
                print('1')

                print('12')
                b = Product.objects.get(id=product_id)
                b.product_record[3] = {"product_name":b.name,"to_location":a.location.name, "quatity": a.quantity, "from_location":"22"}
                print('123')
                b.save()
                return Response("saved")
            except:
                a = WarehouseProductDescription()
                a.quantity =0
                a.product_id = product_id
                a.location_id = to_location_id
                a.save()
                b = Product.objects.get(id=product_id)
                b.product_record[2] = {"product_name":b.name,"to_location":a.location.name, "quatity": a.quantity, "from_location":"22"}

                b.save()
                return Response("new created")
        except Exception as e:
            return Response("data is not correct")
