// static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    // Dark mode toggle
    const themeToggle = document.getElementById('theme-toggle');
    const mobileThemeToggle = document.getElementById('mobile-theme-toggle');
    const html = document.documentElement;
    
    // Check for saved user preference or use system preference
    const savedTheme = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme === 'dark' || (!savedTheme && systemPrefersDark)) {
        html.classList.add('dark');
    }
    
    // Update toggle icons
    updateThemeToggleIcons();
    
    // Theme toggle button
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            html.classList.toggle('dark');
            localStorage.setItem('theme', html.classList.contains('dark') ? 'dark' : 'light');
            updateThemeToggleIcons();
        });
    }
    
    // Mobile theme toggle
    if (mobileThemeToggle) {
        mobileThemeToggle.addEventListener('click', function() {
            html.classList.toggle('dark');
            localStorage.setItem('theme', html.classList.contains('dark') ? 'dark' : 'light');
            updateThemeToggleIcons();
        });
    }
    
    function updateThemeToggleIcons() {
        const isDark = html.classList.contains('dark');
        const darkIcon = document.getElementById('theme-toggle-dark-icon');
        const lightIcon = document.getElementById('theme-toggle-light-icon');
        
        if (darkIcon && lightIcon) {
            darkIcon.classList.toggle('hidden', !isDark);
            lightIcon.classList.toggle('hidden', isDark);
        }
    }
    
    // Mobile menu toggle
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
                
                // Close mobile menu if open
                if (mobileMenu && !mobileMenu.classList.contains('hidden')) {
                    mobileMenu.classList.add('hidden');
                }
            }
        });
    });
    
    // Active nav link highlighting
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.nav-link');
    
    window.addEventListener('scroll', function() {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            
            if (pageYOffset >= sectionTop - 200) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('text-indigo-600', 'dark:text-indigo-400');
            link.classList.add('text-gray-600', 'dark:text-gray-300');
            
            if (link.dataset.section === current) {
                link.classList.remove('text-gray-600', 'dark:text-gray-300');
                link.classList.add('text-indigo-600', 'dark:text-indigo-400');
            }
        });
    });
    
    // Contact form handling
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const submitBtn = document.getElementById('submit-btn');
            const submitText = document.getElementById('submit-text');
            const submitSpinner = document.getElementById('submit-spinner');
            
            // Reset errors
            document.querySelectorAll('[id$="-error"]').forEach(el => {
                el.textContent = '';
                el.classList.add('hidden');
            });
            
            // Show loading state
            submitText.textContent = 'Sending...';
            submitSpinner.classList.remove('hidden');
            submitBtn.disabled = true;
            
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Success - reset form
                    contactForm.reset();
                    window.location.href = "{% url 'contact' %}?success=true";
                } else {
                    // Show errors
                    for (const [field, errors] of Object.entries(data.errors)) {
                        const errorElement = document.getElementById(`${field}-error`);
                        if (errorElement) {
                            errorElement.textContent = errors.join(' ');
                            errorElement.classList.remove('hidden');
                        }
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
            })
            .finally(() => {
                submitText.textContent = 'Send Message';
                submitSpinner.classList.add('hidden');
                submitBtn.disabled = false;
            });
        });
    }
    
    // Initialize animations
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-in-out',
            once: true,
            mirror: false
        });
    }
    
    // Project card hover effects
    document.querySelectorAll('.project-card').forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            card.style.setProperty('--mouse-x', `${x}px`);
            card.style.setProperty('--mouse-y', `${y}px`);
        });
    });
});