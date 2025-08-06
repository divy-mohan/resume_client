from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Service, ServicePackage, Order, ChatMessage, 
    BlogPost, Testimonial, FAQ, NewsletterSubscriber, ContactMessage
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_admin', 'is_verified', 'created_at']
    list_filter = ['is_admin', 'is_verified', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('phone', 'country', 'profession', 'experience_years', 
                      'is_admin', 'is_verified', 'profile_picture', 'bio', 'linkedin_url')
        }),
    )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'order', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display = ['service', 'name', 'price_inr', 'price_usd', 'delivery_days', 'is_popular', 'is_active']
    list_filter = ['service', 'is_popular', 'is_active']
    search_fields = ['name', 'description']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'service_package', 'status', 'payment_status', 'amount', 'currency', 'created_at']
    list_filter = ['status', 'payment_status', 'currency', 'created_at']
    search_fields = ['order_number', 'user__username', 'user__email']
    readonly_fields = ['order_number']


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['order', 'user', 'is_admin', 'created_at']
    list_filter = ['is_admin', 'created_at']
    search_fields = ['message', 'user__username']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'is_featured', 'view_count', 'published_at']
    list_filter = ['is_published', 'is_featured', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating', 'is_featured', 'is_approved', 'company', 'created_at']
    list_filter = ['rating', 'is_featured', 'is_approved', 'created_at']
    search_fields = ['content', 'user__username', 'company']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'is_active', 'order']
    list_filter = ['category', 'is_active']
    search_fields = ['question', 'answer']


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_responded', 'created_at']
    list_filter = ['is_responded', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']