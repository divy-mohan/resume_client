from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# app_name = 'writers_app'  # Removed namespace for simplicity

urlpatterns = [
    # Public pages
    path('', views.IndexView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('services/', views.ServicesView.as_view(), name='services'),
    path('service/<slug:slug>/', views.ServiceDetailView.as_view(), name='service_detail'),
    
    path('pricing/', views.PricingView.as_view(), name='pricing'),
    path('testimonials/', views.TestimonialsView.as_view(), name='testimonials'),
    path('blog/', views.BlogListView.as_view(), name='blog'),
    path('blog/<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('faq/', views.FAQView.as_view(), name='faq'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('samples/', views.SamplesView.as_view(), name='samples'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('terms/', views.TermsView.as_view(), name='terms'),
    path('refund/', views.RefundView.as_view(), name='refund'),
    path('linkedin-service/', views.LinkedInView.as_view(), name='linkedin_service'),
    path('visual-cv-service/', views.VisualCVView.as_view(), name='visual_cv_service'),
    path('infographic-cv-service/', views.InfographicCVView.as_view(), name='infographic_cv_service'),
    path('job-hunt-service/', views.JobHuntView.as_view(), name='job_hunt_service'),
    path('sop-service/', views.SOPView.as_view(), name='sop_service'),
    path('lor-service/', views.LORView.as_view(), name='lor_service'),

    # Authentication
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),

    # User dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('profile/', views.ProfileView.as_view(), name='profile'),

    # Order management
    path('order/<int:package_id>/', views.CreateOrderView.as_view(), name='create_order'),
    path('order/<int:order_id>/payment/', views.PaymentView.as_view(), name='payment'),
    path('order/<int:order_id>/success/', views.PaymentSuccessView.as_view(), name='payment_success'),
    path('order/<int:order_id>/chat/', views.ChatView.as_view(), name='chat'),

    # API endpoints
    path('api/newsletter/subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
    path('api/payment/razorpay/verify/', views.verify_razorpay_payment, name='verify_razorpay_payment'),
    path('api/chat/<int:order_id>/messages/', views.get_chat_messages, name='get_chat_messages'),
    
    # Admin dashboard (for staff users)
    path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
]