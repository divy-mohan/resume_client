from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView
)
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
import json
import razorpay

from .models import *
from .forms import *
from .utils import send_email, create_razorpay_order, verify_payment_signature


class IndexView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testimonials'] = Testimonial.objects.filter(is_featured=True, is_approved=True)[:6]
        context['blog_posts'] = BlogPost.objects.filter(is_published=True)[:3]
        context['services'] = Service.objects.filter(is_active=True)[:6]
        context['featured_samples'] = ResumeSample.objects.filter(is_featured=True, is_active=True)[:6]
        return context


class AboutView(TemplateView):
    template_name = 'about.html'


class ServicesView(ListView):
    model = Service
    template_name = 'services.html'
    context_object_name = 'services'
    
    def get_queryset(self):
        return Service.objects.filter(is_active=True)


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'service_detail.html'
    context_object_name = 'service'
    
    def get_queryset(self):
        return Service.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['packages'] = self.object.packages.filter(is_active=True).order_by('display_order')
        context['testimonials'] = Testimonial.objects.filter(is_approved=True, is_featured=True)[:3]
        return context


class PricingView(TemplateView):
    template_name = 'pricing.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.filter(is_active=True).prefetch_related('packages')
        return context


class TestimonialsView(ListView):
    model = Testimonial
    template_name = 'testimonials.html'
    context_object_name = 'testimonials'
    paginate_by = 12
    
    def get_queryset(self):
        return Testimonial.objects.filter(is_approved=True).order_by('-created_at')


class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog.html'
    context_object_name = 'posts'
    paginate_by = 9
    
    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True).order_by('-published_at')


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog_post.html'
    context_object_name = 'post'
    slug_field = 'slug'
    
    def get_object(self):
        obj = super().get_object()
        obj.view_count += 1
        obj.save()
        return obj


class FAQView(ListView):
    model = FAQ
    template_name = 'faq.html'
    context_object_name = 'faqs'
    
    def get_queryset(self):
        return FAQ.objects.filter(is_active=True).order_by('category', 'order')


class ContactView(CreateView):
    model = ContactMessage
    form_class = ContactForm
    template_name = 'contact.html'
    success_url = '/contact/'
    
    def form_valid(self, form):
        # Save the form
        response = super().form_valid(form)
        
        # Send notification email
        from .utils import send_email
        send_email(
            subject=f"New Contact Form Submission - {form.cleaned_data.get('service', 'General')}",
            recipients=[settings.DEFAULT_FROM_EMAIL],
            template=None,  # Use default template
            name=form.cleaned_data['name'],
            email=form.cleaned_data['email'],
            phone=form.cleaned_data.get('phone', ''),
            service=form.cleaned_data.get('service', ''),
            contact_subject=form.cleaned_data['subject'],
            message=form.cleaned_data['message']
        )
        
        messages.success(self.request, 'Thank you for your message! We will get back to you within 24 hours.')
        return response


class SamplesView(TemplateView):
    template_name = 'samples.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = SampleCategory.objects.filter(is_active=True).order_by('order')
        samples_by_category = {}
        
        for category in categories:
            samples_by_category[category] = ResumeSample.objects.filter(
                category=category, is_active=True
            ).order_by('-is_featured', '-created_at')
        
        context['samples_by_category'] = samples_by_category
        context['categories'] = categories
        return context


class PrivacyView(TemplateView):
    template_name = 'privacy.html'


class TermsView(TemplateView):
    template_name = 'terms.html'


class RefundView(TemplateView):
    template_name = 'refund.html'


class LinkedInView(TemplateView):
    template_name = 'linkedin_service.html'


class VisualCVView(TemplateView):
    template_name = 'visual_cv_service.html'


class InfographicCVView(TemplateView):
    template_name = 'infographic_cv_service.html'


class JobHuntView(TemplateView):
    template_name = 'job_hunt_service.html'


class SOPView(TemplateView):
    template_name = 'sop_service.html'


class LORView(TemplateView):
    template_name = 'lor_service.html'


