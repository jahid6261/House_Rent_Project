from rest_framework import serializers
from product.models import Product

class AdvertisementSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()  # ইউজারের নাম দেখাবে

    class Meta:
        model = Product
        fields = ['id', 'title', 'owner', 'address', 'location', 'price', 'stock', 'approved', 'created_at']
