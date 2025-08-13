from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div, HTML
from .models import Order, ContactMessage, NewsletterSubscriber, ChatMessage

User = get_user_model()


class ContactForm(forms.ModelForm):
    SERVICE_CHOICES = [
        ('resume-writing', 'Resume Writing'),
        ('linkedin-profile', 'LinkedIn Profile Optimization'),
        ('cover-letter', 'Cover Letter Writing'),
        ('sop-lor', 'SOP/LOR Writing'),
        ('career-counselling', 'Career Counselling'),
        ('other', 'Other')
    ]
    
    service = forms.ChoiceField(choices=SERVICE_CHOICES, required=False)
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'service', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Please describe your requirements...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Send Message'))


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=15, required=False)
    country = forms.CharField(max_length=100, required=False)
    profession = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 
                 'phone', 'country', 'profession', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Sign Up'))


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Log In'))


class BlogCommentForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), max_length=1000)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Post Comment'))


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_show_labels = False
        self.helper.add_input(Submit('submit', 'Subscribe'))


class OrderForm(forms.ModelForm):
    uploaded_resume = forms.FileField(required=False, help_text="Upload your current resume (PDF, DOC, DOCX)")

    class Meta:
        model = Order
        fields = ['requirements', 'deadline', 'uploaded_resume']
        widgets = {
            'requirements': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Please describe your requirements, target role, industry, and any specific preferences...'}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Fieldset(
                'Order Details',
                'requirements',
                'deadline',
                'uploaded_resume',
            ),
            Submit('submit', 'Proceed to Payment')
        )


class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message', 'attachment']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your message...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.add_input(Submit('submit', 'Send'))


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'country', 
                 'profession', 'experience_years', 'bio', 'linkedin_url', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.add_input(Submit('submit', 'Update Profile'))