import os
import uuid
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, jsonify, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app import app, db
from models import *
from forms import *
from email_service import send_email, send_welcome_email, send_order_confirmation
from payment_service import create_razorpay_order, verify_razorpay_payment

# Helper function to generate order number
def generate_order_number():
    return f"PW{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"

# Helper function to save uploaded files
def save_uploaded_file(file, order_id, file_type='resume'):
    if file and file.filename:
        filename = secure_filename(file.filename)
        unique_filename = f"{order_id}_{file_type}_{uuid.uuid4().hex}_{filename}"
        
        # Create uploads directory if it doesn't exist
        upload_dir = os.path.join(current_app.root_path, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, unique_filename)
        file.save(file_path)
        
        return unique_filename
    return None

@app.route('/')
def index():
    # Get featured testimonials
    testimonials = Testimonial.query.filter_by(is_featured=True).limit(6).all()
    
    # Get latest blog posts
    blog_posts = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.created_at.desc()).limit(3).all()
    
    # Get services for preview
    services = Service.query.filter_by(is_active=True).limit(6).all()
    
    return render_template('index.html', 
                         testimonials=testimonials, 
                         blog_posts=blog_posts,
                         services=services)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    services = Service.query.filter_by(is_active=True).all()
    return render_template('services.html', services=services)

@app.route('/service/<int:service_id>')
def service_detail(service_id):
    service = Service.query.get_or_404(service_id)
    packages = ServicePackage.query.filter_by(service_id=service_id, is_active=True).all()
    testimonials = Testimonial.query.filter_by(service_used=service.name).limit(3).all()
    
    return render_template('service_detail.html', 
                         service=service, 
                         packages=packages,
                         testimonials=testimonials)

@app.route('/pricing')
def pricing():
    services = Service.query.filter_by(is_active=True).all()
    packages_by_service = {}
    
    for service in services:
        packages_by_service[service.id] = ServicePackage.query.filter_by(
            service_id=service.id, is_active=True
        ).all()
    
    return render_template('pricing.html', 
                         services=services, 
                         packages_by_service=packages_by_service)

@app.route('/samples')
def samples():
    return render_template('samples.html')

@app.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)
    posts = BlogPost.query.filter_by(is_published=True).order_by(
        BlogPost.created_at.desc()
    ).paginate(page=page, per_page=6, error_out=False)
    
    return render_template('blog.html', posts=posts)

@app.route('/blog/<slug>')
def blog_post(slug):
    post = BlogPost.query.filter_by(slug=slug, is_published=True).first_or_404()
    related_posts = BlogPost.query.filter(
        BlogPost.id != post.id, 
        BlogPost.is_published == True
    ).limit(3).all()
    
    return render_template('blog_post.html', post=post, related_posts=related_posts)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Send email notification
        send_email(
            subject=f"New Contact Form Submission - {form.service.data}",
            recipients=[current_app.config.get('MAIL_DEFAULT_SENDER')],
            template='email/contact_notification.html',
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            service=form.service.data,
            message=form.message.data
        )
        
        flash('Thank you for your message! We will get back to you within 24 hours.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html', form=form)

