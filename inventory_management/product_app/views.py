from datetime import datetime

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


class CreateProduct(APIView):
    def get(self,request):

        obj = Product()
        obj.name = "Fridge" #request.GET.get("name")
        obj.product_id = 2346 #request.GET.get("name")
        obj.price = 12000 #request.GET.get("name")
        obj.actual_quantity = 1000 #request.GET.get("name")
        obj.product_record = {0: {"prodct_name": str(obj.name),"timestamp":str(datetime.now()), "initial_quantity":str(obj.actual_quantity),
                                   "price":str(obj.price), "product_id":str(obj.product_id)}}
        obj.save()
        return Response("saved")


class Delete(APIView):
    def get(self, request):
        WarehouseProductDescription.objects.all().delete()
        Product.objects.all().delete()
        return Response("done")

class ProductTransport(APIView):

    def post(self,request):
        try:
            product_id = 30  # request.data['product_id']
            from_location_id = 5  # request.data['from_location']
            quantity_add = 10  # request.data['quantity']
            to_location_id = 4  # request.data['to_location']
            if to_location_id == from_location_id:
                return Response("Same Location Not Possible")

            ware_data2 = WarehouseProductDescription.objects.filter(product_id=product_id, location_id=from_location_id)
            print(ware_data2)
            asd = {}
            asd['quantity'] =  quantity_add
            if ware_data2.exists():
                for data in ware_data2:
                    if int(data.quantity) < quantity_add:
                        return Response('quantity is not available')
                    else:
                        asd['previous_from_location_quantity'] = data.quantity
                        asd['from_loc_time'] = str(datetime.now())
                        data.quantity = int(data.quantity) - quantity_add
                        data.save()
                        asd['from_location'] = from_location_id, data.location.name
                        asd['updated_from_location_quantity'] = data.quantity
            else:
                create_wh_pdt(product_id, from_location_id)
                return Response("created")
            ware_data1 = WarehouseProductDescription.objects.filter(product_id=product_id, location_id=to_location_id)
            if ware_data1.exists():
                for dat in ware_data1:
                    print("1111111111111111111")
                    asd['previous_to_location_quantity'] = dat.quantity
                    dat.quantity = int(dat.quantity) + quantity_add
                    dat.save()
                    asd['to_location'] = to_location_id, dat.location.name
                    asd['updated_to_location_quantity'] = dat.quantity
                    asd['to_loc_time'] = str(datetime.now())
                    b = Product.objects.get(id=product_id)
                    ass = list(b.product_record.keys())
                    num = ass[-1]
                    b.product_record[int(num) + 1] = asd
                    b.save()
                    return Response("updated")

            else:
                datae = WarehouseProductDescription()
                datae.quantity = int(quantity_add)
                datae.product_id = int(product_id)
                datae.location_id = int(to_location_id)
                datae.save()
                asd['previous_to_location_quantity'] = 0
                asd['updated_to_location_quantity'] = quantity_add
                asd['to_location'] = to_location_id, datae.location.name
                asd['to_loc_time'] = str(datetime.now())
                b = Product.objects.get(id=product_id)
                ass = list(b.product_record.keys())
                num = ass[-1]
                b.product_record[int(num) + 1] = asd
                b.save()
                return Response("new created")

        except Exception as e:
            return Response(e)


def create_wh_pdt(product_id, location_id):

    if WarehouseProductDescription.objects.filter(product_id=product_id, location_id=location_id).exists():
        pass
    else:
        b = Product.objects.get(id=product_id)
        a = WarehouseProductDescription()
        a.quantity = b.actual_quantity
        a.product_id = product_id
        a.location_id = location_id
        a.save()

        b.product_record[1] = {"product_name":b.name,"from_location":a.location.name,"timestamp": str(datetime.now()),
                               "quantity": a.quantity, "to_location":""}

        b.save()
        return Response("new created")
    return Response("Nothing Happenned")

