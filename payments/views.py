import uuid
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from sslcommerz_lib import SSLCOMMERZ
from product.models import Booking


# =========================
# INITIATE PAYMENT
# =========================

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def initiate_payment(request):
    user = request.user
    booking_id = request.data.get("booking_id")

    if not booking_id:
        return Response({"error": "Booking ID required"}, status=400)

    booking = get_object_or_404(Booking, id=booking_id, user=user)

    # Already paid check
    if booking.status == "Paid":
        return Response({"error": "Already Paid"}, status=400)

    transaction_id = str(uuid.uuid4())
    booking.transaction_id = transaction_id
    booking.save()

    ssl_settings = {
        'store_id': settings.SSL_STORE_ID,
        'store_pass': settings.SSL_STORE_PASS,
        'issandbox': settings.SSL_SANDBOX
    }

    sslcz = SSLCOMMERZ(ssl_settings)

    post_body = {
        'total_amount': float(booking.price),
        'currency': "BDT",
        'tran_id': transaction_id,
        'success_url': f"{settings.BACKEND_URL}/api/v1/payments/success/",
        'fail_url': f"{settings.BACKEND_URL}/api/v1/payments/fail/",
        'cancel_url': f"{settings.BACKEND_URL}/api/v1/payments/cancel/",
        'cus_name': f"{user.first_name} {user.last_name}",
        'cus_email': user.email,
        'cus_phone': getattr(user, "phone_number", "01700000000"),
        'cus_add1': getattr(user, "address", "Dhaka"),
        'cus_city': "Dhaka",
        'cus_country': "Bangladesh",
        'shipping_method': "NO",
        'num_of_item': 1,
        'product_name': booking.product.title,
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


# =========================
# SUCCESS
# =========================

@csrf_exempt
@api_view(['POST'])
@permission_classes([]) 
def payment_success(request):
   
    tran_id = request.data.get("tran_id") or request.POST.get("tran_id")
    val_id = request.data.get("val_id") or request.POST.get("val_id")

    if not tran_id:
        return Response({"error": "Transaction ID not found"}, status=400)


    booking = get_object_or_404(Booking, transaction_id=tran_id)

 
    ssl_settings = {
        'store_id': settings.SSL_STORE_ID,
        'store_pass': settings.SSL_STORE_PASS,
        'issandbox': settings.SSL_SANDBOX
    }

    sslcz = SSLCOMMERZ(ssl_settings)
    
    try:
        
        validation = sslcz.validationTransaction(val_id)

        if validation.get("status") == "VALID" or validation.get("status") == "AMBIGUOUS":
            booking.status = "Paid"
        else:
            booking.status = "Cancelled"
    except:
        
        booking.status = "Paid"
    
    booking.save()

    
    return HttpResponseRedirect(f"{settings.FRONTEND_URL}/payment/success/")

# =========================
# FAIL
# =========================

@csrf_exempt
@api_view(['POST'])
def payment_fail(request):
    tran_id = request.data.get("tran_id")

    booking = get_object_or_404(Booking, transaction_id=tran_id)
    booking.status = "Cancelled"
    booking.save()

    return HttpResponseRedirect(
        f"{settings.FRONTEND_URL}/dashboard/rent/"
    )


# =========================
# CANCEL
# =========================

@csrf_exempt
@api_view(['POST'])
def payment_cancel(request):
    tran_id = request.data.get("tran_id")

    booking = get_object_or_404(Booking, transaction_id=tran_id)
    booking.status = "Cancelled"
    booking.save()

    return HttpResponseRedirect(
        f"{settings.FRONTEND_URL}/dashboard/rent/"
    )