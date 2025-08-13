// Professional Writers - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initNavbar();
    initAnimations();
    initForms();
    initModalHandlers();
    initTooltips();
    initCarousels();
    
    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Navbar scroll effect
function initNavbar() {
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', throttle(function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }, 10));
    
    // Add smooth hover effects to nav links
    document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Animation on scroll
function initAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);
    
    // Observe all animated elements
    document.querySelectorAll('.fade-in, .slide-in-left, .slide-in-right').forEach((el, index) => {
        // Add staggered animation delay
        el.style.animationDelay = `${index * 0.1}s`;
        observer.observe(el);
    });
    
    // Add parallax effect to floating shapes
    window.addEventListener('scroll', throttle(() => {
        const scrolled = window.pageYOffset;
        const parallaxElements = document.querySelectorAll('.floating-shape');
        
        parallaxElements.forEach((element, index) => {
            const speed = 0.5 + (index * 0.1);
            const yPos = -(scrolled * speed);
            element.style.transform = `translateY(${yPos}px)`;
        });
    }, 10));
}

// Form handling
function initForms() {
    // Contact form
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', handleContactForm);
    }
    
    // Newsletter form
    const newsletterForm = document.getElementById('newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', handleNewsletterForm);
    }
    
    // Order form
    const orderForm = document.getElementById('order-form');
    if (orderForm) {
        orderForm.addEventListener('submit', handleOrderForm);
    }
}

function handleContactForm(e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    
    // Show loading state
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Sending...';
    submitBtn.disabled = true;
    
    // Submit form
    fetch(form.action, {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        showNotification('Message sent successfully! We will get back to you soon.', 'success');
        form.reset();
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('There was an error sending your message. Please try again.', 'error');
    })
    .finally(() => {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    });
}

function handleNewsletterForm(e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    
    fetch('/subscribe', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        showNotification('Successfully subscribed to our newsletter!', 'success');
        form.reset();
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Subscription failed. Please try again.', 'error');
    });
}

function handleOrderForm(e) {
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    
    // Show loading state
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
    submitBtn.disabled = true;
}

// Modal handlers
function initModalHandlers() {
    // Service detail modals
    document.querySelectorAll('[data-service-modal]').forEach(trigger => {
        trigger.addEventListener('click', function() {
            const serviceId = this.dataset.serviceModal;
            loadServiceModal(serviceId);
        });
    });
    
    // Sample modal handlers
    document.querySelectorAll('[data-sample-modal]').forEach(trigger => {
        trigger.addEventListener('click', function() {
            const sampleType = this.dataset.sampleModal;
            loadSampleModal(sampleType);
        });
    });
}

function loadServiceModal(serviceId) {
    // In a real application, you would fetch service details via AJAX
    console.log('Loading service modal for:', serviceId);
}

function loadSampleModal(sampleType) {
    // In a real application, you would load sample content
    console.log('Loading sample modal for:', sampleType);
}

