import uuid
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from sslcommerz_lib import SSLCOMMERZ
from .models import Payment
from product.models import Booking



# INITIATE PAYMENT

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_payment(request):
    user = request.user
    booking_id = request.data.get("booking_id")

    if not booking_id:
        return Response({"error": "Booking ID required"}, status=400)

    booking = get_object_or_404(Booking, id=booking_id, user=user)

    amount = booking.rent_amount
    transaction_id = str(uuid.uuid4())

    payment = Payment.objects.create(
        user=user,
        booking=booking,
        amount=amount,
        transaction_id=transaction_id,
        status='PENDING'
    )

    ssl_settings = {
        'store_id': settings.SSL_STORE_ID,
        'store_pass': settings.SSL_STORE_PASS,
        'issandbox': settings.SSL_SANDBOX
    }

    sslcz = SSLCOMMERZ(ssl_settings)

    post_body = {
        'total_amount': amount,
        'currency': "BDT",
        'tran_id': transaction_id,
        'success_url': f"{settings.BACKEND_URL}/api/v1/payments/success/",
        'fail_url': f"{settings.BACKEND_URL}/api/v1/payments/fail/",
        'cancel_url': f"{settings.BACKEND_URL}/api/v1/payments/cancel/",
        'cus_name': f"{user.first_name} {user.last_name}",
        'cus_email': user.email,
        'cus_phone': user.phone_number,
        'cus_add1': user.address,
        'cus_city': "Dhaka",
        'cus_country': "Bangladesh",
        'shipping_method': "NO",
        'num_of_item': 1,
        'product_name': "House Rent Payment",
        'product_category': "Rent",
        'product_profile': "general"
    }

    response = sslcz.createSession(post_body)

    if response.get("status") == 'SUCCESS':
        return Response({
            "payment_url": response['GatewayPageURL'],
            "transaction_id": transaction_id
        })

    return Response({"error": "Payment initiation failed"}, status=400)



# SUCCESS

@csrf_exempt
@api_view(['GET', 'POST'])
def payment_success(request):
    tran_id = request.GET.get("tran_id") or request.data.get("tran_id")

    payment = get_object_or_404(Payment, transaction_id=tran_id)

    payment.status = 'SUCCESS'
    payment.save()

    booking = payment.booking
    booking.status = 'Paid'
    booking.save()

    return HttpResponseRedirect(
        f"{settings.FRONTEND_URL}/dashboard/rent/"
    )



# FAIL

@csrf_exempt
@api_view(['GET', 'POST'])
def payment_fail(request):
    tran_id = request.GET.get("tran_id") or request.data.get("tran_id")

    payment = get_object_or_404(Payment, transaction_id=tran_id)

    payment.status = 'FAILED'
    payment.save()

    return HttpResponseRedirect(
        f"{settings.FRONTEND_URL}/dashboard/rent/"
    )



# CANCEL

@csrf_exempt
@api_view(['GET', 'POST'])
def payment_cancel(request):
    tran_id = request.GET.get("tran_id") or request.data.get("tran_id")

    payment = get_object_or_404(Payment, transaction_id=tran_id)

    payment.status = 'CANCELLED'
    payment.save()

    return HttpResponseRedirect(
        f"{settings.FRONTEND_URL}/dashboard/rent/"
    )
