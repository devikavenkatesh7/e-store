from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from product.custom_permissions import IsSeller, IsBuyer
from .order import insert_order_data_into_db
from product.models import Product, Location, Cart, Order, Review
from product.myserializer import ProductSerializer, LocationSerializer, CartSerializer, UserSerializer, \
    OrderSerializerOut, OrderSerializerIn, ReviewSerializer


# Create your views here.
class ProductViewSet(ModelViewSet):
    """ provides GET, POST, PUT, DELETE APIs for Product and only the seller has access to this API """
    # permission_classes = [permissions.IsAuthenticated, IsSeller]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


class MyUserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LocationViewSet(ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class CartViewSet(ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated, IsBuyer]
    queryset = Cart.objects.all().order_by('-id')
    serializer_class = CartSerializer

    # def get_queryset(self):
    #     return Cart.objects.filter(Q(user=self.request.user) & Q(is_purchased=False))


@api_view(['GET', 'POST'])
def order_now(request: Request) -> Response:
    if request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializerOut(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = OrderSerializerIn(request.data)
        if serializer.is_valid():
            result = insert_order_data_into_db(request)
            # print(result)
            if result == 1:
                return Response({'response': 'order placed successfully'}, status=status.HTTP_200_OK)
            elif result == 0:
                return Response({'response': 'Invalid delivery address'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({'delivery_address': 'This field is mandatory'}, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated, IsBuyer]
    queryset = Review.objects.all().order_by('-id')
    serializer_class = ReviewSerializer