// Tooltip initialization
function initTooltips() {
    // Initialize Bootstrap tooltips if available
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

// Carousel initialization
function initCarousels() {
    // Testimonials carousel
    const testimonialsCarousel = document.getElementById('testimonials-carousel');
    if (testimonialsCarousel && typeof bootstrap !== 'undefined') {
        new bootstrap.Carousel(testimonialsCarousel, {
            interval: 5000,
            wrap: true
        });
    }
    
    // Companies carousel
    const companiesCarousel = document.getElementById('companies-carousel');
    if (companiesCarousel && typeof bootstrap !== 'undefined') {
        new bootstrap.Carousel(companiesCarousel, {
            interval: 3000,
            wrap: true
        });
    }
}

// Notification system
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        max-width: 500px;
    `;
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Pricing calculator
function calculatePrice(packageType, region = 'india') {
    const pricing = {
        india: {
            fresher: 999,
            premium: 2499,
            executive: 3999,
            international: 4999
        },
        international: {
            fresher: 12,
            premium: 30,
            executive: 48,
            international: 60
        }
    };
    
    return pricing[region][packageType] || 0;
}

// Currency formatter
function formatCurrency(amount, currency = 'INR') {
    const formatters = {
        INR: new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR'
        }),
        USD: new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        })
    };
    
    return formatters[currency] ? formatters[currency].format(amount) : amount;
}

// Service package selection
function selectPackage(packageId, packageName, price) {
    // Store selected package in sessionStorage
    sessionStorage.setItem('selectedPackage', JSON.stringify({
        id: packageId,
        name: packageName,
        price: price
    }));
    
    // Redirect to order page or show login modal
    if (document.querySelector('.user-authenticated')) {
        window.location.href = `/order/${packageId}`;
    } else {
        showLoginModal();
    }
}

function showLoginModal() {
    // Show login modal
    const loginModal = document.getElementById('loginModal');
    if (loginModal && typeof bootstrap !== 'undefined') {
        const modal = new bootstrap.Modal(loginModal);
        modal.show();
    }
}

// File upload handler
function handleFileUpload(input) {
    const file = input.files[0];
    if (file) {
        const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
        const maxSize = 10 * 1024 * 1024; // 10MB
        
        if (!allowedTypes.includes(file.type)) {
            showNotification('Please upload only PDF or Word documents.', 'error');
            input.value = '';
            return false;
        }
        
        if (file.size > maxSize) {
            showNotification('File size should be less than 10MB.', 'error');
            input.value = '';
            return false;
        }
        
        // Show file info
        const fileInfo = input.parentNode.querySelector('.file-info');
        if (fileInfo) {
            fileInfo.textContent = `Selected: ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`;
            fileInfo.style.display = 'block';
        }
        
        return true;
    }
}

// Search functionality
function initSearch() {
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    
    if (searchInput && searchResults) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length < 2) {
                searchResults.style.display = 'none';
                return;
            }
            
            searchTimeout = setTimeout(() => {
                performSearch(query);
            }, 300);
        });
    }
}

function performSearch(query) {
    // In a real application, this would make an AJAX call to search endpoint
    console.log('Searching for:', query);
    
    // Mock search results
    const mockResults = [
        { title: 'Resume Writing Services', url: '/services/resume-writing' },
        { title: 'LinkedIn Profile Optimization', url: '/services/linkedin' },
        { title: 'Cover Letter Writing', url: '/services/cover-letter' }
    ];
    
    displaySearchResults(mockResults.filter(result => 
        result.title.toLowerCase().includes(query.toLowerCase())
    ));
}

function displaySearchResults(results) {
    const searchResults = document.getElementById('search-results');
    
    if (results.length === 0) {
        searchResults.innerHTML = '<div class="search-result">No results found</div>';
    } else {
        searchResults.innerHTML = results.map(result => 
            `<a href="${result.url}" class="search-result">${result.title}</a>`
        ).join('');
    }
    
    searchResults.style.display = 'block';
}

// FAQ accordion
function initFAQ() {
    document.querySelectorAll('.faq-question').forEach(question => {
        question.addEventListener('click', function() {
            const answer = this.nextElementSibling;
            const icon = this.querySelector('.faq-icon');
            
            // Toggle answer
            if (answer.style.display === 'block') {
                answer.style.display = 'none';
                icon.classList.remove('fa-minus');
                icon.classList.add('fa-plus');
            } else {
                // Close all other answers
                document.querySelectorAll('.faq-answer').forEach(a => a.style.display = 'none');
                document.querySelectorAll('.faq-icon').forEach(i => {
                    i.classList.remove('fa-minus');
                    i.classList.add('fa-plus');
                });
                
                // Open this answer
                answer.style.display = 'block';
                icon.classList.remove('fa-plus');
                icon.classList.add('fa-minus');
            }
        });
    });
}

// Testimonials rating display
function displayRating(rating) {
    let stars = '';
    for (let i = 1; i <= 5; i++) {
        if (i <= rating) {
            stars += '<i class="fas fa-star"></i>';
        } else {
            stars += '<i class="far fa-star"></i>';
        }
    }
    return stars;
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Initialize additional components when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initSearch();
    initFAQ();
});

// Export functions for global use
window.ProfessionalWriters = {
    showNotification,
    calculatePrice,
    formatCurrency,
    selectPackage,
    handleFileUpload,
    displayRating
};
