from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from product.models import Product
from .serializers import AdvertisementSerializer
from django.utils.timezone import now

class AdminAdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [permissions.IsAdminUser]  # শুধুমাত্র admin access

    # Statistics API
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        today = now().date()
        current_month_ads = Product.objects.filter(
            created_at__month=today.month,
            created_at__year=today.year
        ).count()
        last_month_ads = Product.objects.filter(
            created_at__month=today.month-1,
            created_at__year=today.year
        ).count()
        return Response({
            'current_month_ads': current_month_ads,
            'last_month_ads': last_month_ads
        }, status=status.HTTP_200_OK)
