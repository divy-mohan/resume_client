# Professional Writers - Django Project

This project has been successfully converted from Flask to Django. Here's how to set it up and run it on your local machine.

## Installation and Setup

### 1. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r django_requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the project root with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database Settings (PostgreSQL)
DATABASE_URL=postgresql://username:password@localhost:5432/professional_writers
PGDATABASE=professional_writers
PGHOST=localhost
PGPORT=5432
PGUSER=postgres
PGPASSWORD=yourpassword

# Email Settings
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_DEFAULT_SENDER=your_email@gmail.com

# Payment Settings
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret
PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_CLIENT_SECRET=your_paypal_client_secret

# Redis Settings (for Channels/WebSocket)
REDIS_URL=redis://localhost:6379/0
```

### 4. Database Setup
```bash
# Create and run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load initial data (optional)
python manage.py loaddata initial_data.json
```

### 5. Collect Static Files
```bash
python manage.py collectstatic
```

### 6. Run the Server
```bash
python manage.py runserver
```

The application will be available at: http://127.0.0.1:8000/

## Key Features Converted

### ✅ Models
- **User Model**: Extended Django's AbstractUser with additional fields
- **Service & ServicePackage**: Service offerings and pricing tiers
- **Order Management**: Complete order processing system
- **Chat System**: Real-time messaging with WebSocket support
- **Blog System**: Content management for blog posts
- **Testimonials**: Customer reviews and ratings
- **FAQ System**: Frequently asked questions
- **Newsletter**: Email subscription management

### ✅ Views & URLs
- **Class-based views** for better organization
- **Authentication**: Login, logout, registration, password reset
- **User Dashboard**: Profile management and order tracking
- **Payment Processing**: Razorpay integration
- **Admin Dashboard**: Staff management interface
- **API endpoints**: RESTful APIs for AJAX functionality

### ✅ Templates
- **Bootstrap 5** responsive design
- **Crispy Forms** integration for form rendering
- **Django template syntax** (converted from Jinja2)
- **Static files** properly configured

### ✅ Features
- **CSRF Protection**: Built-in Django security
- **Admin Interface**: Django admin for content management
- **Email System**: Django's email backend
- **WebSocket Support**: Django Channels for real-time chat
- **File Uploads**: Secure file handling for resumes
- **Payment Integration**: Razorpay payment gateway

## Directory Structure
```
professional_writers/
├── manage.py
├── django_requirements.txt
├── professional_writers/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── writers_app/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── utils.py
│   ├── consumers.py
│   ├── routing.py
│   └── migrations/
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── registration/
│   └── ... (other templates)
└── static/
    ├── css/
    ├── js/
    └── images/
```

## Additional Setup for Production

### 1. Database Configuration
Update `DATABASES` in settings.py for your production database.

### 2. Redis Setup (for Channels)
Install and configure Redis for WebSocket support:
```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS
brew install redis

# Start Redis
redis-server
```

### 3. Static Files
Configure `STATIC_ROOT` and run `collectstatic` for production.

### 4. Environment Variables
Set all environment variables in your production environment.

## API Endpoints

- `/api/newsletter/subscribe/` - Newsletter subscription
- `/api/payment/razorpay/verify/` - Payment verification
- `/api/chat/<order_id>/messages/` - Chat messages

## WebSocket Endpoints

- `/ws/chat/<order_id>/` - Real-time chat for orders

## Admin Interface

Access the Django admin at: http://127.0.0.1:8000/admin/

Create a superuser to access the admin interface and manage:
- Users and permissions
- Services and packages
- Orders and payments
- Blog posts and testimonials
- FAQ and newsletter subscribers

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure PostgreSQL is running
   - Check database credentials in .env file
   - Run `python manage.py migrate`

2. **Static Files Not Loading**
   - Run `python manage.py collectstatic`
   - Check `STATIC_URL` and `STATIC_ROOT` in settings.py

3. **Redis Connection Error**
   - Start Redis server: `redis-server`
   - Check `CHANNEL_LAYERS` configuration in settings.py

4. **Email Not Sending**
   - Configure SMTP settings in .env file
   - For Gmail, use app-specific passwords

## Development Commands

```bash
# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic
```

## Notes

- The project uses Django 4.2+ features
- PostgreSQL is recommended for production
- Redis is required for WebSocket functionality
- All templates have been converted to Django template syntax
- Forms use Django Crispy Forms with Bootstrap 5