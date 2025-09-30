# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from adminpanel.views import AdminAdvertisementViewSet
from product.views import CategoryViewSet, ProductViewSet, RentRequestViewSet, FavoriteViewSet,ReviewViewSet,ProductImageViewSet


# Main router
router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('products', ProductViewSet, basename='product')

# Nested router for RentRequests and Favorites under Product
product_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('rent-requests', RentRequestViewSet, basename='product-rentrequests')
products_router.register('favorites', FavoriteViewSet, basename='product-favorites')
products_router.register('reviews', ReviewViewSet, basename='product-reviews') 
products_router.register('images', ProductImageViewSet,
                        basename='product-images')
router.register( 'admin-ads', AdminAdvertisementViewSet, basename='admin-ads')
urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
      path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    
]
