import razorpay
from django.shortcuts import get_object_or_404, redirect, render,HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from Cart.models import Order
from .models import Payment,Invoice
from django.contrib import messages
from Cart.views import get_cart
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import datetime

# Initialize Razorpay Client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@login_required
def process_payment(request, order_id):
    """Handles payment creation and redirection to Razorpay."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Create Razorpay order
    razorpay_order = client.order.create({
        'amount': int(order.total_price * 100),  # Razorpay takes the amount in paise (1 INR = 100 paise)
        'currency': 'INR',
        'payment_capture': '1'  # Auto capture
    })

    # Store razorpay_order_id in Payment model
    payment = Payment.objects.create(
        order=order,
        user=request.user,
        amount=order.total_price,
        razorpay_order_id=razorpay_order['id']
    )

    # Pass necessary information to the template
    context = {
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'amount': order.total_price * 100,  # Amount in paise
        'order_id': order.id,
        'order':order,
    }

    return render(request, 'process_payment.html', context)


@csrf_exempt
def payment_success(request):
    """Handles payment statuses: Success, Failed, and Pending."""
    if request.method == "POST":
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_signature = request.POST.get('razorpay_signature', '')

        payment = get_object_or_404(Payment, razorpay_order_id=razorpay_order_id)

        # Verifying payment signature to ensure it’s legitimate
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })

            # If verification succeeds, mark the payment as successful
            payment.razorpay_payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.status = 'SUCCESS'
            payment.save()

            

            # Mark order as paid
            order = payment.order
            order.is_paid = True
            order.status = 'Processing'
            order.save()

            #Invoice generation
            invoice, created = Invoice.objects.get_or_create(order=order,defaults={'total_amount': order.total_price, 'is_paid': True})
            # Optionally: Clear cart after successful payment
            cart = get_cart(request)
            cart.cart_items.all().delete()

            messages.success(request, "Payment successful!")

            #directly  downloading the pdf and rediecting to the pay page but i want to rediect it to the order details page
            # return generate_invoice_pdf(invoice)  

            return redirect('order_detail', order_id=order.id)

        except razorpay.errors.SignatureVerificationError:
            # If verification fails, mark payment as failed
            payment.status = 'FAILED'
            payment.save()

            messages.error(request, "Payment verification failed. Please try again.")
            return redirect('order_detail', order_id=payment.order.id)

    return redirect('cart_detail')


@login_required
def payment_pending(request, order_id):
    """Handles payment pending situation."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    payment = order.payment

    if payment.status == 'PENDING':
        messages.warning(request, "Your payment is still being processed. Please wait for confirmation.")
    else:
        messages.info(request, "Payment status updated.")

    return redirect('order_detail', order_id=order.id)


def generate_invoice_pdf(invoice):
    template_path = 'invoice_template.html'
    context = {
        'invoice': invoice,
        'order': invoice.order,
        'user': invoice.order.user,
        'date': datetime.datetime.now(),
    }

    # Render the HTML template with context
    html = render_to_string(template_path, context)

    # Create a PDF file response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{invoice.invoice_filename}"'

    # Convert HTML to PDF using xhtml2pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response