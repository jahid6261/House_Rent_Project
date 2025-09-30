from rest_framework import viewsets, permissions
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from api.permissions import IsAdminOrReadOnly
from product.permissions import IsReviewAuthorOrReadonly
from .models import Category, Product, RentRequest, Favorite,Review,ProductImage
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    RentRequestSerializer,
    FavoriteSerializer,
    ReviewSerializer,
    ProductImageSerializer
)
from product.filters import ProductFilter
from product.paginations import DefaultPagination  
from drf_yasg.utils import swagger_auto_schema


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.annotate(product_count=Count('products'))
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(approved=True)
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['title', 'description']  
    ordering_fields = ['price', 'updated_at']

    permission_classes = [IsAdminOrReadOnly]
    @swagger_auto_schema(
        operation_summary="Create a new product",
        operation_description="This endpoint allows an admin to create a new product. "
                              "Owner is automatically set as the logged-in user."
    )      
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    @swagger_auto_schema(
        operation_summary="List all products",
        operation_description="Retrieve a paginated list of all approved products. "
                              "Supports filtering, searching and ordering."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]
    @swagger_auto_schema(
        operation_summary="List product images",
        operation_description="Retrieve all images for a specific product."
    )

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs.get('product_pk'))

    def perform_create(self, serializer):
        serializer.save(product_id=self.kwargs.get('product_pk'))


class RentRequestViewSet(viewsets.ModelViewSet):
    serializer_class = RentRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(
        operation_summary="List rent requests",
        operation_description="Retrieve all rent requests for a specific advertisement."
    )
    def get_queryset(self):
        product_pk = self.kwargs.get('product_pk')
        
        return RentRequest.objects.filter(advertisement_id=product_pk)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, advertisement_id=self.kwargs.get('product_pk'))




class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(advertisement_id=self.kwargs.get('product_pk'))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, advertisement_id=self.kwargs.get('product_pk'))





class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorOrReadonly]
    @swagger_auto_schema(
        operation_summary="Create a new review",
        operation_description="Users can create a review for a specific product. "
                              "The logged-in user will automatically be set as the review author."
    )
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    @swagger_auto_schema(
        operation_summary="Update a review",
        operation_description="Users can update their own review for a product."
    )
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
    @swagger_auto_schema(
        operation_summary="Get product reviews",
        operation_description="Retrieve all reviews for a given product."
    )
    
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs.get('product_pk'))

    def get_serializer_context(self):
        return {'product_id': self.kwargs.get('product_pk')}     
 