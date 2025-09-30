
from rest_framework import serializers
from .models import Category, Product,  RentRequest, Favorite,Review,ProductImage
from django.contrib.auth import get_user_model

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'product_count']
        
    product_count = serializers.IntegerField(read_only=True)

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']
class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True) 
   

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'owner',
            'address',
            'location',
            'description',
            'category',
            'stock',
            'price',
            'approved',
            'created_at',
            'updated_at',
            'images',
            
        ]


class RentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentRequest
        fields = ['id', 'advertisement', 'user', 'accepted', 'created_at']


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'advertisement']

class SimpleUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(
        method_name='get_current_user_name')

    class Meta:
        model = get_user_model()
        fields = ['id', 'name']

    def get_current_user_name(self, obj):
        return obj.get_full_name()        

class ReviewSerializer(serializers.ModelSerializer):
   
    user = serializers.SerializerMethodField(method_name='get_user')

    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'rating', 'comment']
        read_only_fields = ['user','produce']

    def get_user(self, obj):
        return SimpleUserSerializer(obj.user).data

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)        