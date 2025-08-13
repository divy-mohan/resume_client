import razorpay
import hashlib
import hmac
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_email(subject, recipients, template=None, **context):
    """Send email using Django's email system"""
    try:
        if template:
            html_message = render_to_string(f'email/{template}', context)
        else:
            # Default email template for contact forms
            html_message = f"""
            <html>
                <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 20px; text-align: center;">
                        <h1 style="color: white; margin: 0;">Professional Writers</h1>
                    </div>
                    <div style="padding: 20px;">
                        <h2>New Contact Form Submission</h2>
                        <p><strong>Name:</strong> {context.get('name', 'N/A')}</p>
                        <p><strong>Email:</strong> {context.get('email', 'N/A')}</p>
                        <p><strong>Phone:</strong> {context.get('phone', 'N/A')}</p>
                        <p><strong>Service:</strong> {context.get('service', 'N/A')}</p>
                        <p><strong>Subject:</strong> {context.get('contact_subject', 'N/A')}</p>
                        <p><strong>Message:</strong></p>
                        <div style="background: #f8f9fa; padding: 15px; border-left: 4px solid #2a5298;">
                            {context.get('message', 'N/A')}
                        </div>
                    </div>
                    <div style="background: #f8f9fa; padding: 20px; text-align: center; margin-top: 20px;">
                        <p style="margin: 0; color: #666;">Professional Writers - Your Career Success Partner</p>
                    </div>
                </body>
            </html>
            """
        
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
    subject = "Welcome to Professional Writers!"
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 20px; text-align: center;">
                <h1 style="color: white; margin: 0;">Welcome to Professional Writers!</h1>
            </div>
            <div style="padding: 20px;">
                <h2>Hello {user.get_full_name()}!</h2>
                <p>Thank you for joining Professional Writers. We're excited to help you achieve your career goals.</p>
                <p>Here's what you can expect from us:</p>
                <ul>
                    <li>🎓 IIT/IIM Alumni Writers</li>
                    <li>🌍 Global Resume Standards</li>
                    <li>🧠 AI + Human Expertise</li>
                    <li>📞 24x7 Client Support</li>
                </ul>
                <p>Ready to get started? Browse our services and find the perfect package for your needs.</p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="#" style="background: #2a5298; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px;">Explore Services</a>
                </div>
            </div>
            <div style="background: #f8f9fa; padding: 20px; text-align: center;">
                <p style="margin: 0; color: #666;">Professional Writers - Your Career Success Partner</p>
            </div>
        </body>
    </html>
    """
    
    try:
        email = EmailMessage(
            subject=subject,
            body=html_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        email.content_subtype = 'html'
        email.send()
        return True
    except Exception as e:
        print(f"Welcome email failed: {e}")
        return False


def process_refund(payment_id, amount):
    """Process refund for a payment"""
    try:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        refund = client.payment.refund(payment_id, {
            'amount': int(amount * 100)  # Convert to paisa
        })
        
        return refund
    except Exception as e:
        print(f"Refund processing failed: {e}")
        return None


def create_paypal_order(amount_usd):
    """Create PayPal order (placeholder implementation)"""
    # PayPal integration would go here
    return {
        'id': 'paypal_order_id',
        'status': 'CREATED'
    }


def verify_paypal_payment(payment_id):
    """Verify PayPal payment (placeholder implementation)"""
    # PayPal verification would go here
    return True


def send_order_confirmation(order):
    """Send order confirmation email"""
    subject = f"Order Confirmation #{order.order_number}"
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 20px; text-align: center;">
                <h1 style="color: white; margin: 0;">Order Confirmed!</h1>
            </div>
            <div style="padding: 20px;">
                <h2>Hello {order.user.get_full_name()}!</h2>
                <p>Your order has been successfully confirmed and payment received.</p>
                
                <div style="background: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="margin-top: 0;">Order Details</h3>
                    <p><strong>Order Number:</strong> {order.order_number}</p>
                    <p><strong>Service:</strong> {order.service_package.service.name}</p>
                    <p><strong>Package:</strong> {order.service_package.name}</p>
                    <p><strong>Amount Paid:</strong> ₹{order.amount}</p>
                    <p><strong>Status:</strong> Confirmed</p>
                </div>
                
                <p>Our expert writers will start working on your order immediately. You can track the progress and communicate with our team through your dashboard.</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="#" style="background: #2a5298; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px;">View Order Status</a>
                </div>
                
                <p>If you have any questions, feel free to reach out to us at any time.</p>
            </div>
            <div style="background: #f8f9fa; padding: 20px; text-align: center;">
                <p style="margin: 0; color: #666;">Professional Writers - Your Career Success Partner</p>
            </div>
        </body>
    </html>
    """
    
    try:
        from django.core.mail import EmailMessage
        email = EmailMessage(
            subject=subject,
            body=html_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[order.user.email]
        )
        email.content_subtype = 'html'
        email.send()
        return True
    except Exception as e:
        print(f"Order confirmation email failed: {e}")
        return False


def send_order_confirmation(order):
    """Send order confirmation email"""
    return send_email(
        subject=f"Order Confirmation - {order.order_number}",
        recipients=[order.user.email],
        template='order_confirmation.html',
        order=order,
        user=order.user
    )