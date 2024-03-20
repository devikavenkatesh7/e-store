from django.contrib.auth.models import User
from rest_framework import serializers

from product.models import Profile, Product, OrderHistory, Review, Cart, Location


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        exclude = ('user',)


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        exclude = ('added_by',)


class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    user = UserSerializer()

    class Meta:
        model = Cart
        fields = ['product', 'quantity', 'is_purchased', 'user']


class OrderSerializerIn(serializers.Serializer):
    delivery_address = serializers.IntegerField()


class OrderSerializerOut(serializers.ModelSerializer):
    ordered_by = UserSerializer()
    delivery_address = LocationSerializer()


class OrderHistorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderHistory
        fields = "__all__"
