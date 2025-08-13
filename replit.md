# Professional Writers - Career Documentation Platform

## Overview

Professional Writers is a comprehensive career documentation platform that provides professional resume writing, LinkedIn optimization, cover letter writing, and other career services. The platform serves both Indian and international clients, offering packages in multiple currencies (INR/USD) with integrated payment processing through Razorpay and PayPal. The system features real-time chat communication between clients and writers, user authentication, order management, and an admin dashboard for business operations.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes

- **Django Conversion Completed (August 6, 2025)**: Successfully converted entire Flask project to Django
- **Migration from Flask to Django**: Complete rewrite of models, views, forms, and templates
- **Django Features Added**: Admin interface, class-based views, Django forms with Crispy Forms
- **Database Migration**: Converted SQLAlchemy models to Django ORM models with custom User model
- **Authentication System**: Replaced Flask-Login with Django's built-in authentication
- **WebSocket Support**: Implemented Django Channels for real-time chat functionality
- **Template Conversion**: Updated all Jinja2 templates to Django template syntax
- **URL Routing**: Converted Flask routes to Django URLconf patterns
- **Static Files**: Configured Django static files system with WhiteNoise
- **Requirements**: Created django_requirements.txt for easy installation
- **Model Relationships Fixed**: Resolved conflicts between Order and ServicePackage models
- **Admin User Created**: Successfully created admin superuser for Django admin interface
- **Django Server Running**: Application now running successfully on Django framework

## System Architecture

### Backend Architecture
- **Framework**: Flask-based web application with modular structure
- **Database**: SQLAlchemy ORM with SQLite default (configurable to other databases)
- **Authentication**: Flask-Login for user session management with role-based access (admin/customer)
- **Real-time Communication**: Flask-SocketIO for live chat between clients and service providers
- **File Handling**: Secure file upload system for resumes and documents with UUID-based naming

### Frontend Architecture
- **Template Engine**: Jinja2 templating with Bootstrap 5 for responsive design
- **CSS Framework**: Custom CSS with CSS variables for brand consistency, featuring blue gradient color scheme
- **JavaScript**: Vanilla JavaScript with Socket.IO client for real-time features
- **Typography**: Playfair Display for headings, Lato for body text
- **Responsive Design**: Mobile-first approach with progressive enhancement

### Database Schema
- **User Management**: User model with profile information, admin flags, and relationship mapping
- **Service Management**: Service and ServicePackage models for different offerings and pricing tiers
- **Order System**: Order tracking with status management and file associations
- **Communication**: ChatMessage model for real-time client-writer communication
- **Content Management**: Blog, testimonials, and FAQ management capabilities

### Payment Integration
- **Multi-currency Support**: Razorpay for INR payments, PayPal for international transactions
- **Payment Verification**: Signature verification for secure payment processing
- **Order Generation**: Automated order number generation with date-based prefixes

### Email System
- **Flask-Mail Integration**: SMTP email delivery for notifications and confirmations
- **Template System**: HTML email templates for welcome messages and order confirmations
- **Service Communication**: Automated email workflows for customer engagement

### Security Features
- **Password Security**: Werkzeug password hashing for secure authentication
- **File Security**: Secure filename handling and restricted file type uploads
- **Session Management**: Environment-based secret key configuration
- **Proxy Handling**: ProxyFix middleware for deployment behind reverse proxies

## External Dependencies

### Core Framework Dependencies
- **Flask**: Web application framework with extensions for database, authentication, and email
- **SQLAlchemy**: Database ORM with declarative base model structure
- **Flask-SocketIO**: WebSocket support for real-time chat functionality
- **WTForms**: Form handling and validation with CSRF protection

### Payment Gateways
- **Razorpay**: Indian payment gateway for INR transactions with order creation and verification
- **PayPal**: International payment processing for USD transactions (placeholder implementation)

### Email Service
- **SMTP Configuration**: Gmail SMTP integration with TLS encryption
- **Environment Variables**: Configurable email credentials and server settings

### Frontend Libraries
- **Bootstrap 5**: CSS framework for responsive design components
- **Font Awesome**: Icon library for UI elements and navigation
- **Google Fonts**: Playfair Display and Lato font families for brand typography

### Development Tools
- **Database Configuration**: Environment-based database URL with connection pooling
- **Logging**: Built-in Python logging for debugging and error tracking
- **File Storage**: Local file system storage with configurable upload directories

### Environment Configuration
- **Session Security**: Configurable secret keys for production deployment
- **Database URLs**: Support for SQLite, PostgreSQL, and other SQLAlchemy-compatible databases
- **Service Credentials**: Environment-based API key management for payment and email services