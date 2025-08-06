import os
import razorpay
import hmac
import hashlib
from flask import current_app

def create_razorpay_order(amount, order_number):
    """Create Razorpay order"""
    try:
        client = razorpay.Client(auth=(
            current_app.config.get('RAZORPAY_KEY_ID', 'rzp_test_key'),
            current_app.config.get('RAZORPAY_KEY_SECRET', 'rzp_test_secret')
        ))
        
        order_data = {
            'amount': int(amount * 100),  # Convert to paise
            'currency': 'INR',
            'receipt': f'order_{order_number}',
            'payment_capture': 1
        }
        
        order = client.order.create(data=order_data)
        return order
    except Exception as e:
        current_app.logger.error(f"Failed to create Razorpay order: {str(e)}")
        return None

def verify_razorpay_payment(payment_id, order_id, signature):
    """Verify Razorpay payment signature"""
    try:
        client = razorpay.Client(auth=(
            current_app.config.get('RAZORPAY_KEY_ID', 'rzp_test_key'),
            current_app.config.get('RAZORPAY_KEY_SECRET', 'rzp_test_secret')
        ))
        
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        
        client.utility.verify_payment_signature(params_dict)
        return True
    except Exception as e:
        current_app.logger.error(f"Payment verification failed: {str(e)}")
        return False

def create_paypal_order(amount_usd):
    """Create PayPal order (placeholder implementation)"""
    # PayPal integration would go here
    # This is a simplified placeholder
    return {
        'id': 'paypal_order_id',
        'status': 'CREATED'
    }

def verify_paypal_payment(payment_id):
    """Verify PayPal payment (placeholder implementation)"""
    # PayPal verification would go here
    return True

def process_refund(payment_id, amount):
    """Process refund for a payment"""
    try:
        client = razorpay.Client(auth=(
            current_app.config.get('RAZORPAY_KEY_ID', 'rzp_test_key'),
            current_app.config.get('RAZORPAY_KEY_SECRET', 'rzp_test_secret')
        ))
        
        refund = client.payment.refund(payment_id, {
            'amount': int(amount * 100)  # Convert to paise
        })
        
        return refund
    except Exception as e:
        current_app.logger.error(f"Refund failed: {str(e)}")
        return None
