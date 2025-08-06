import razorpay
import hashlib
import hmac
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_email(subject, recipients, template, **context):
    """Send email using Django's email system"""
    try:
        html_message = render_to_string(f'email/{template}', context)
        plain_message = strip_tags(html_message)
        
        email = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipients
        )
        email.content_subtype = 'html'
        email.send()
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False


def create_razorpay_order(order):
    """Create Razorpay order"""
    try:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        razorpay_order = client.order.create({
            'amount': int(order.amount * 100),  # Amount in paisa
            'currency': order.currency,
            'receipt': order.order_number,
            'notes': {
                'order_id': order.id,
                'user_id': order.user.id
            }
        })
        
        return razorpay_order
    except Exception as e:
        print(f"Razorpay order creation failed: {e}")
        return None


def verify_payment_signature(payment_id, order_id, signature):
    """Verify Razorpay payment signature"""
    try:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        # Create signature verification string
        body = order_id + "|" + payment_id
        expected_signature = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode('utf-8'),
            body.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(expected_signature, signature)
    except Exception as e:
        print(f"Payment verification failed: {e}")
        return False


def send_welcome_email(user):
    """Send welcome email to new user"""
    return send_email(
        subject="Welcome to Professional Writers!",
        recipients=[user.email],
        template='welcome.html',
        user=user
    )


def send_order_confirmation(order):
    """Send order confirmation email"""
    return send_email(
        subject=f"Order Confirmation - {order.order_number}",
        recipients=[order.user.email],
        template='order_confirmation.html',
        order=order,
        user=order.user
    )