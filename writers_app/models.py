from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid


class User(AbstractUser):
    """Extended User model with additional profile information"""
    phone = models.CharField(max_length=15, blank=True)
    country = models.CharField(max_length=100, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    experience_years = models.IntegerField(null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

    def __str__(self):
        return self.get_full_name()


class Service(models.Model):
    """Service offerings like Resume Writing, LinkedIn Optimization, etc."""
    ICON_CHOICES = [
        # Resume/CV Related Icons
        ('fa-file-alt', 'Basic Document'),
        ('fa-file-image', 'Visual/Infographic CV'),
        ('fa-file-invoice', 'Professional CV'),
        ('fa-chart-line', 'Infographic Elements'),
        ('fa-palette', 'Visual Design'),
        
        # Job Hunt Related
        ('fa-briefcase', 'Job/Career'),
        ('fa-search', 'Job Search'),
        ('fa-bullseye', 'Job Target'),
        ('fa-handshake', 'Job Offer'),
        ('fa-map-signs', 'Career Path'),
        
        # Academic Writing Related
        ('fa-graduation-cap', 'Academic'),
        ('fa-university', 'University'),
        ('fa-book', 'Statement of Purpose'),
        ('fa-envelope-open-text', 'Letter of Recommendation'),
        ('fa-award', 'Achievements'),
        
        # LinkedIn/Social Related
        ('fab fa-linkedin', 'LinkedIn'),
        ('fas fa-user-tie', 'Professional Profile'),
        ('fas fa-network-wired', 'Professional Network'),
        ('fas fa-share-alt', 'Social Presence'),
        ('fas fa-project-diagram', 'Network Growth'),
        
        # Additional Professional Icons
        ('fa-certificate', 'Certifications'),
        ('fa-star', 'Excellence'),
        ('fa-trophy', 'Achievements'),
        ('fa-medal', 'Awards'),
        ('fa-crown', 'Premium Quality'),
        ('fa-rocket', 'Career Launch'),
        ('fa-lightbulb', 'Innovation'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300)
    icon = models.CharField(max_length=100, choices=ICON_CHOICES, help_text="Select an icon for the service")
    

    
    # Display options
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    # Legacy fields
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    booking_url = models.CharField(max_length=255, blank=True)
    details_url = models.CharField(max_length=255, blank=True, help_text="URL name for Learn More button (e.g., 'linkedin_service', 'services')")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return f"/service/{self.slug}/"
        
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_learn_more_url(self):
        return self.details_url or 'services'
    



class ServicePackage(models.Model):
    """Different pricing tiers for services"""
    CURRENCY_CHOICES = [
        ('INR', 'Indian Rupee'),
        ('USD', 'US Dollar'),
    ]

    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='packages')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price_inr = models.DecimalField(max_digits=10, decimal_places=2)
    price_usd = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)
    delivery_days = models.IntegerField()
    revisions = models.IntegerField()
    is_popular = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['service', 'display_order', 'price_inr']

    def __str__(self):
        return f"{self.service.name} - {self.name}"

    def get_price(self, currency='INR'):
        return self.price_inr if currency == 'INR' else self.price_usd


class Order(models.Model):
    """Customer orders for services"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('revision', 'Under Revision'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    order_number = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    service_package = models.ForeignKey(ServicePackage, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # Payment details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR')
    payment_method = models.CharField(max_length=50, blank=True)
    payment_id = models.CharField(max_length=100, blank=True)
    
    # Order details
    requirements = models.TextField(help_text="Customer requirements and specifications")
    deadline = models.DateTimeField()
    notes = models.TextField(blank=True)
    
    # File uploads
    uploaded_resume = models.FileField(upload_to='uploads/resumes/', null=True, blank=True)
    additional_files = models.JSONField(default=list, help_text="List of additional uploaded files")
    
    # Delivery
    final_files = models.JSONField(default=list, help_text="List of delivered files")
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.order_number} - {self.user.get_full_name()}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate order number: PW + YYYYMMDD + random string
            date_str = timezone.now().strftime('%Y%m%d')
            random_str = str(uuid.uuid4())[:8].upper()
            self.order_number = f"PW{date_str}{random_str}"
        super().save(*args, **kwargs)


class ChatMessage(models.Model):
    """Chat messages between customers and support team"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='chat_messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_admin = models.BooleanField(default=False)
    attachment = models.FileField(upload_to='uploads/chat/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message from {self.user.get_full_name()} - {self.created_at}"


class BlogPost(models.Model):
    """Blog posts for career tips and company updates"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    excerpt = models.TextField(max_length=500)
    featured_image = models.ImageField(upload_to='blog/', null=True, blank=True)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    tags = models.JSONField(default=list)
    meta_description = models.CharField(max_length=160, blank=True)
    view_count = models.IntegerField(default=0)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    """Customer testimonials and reviews"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    is_featured = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    position = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='testimonials/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Testimonial by {self.user.get_full_name()}"


class FAQ(models.Model):
    """Frequently Asked Questions"""
    question = models.CharField(max_length=300)
    answer = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'order']

    def __str__(self):
        return self.question


class NewsletterSubscriber(models.Model):
    """Newsletter email subscribers"""
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email


class ContactMessage(models.Model):
    """Contact form submissions"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    service = models.CharField(max_length=50, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_responded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"


class BlogComment(models.Model):
    """Blog post comments"""
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"


class SampleCategory(models.Model):
    """Categories for resume samples"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#007bff', help_text='Hex color code')
    icon = models.CharField(max_length=50, default='fas fa-folder')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Sample Categories'

    def __str__(self):
        return self.name


class ResumeSample(models.Model):
    """Resume samples for portfolio"""
    SAMPLE_TYPE_CHOICES = [
        ('before', 'Before'),
        ('after', 'After'),
        ('standalone', 'Standalone'),
    ]
    
    title = models.CharField(max_length=200)
    category = models.ForeignKey(SampleCategory, on_delete=models.CASCADE, related_name='samples')
    sample_type = models.CharField(max_length=20, choices=SAMPLE_TYPE_CHOICES, default='standalone')
    image = models.ImageField(upload_to='samples/', help_text='A4 ratio image (210x297mm or 595x842px)')
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.category.name})"
    
