import os
from flask import render_template_string, current_app
from flask_mail import Message
from app import mail

def send_email(subject, recipients, template=None, **kwargs):
    """Send email using Flask-Mail"""
    try:
        msg = Message(
            subject=subject,
            recipients=recipients,
            sender=current_app.config.get('MAIL_DEFAULT_SENDER')
        )
        
        if template:
            # In a real application, you would use render_template() with actual email templates
            msg.html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 20px; text-align: center;">
                        <h1 style="color: white; margin: 0;">Professional Writers</h1>
                    </div>
                    <div style="padding: 20px;">
                        <h2>Hello!</h2>
                        <p>Thank you for contacting Professional Writers.</p>
                        <p><strong>Details:</strong></p>
                        <p>Name: {kwargs.get('name', 'N/A')}</p>
                        <p>Email: {kwargs.get('email', 'N/A')}</p>
                        <p>Phone: {kwargs.get('phone', 'N/A')}</p>
                        <p>Service: {kwargs.get('service', 'N/A')}</p>
                        <p>Message: {kwargs.get('message', 'N/A')}</p>
                    </div>
                    <div style="background: #f8f9fa; padding: 20px; text-align: center; margin-top: 20px;">
                        <p style="margin: 0; color: #666;">Professional Writers - Your Career Success Partner</p>
                    </div>
                </body>
            </html>
            """
        
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to send email: {str(e)}")
        return False

def send_welcome_email(email, name):
    """Send welcome email to new users"""
    subject = "Welcome to Professional Writers!"
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 20px; text-align: center;">
                <h1 style="color: white; margin: 0;">Welcome to Professional Writers!</h1>
            </div>
            <div style="padding: 20px;">
                <h2>Hello {name}!</h2>
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
        msg = Message(
            subject=subject,
            recipients=[email],
            sender=current_app.config.get('MAIL_DEFAULT_SENDER'),
            html=html_content
        )
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to send welcome email: {str(e)}")
        return False

def send_order_confirmation(order):
    """Send order confirmation email"""
    subject = f"Order Confirmation - {order.order_number}"
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 20px; text-align: center;">
                <h1 style="color: white; margin: 0;">Order Confirmed!</h1>
            </div>
            <div style="padding: 20px;">
                <h2>Hello {order.customer.get_full_name()}!</h2>
                <p>Your order has been confirmed and we're excited to work on your project.</p>
                
                <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="margin-top: 0;">Order Details:</h3>
                    <p><strong>Order Number:</strong> {order.order_number}</p>
                    <p><strong>Service:</strong> {order.package.service.name}</p>
                    <p><strong>Package:</strong> {order.package.name}</p>
                    <p><strong>Amount:</strong> ₹{order.amount}</p>
                    <p><strong>Delivery:</strong> {order.package.delivery_days} working days</p>
                </div>
                
                <p><strong>What's Next?</strong></p>
                <ol>
                    <li>Our team will review your requirements within 24 hours</li>
                    <li>You'll be assigned a dedicated writer from our expert team</li>
                    <li>We'll start working on your project immediately</li>
                    <li>You can track progress through your dashboard</li>
                </ol>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="#" style="background: #2a5298; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px;">View Order Status</a>
                </div>
            </div>
            <div style="background: #f8f9fa; padding: 20px; text-align: center;">
                <p style="margin: 0; color: #666;">Professional Writers - Your Career Success Partner</p>
            </div>
        </body>
    </html>
    """
    
    try:
        msg = Message(
            subject=subject,
            recipients=[order.customer.email],
            sender=current_app.config.get('MAIL_DEFAULT_SENDER'),
            html=html_content
        )
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to send order confirmation: {str(e)}")
        return False

def send_order_completed_email(order):
    """Send email when order is completed"""
    subject = f"Your Order is Complete - {order.order_number}"
    # Implementation for order completion email
    pass

def send_newsletter_email(subscribers, subject, content):
    """Send newsletter to subscribers"""
    # Implementation for newsletter emails
    pass