# Authentication Views
class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'
    
    def get_success_url(self):
        return '/dashboard/'


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = '/dashboard/'
    
    def form_valid(self, form):
        user = form.save()
        
        # Send welcome email
        from .utils import send_welcome_email
        send_welcome_email(user)
        
        login(self.request, user)
        messages.success(self.request, 'Welcome! Your account has been created successfully.')
        return super().form_valid(form)


# User Dashboard Views
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(user=self.request.user).order_by('-created_at')
        context['recent_orders'] = context['orders'][:5]
        return context


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'profile.html'
    success_url = '/profile/'
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)


# Order Management Views
class CreateOrderView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'create_order.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        package_id = self.kwargs['package_id']
        context['package'] = get_object_or_404(ServicePackage, id=package_id)
        return context
    
    def form_valid(self, form):
        package = get_object_or_404(ServicePackage, id=self.kwargs['package_id'])
        order = form.save(commit=False)
        order.user = self.request.user
        order.service_package = package
        order.amount = package.price_inr  # Default to INR, can be modified
        order.currency = 'INR'
        order.save()
        return redirect('writers_app:payment', order_id=order.id)


class PaymentView(LoginRequiredMixin, TemplateView):
    template_name = 'payment.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs['order_id']
        context['order'] = get_object_or_404(Order, id=order_id, user=self.request.user)
        
        # Create Razorpay order
        if context['order'].payment_status == 'pending':
            from .utils import create_razorpay_order
            razorpay_order = create_razorpay_order(context['order'])
            if razorpay_order:
                context['razorpay_order'] = razorpay_order
                context['razorpay_key'] = settings.RAZORPAY_KEY_ID
        
        return context


class PaymentSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'payment_success.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs['order_id']
        context['order'] = get_object_or_404(Order, id=order_id, user=self.request.user)
        return context


class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chat.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs['order_id']
        context['order'] = get_object_or_404(Order, id=order_id, user=self.request.user)
        context['messages'] = ChatMessage.objects.filter(order_id=order_id).order_by('created_at')
        context['form'] = ChatMessageForm()
        return context
    
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        form = ChatMessageForm(request.POST, request.FILES)
        
        if form.is_valid():
            message = form.save(commit=False)
            message.order = order
            message.user = request.user
            message.save()
            messages.success(request, 'Message sent successfully!')
        
        return redirect('writers_app:chat', order_id=order_id)


# Admin Views
class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'admin/admin_dashboard.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'Access denied.')
            return redirect('writers_app:index')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_orders'] = Order.objects.count()
        context['pending_orders'] = Order.objects.filter(status='pending').count()
        context['total_users'] = User.objects.count()
        context['recent_orders'] = Order.objects.order_by('-created_at')[:10]
        return context


# API Views
def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
            if created:
                messages.success(request, 'Successfully subscribed to our newsletter!')
            else:
                messages.info(request, 'You are already subscribed to our newsletter.')
        else:
            messages.error(request, 'Please provide a valid email address.')
    
    return redirect(request.META.get('HTTP_REFERER', '/'))


def verify_razorpay_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_id = data.get('order_id')
            payment_id = data.get('payment_id')
            signature = data.get('signature')
            
            order = get_object_or_404(Order, id=order_id, user=request.user)
            
            # Verify payment signature
            from .utils import verify_payment_signature, send_order_confirmation
            if verify_payment_signature(payment_id, order.order_number, signature):
                order.payment_status = 'paid'
                order.payment_id = payment_id
                order.status = 'confirmed'
                order.save()
                
                # Send order confirmation email
                send_order_confirmation(order)
                
                return JsonResponse({'success': True, 'redirect': f'/order/{order.id}/success/'})
            else:
                return JsonResponse({'success': False, 'error': 'Payment verification failed'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def get_chat_messages(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    messages = ChatMessage.objects.filter(order=order).order_by('created_at')
    
    messages_data = [{
        'id': msg.id,
        'message': msg.message,
        'is_admin': msg.is_admin,
        'created_at': msg.created_at.isoformat(),
        'user_name': msg.user.get_full_name() if not msg.is_admin else 'Support Team'
    } for msg in messages]
    
    return JsonResponse(messages_data, safe=False)