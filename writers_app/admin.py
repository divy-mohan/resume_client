from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from .models import (
    User, Service, ServicePackage, Order, ChatMessage, 
    BlogPost, Testimonial, FAQ, NewsletterSubscriber, ContactMessage,
    SampleCategory, ResumeSample
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
    list_display = ['name', 'icon', 'price', 'is_active', 'is_featured', 'order', 'created_at']
    list_filter = ['is_active', 'is_featured']
    search_fields = ['name', 'description', 'short_description']
    list_editable = ['icon', 'is_active', 'is_featured', 'order']
    fieldsets = (
        (None, {
            'fields': ('name', 'icon', 'description', 'short_description')
        }),
        ('Display Options', {
            'fields': ('is_active', 'is_featured', 'order')
        }),
        ('Pricing & Links', {
            'fields': ('price', 'booking_url', 'details_url')
        })
    )


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


class SampleCategoryForm(forms.ModelForm):
    COLOR_CHOICES = [
        ('#007bff', '🔵 Blue (#007bff)'),
        ('#28a745', '🟢 Green (#28a745)'),
        ('#dc3545', '🔴 Red (#dc3545)'),
        ('#ffc107', '🟡 Yellow (#ffc107)'),
        ('#6f42c1', '🟣 Purple (#6f42c1)'),
        ('#fd7e14', '🟠 Orange (#fd7e14)'),
        ('#20c997', '🟢 Teal (#20c997)'),
        ('#e83e8c', '🩷 Pink (#e83e8c)'),
        ('#6c757d', '⚫ Gray (#6c757d)'),
        ('#17a2b8', '🔷 Cyan (#17a2b8)'),
        ('#343a40', '⚫ Dark (#343a40)'),
        ('#f8f9fa', '⚪ Light (#f8f9fa)'),
    ]
    
    ICON_CHOICES = [
        ('fas fa-file-alt', '📄 Document (fas fa-file-alt)'),
        ('fas fa-user-tie', '👔 Professional (fas fa-user-tie)'),
        ('fas fa-briefcase', '💼 Business (fas fa-briefcase)'),
        ('fas fa-graduation-cap', '🎓 Education (fas fa-graduation-cap)'),
        ('fas fa-code', '💻 Technology (fas fa-code)'),
        ('fas fa-paint-brush', '🎨 Creative (fas fa-paint-brush)'),
        ('fas fa-stethoscope', '🩺 Healthcare (fas fa-stethoscope)'),
        ('fas fa-chart-line', '📈 Finance (fas fa-chart-line)'),
        ('fas fa-cogs', '⚙️ Engineering (fas fa-cogs)'),
        ('fas fa-bullhorn', '📢 Marketing (fas fa-bullhorn)'),
        ('fas fa-users', '👥 HR (fas fa-users)'),
        ('fas fa-balance-scale', '⚖️ Legal (fas fa-balance-scale)'),
        ('fas fa-camera', '📷 Photography (fas fa-camera)'),
        ('fas fa-music', '🎵 Music (fas fa-music)'),
        ('fas fa-plane', '✈️ Travel (fas fa-plane)'),
        ('fas fa-utensils', '🍽️ Food Service (fas fa-utensils)'),
        ('fas fa-home', '🏠 Real Estate (fas fa-home)'),
        ('fas fa-car', '🚗 Automotive (fas fa-car)'),
        ('fas fa-heart', '❤️ Non-profit (fas fa-heart)'),
        ('fas fa-star', '⭐ Featured (fas fa-star)'),
    ]
    
    color = forms.ChoiceField(
        choices=COLOR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Select a color for this category'
    )
    
    icon = forms.ChoiceField(
        choices=ICON_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Select an icon for this category'
    )
    
    class Meta:
        model = SampleCategory
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

@admin.register(SampleCategory)
class SampleCategoryAdmin(admin.ModelAdmin):
    form = SampleCategoryForm
    list_display = ['name', 'slug', 'color_preview', 'icon_preview', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'order']
    
    def color_preview(self, obj):
        return f'<span style="display:inline-block;width:20px;height:20px;background-color:{obj.color};border:1px solid #ccc;border-radius:3px;margin-right:5px;"></span>{obj.color}'
    color_preview.allow_tags = True
    color_preview.short_description = 'Color'
    
    def icon_preview(self, obj):
        return f'<i class="{obj.icon}" style="margin-right:5px;"></i>{obj.icon}'
    icon_preview.allow_tags = True
    icon_preview.short_description = 'Icon'
    
    class Media:
        css = {
            'all': ('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',)
        }


@admin.register(ResumeSample)
class ResumeSampleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'sample_type', 'is_featured', 'is_active', 'view_count', 'created_at']
    list_filter = ['category', 'sample_type', 'is_featured', 'is_active', 'created_at']
    search_fields = ['title']
    list_editable = ['is_featured', 'is_active']
    readonly_fields = ['view_count']
    
    class Media:
        css = {
            'all': ('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',)
        }