@app.route('/testimonials')
def testimonials():
    testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    return render_template('testimonials.html', testimonials=testimonials)

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/refund')
def refund():
    return render_template('refund.html')

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Welcome back!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('auth/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if user already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please use a different email.', 'error')
            return render_template('auth/register.html', form=form)
        
        # Create new user
        user = User(
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        # Send welcome email
        send_welcome_email(user.email, user.get_full_name())
        
        login_user(user)
        flash('Registration successful! Welcome to Professional Writers!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('auth/register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

# Dashboard and order management
@app.route('/dashboard')
@login_required
def dashboard():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('dashboard.html', orders=orders)

@app.route('/order/<int:package_id>', methods=['GET', 'POST'])
@login_required
def create_order(package_id):
    package = ServicePackage.query.get_or_404(package_id)
    form = OrderForm()
    form.package_id.data = package_id
    
    if form.validate_on_submit():
        # Create order
        order = Order(
            user_id=current_user.id,
            package_id=package_id,
            order_number=generate_order_number(),
            amount=package.price_inr,
            notes=form.notes.data
        )
        
        db.session.add(order)
        db.session.flush()  # Get the order ID
        
        # Save uploaded file if provided
        if form.current_resume.data:
            filename = save_uploaded_file(form.current_resume.data, order.id, 'current_resume')
            if filename:
                order_file = OrderFile(
                    order_id=order.id,
                    filename=filename,
                    original_filename=form.current_resume.data.filename,
                    file_type='current_resume',
                    uploaded_by='customer'
                )
                db.session.add(order_file)
        
        db.session.commit()
        
        # Redirect to payment
        return redirect(url_for('payment', order_id=order.id))
    
    return render_template('order.html', package=package, form=form)

@app.route('/payment/<int:order_id>')
@login_required
def payment(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    
    if order.payment_status == 'paid':
        flash('This order has already been paid.', 'info')
        return redirect(url_for('dashboard'))
    
    # Create Razorpay order
    razorpay_order = create_razorpay_order(order.amount, order.order_number)
    
    return render_template('payment.html', order=order, razorpay_order=razorpay_order)

@app.route('/payment/success', methods=['POST'])
@login_required
def payment_success():
    # Verify payment
    payment_id = request.form.get('razorpay_payment_id')
    order_id = request.form.get('razorpay_order_id')
    signature = request.form.get('razorpay_signature')
    
    if verify_razorpay_payment(payment_id, order_id, signature):
        # Update order
        order = Order.query.filter_by(order_number=order_id.split('_')[1]).first()
        if order:
            order.payment_status = 'paid'
            order.payment_id = payment_id
            order.status = 'confirmed'
            db.session.commit()
            
            # Send confirmation email
            send_order_confirmation(order)
            
            flash('Payment successful! Your order has been confirmed.', 'success')
            return render_template('payment_success.html', order=order)
    
    flash('Payment verification failed. Please contact support.', 'error')
    return redirect(url_for('dashboard'))

# Newsletter subscription
@app.route('/subscribe', methods=['POST'])
def subscribe_newsletter():
    form = NewsletterForm()
    if form.validate_on_submit():
        # Check if already subscribed
        existing = EmailSubscriber.query.filter_by(email=form.email.data).first()
        if not existing:
            subscriber = EmailSubscriber(email=form.email.data)
            db.session.add(subscriber)
            db.session.commit()
            
            flash('Successfully subscribed to our newsletter!', 'success')
        else:
            flash('You are already subscribed to our newsletter.', 'info')
    
    return redirect(request.referrer or url_for('index'))

# API endpoints for chat and real-time features
@app.route('/api/chat/messages/<int:order_id>')
@login_required
def get_chat_messages(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    messages = ChatMessage.query.filter_by(order_id=order_id).order_by(ChatMessage.created_at.asc()).all()
    
    return jsonify([{
        'id': msg.id,
        'message': msg.message,
        'is_admin': msg.is_admin,
        'created_at': msg.created_at.isoformat(),
        'user_name': msg.user.get_full_name() if not msg.is_admin else 'Support Team'
    } for msg in messages])

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

# Initialize sample data
@app.route('/init-data')
def init_sample_data():
    """Initialize the database with sample services and packages"""
    if Service.query.count() > 0:
        return "Data already initialized"
    
    # Create services
    services_data = [
        {
            'name': 'Resume Writing',
            'description': 'Professional resume writing services for all career levels',
            'short_description': 'Get a professionally written resume that stands out',
            'icon': 'fas fa-file-alt'
        },
        {
            'name': 'LinkedIn Profile Optimization',
            'description': 'Optimize your LinkedIn profile for maximum visibility',
            'short_description': 'Enhance your LinkedIn presence and attract recruiters',
            'icon': 'fab fa-linkedin'
        },
        {
            'name': 'Cover Letter Writing',
            'description': 'Compelling cover letters that complement your resume',
            'short_description': 'Professional cover letters that make an impact',
            'icon': 'fas fa-envelope'
        },
        {
            'name': 'SOP/LOR Writing',
            'description': 'Statement of Purpose and Letter of Recommendation services',
            'short_description': 'Academic writing for university applications',
            'icon': 'fas fa-graduation-cap'
        },
        {
            'name': 'Career Counselling',
            'description': 'Professional career guidance and planning sessions',
            'short_description': 'Expert advice to accelerate your career growth',
            'icon': 'fas fa-user-tie'
        }
    ]
    
    for service_data in services_data:
        service = Service(**service_data)
        db.session.add(service)
        db.session.flush()
        
        # Add packages for each service
        packages_data = [
            {'name': 'Fresher', 'price_inr': 999, 'price_usd': 12, 'delivery_days': 2, 'revisions': 2},
            {'name': 'Premium', 'price_inr': 2499, 'price_usd': 30, 'delivery_days': 3, 'revisions': 3},
            {'name': 'Executive', 'price_inr': 3999, 'price_usd': 48, 'delivery_days': 5, 'revisions': 5},
            {'name': 'International', 'price_inr': 4999, 'price_usd': 60, 'delivery_days': 7, 'revisions': 5}
        ]
        
        for package_data in packages_data:
            package = ServicePackage(
                service_id=service.id,
                **package_data,
                features='["Professional formatting", "ATS optimization", "Keyword optimization", "Industry-specific content"]'
            )
            db.session.add(package)
    
    # Add sample testimonials
    testimonials_data = [
        {
            'client_name': 'Rahul Sharma',
            'client_title': 'Software Engineer',
            'client_company': 'Google',
            'client_location': 'Bangalore, India',
            'service_used': 'Resume Writing',
            'rating': 5,
            'testimonial': 'Professional Writers helped me land my dream job at Google. Their attention to detail and industry knowledge is exceptional.',
            'is_featured': True
        },
        {
            'client_name': 'Priya Patel',
            'client_title': 'Data Analyst',
            'client_company': 'Amazon',
            'client_location': 'Mumbai, India',
            'service_used': 'LinkedIn Profile Optimization',
            'rating': 5,
            'testimonial': 'My LinkedIn profile views increased by 300% after their optimization. Highly recommended!',
            'is_featured': True
        }
    ]
    
    for testimonial_data in testimonials_data:
        testimonial = Testimonial(**testimonial_data)
        db.session.add(testimonial)
    
    # Add sample blog posts
    blog_posts_data = [
        {
            'title': 'Top 5 Resume Mistakes to Avoid in 2025',
            'slug': 'top-5-resume-mistakes-2025',
            'content': 'Learn about the most common resume mistakes that could be costing you job opportunities...',
            'excerpt': 'Discover the critical resume mistakes that could be preventing you from landing interviews.',
            'author': 'Professional Writers Team',
            'is_published': True
        },
        {
            'title': 'ATS Optimization: Making Your Resume Robot-Friendly',
            'slug': 'ats-optimization-guide',
            'content': 'Understanding how Applicant Tracking Systems work and how to optimize your resume...',
            'excerpt': 'Master the art of ATS optimization to ensure your resume reaches human recruiters.',
            'author': 'Professional Writers Team',
            'is_published': True
        }
    ]
    
    for post_data in blog_posts_data:
        blog_post = BlogPost(**post_data)
        db.session.add(blog_post)
    
    db.session.commit()
    return "Sample data initialized successfully!"
