from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.contrib import messages

from .models import Project, Experience, Skill
from .forms import ContactForm

class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'featured_projects': Project.objects.filter(featured=True).order_by('order')[:3],
            'meta_title': 'Professional Portfolio | Your Name',
            'meta_description': 'Welcome to my professional portfolio showcasing my work and skills.',
        })
        return context


class AboutView(TemplateView):
    template_name = 'about.html'
    
    skill1=Skill()
    skill1.name = 'Python'
    skill1.type = 'Programming Language'
    skill1.proficiency='Intermediate'
    skill1.order=0


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'skills': Skill.objects.all().order_by('order'),
            'meta_title': 'About Me | Your Name',
            'meta_description': 'Learn more about my professional background and technical skills.',
        })
        return context


class ProjectsView(TemplateView):
    template_name = 'projects.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'projects': Project.objects.all().order_by('order'),
            'meta_title': 'My Projects | Your Name',
            'meta_description': 'Explore my portfolio of professional and personal projects.',
        })
        return context


class ResumeView(TemplateView):
    template_name = 'resume.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'work_experiences': Experience.objects.filter(type='WORK').order_by('-end_date'),
            'educations': Experience.objects.filter(type='EDU').order_by('-end_date'),
            'meta_title': 'My Resume | Your Name',
            'meta_description': 'View my professional work experience and education history.',
        })
        return context


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Send email to admin
            send_mail(
                f"Portfolio Contact: {subject}",
                f"From: {name} <{email}>\n\n{message}",
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            
            # Send confirmation to user
            send_mail(
                "Thank you for your message",
                render_to_string('emails/contact_confirmation.txt', {'name': name}),
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'meta_title': 'Contact Me | Your Name',
        'meta_description': 'Get in touch with me for professional opportunities or collaborations.',
    }
    return render(request, 'contact.html', context)


def custom_404(request, exception):
    context = {
        'meta_title': 'Page Not Found',
        'error_code': 404,
        'error_message': 'The page you are looking for might have been removed or is temporarily unavailable.'
    }
    return render(request, 'errors/404.html', context, status=404)


def custom_500(request):
    context = {
        'meta_title': 'Server Error',
        'error_code': 500,
        'error_message': 'We encountered an unexpected error. Our team has been notified.'
    }
    return render(request, 'errors/500.html', context, status=500)


def project_detail(request, slug):
    try:
        project = Project.objects.get(slug=slug)
        context = {
            'project': project,
            'meta_title': f"{project.title} | Your Name",
            'meta_description': project.short_description,
            'meta_image': project.image.url if project.image else None,
        }
        return render(request, 'projects/detail.html', context)
    except Project.DoesNotExist:
        return custom_404(request, None)


def resume_pdf_view(request):
    # Serve PDF resume for download
    file_path = os.path.join(settings.MEDIA_ROOT, 'resume.pdf')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="YourName_Resume.pdf"'
            return response
    return custom_404(request, None)


# API Views (if needed)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProjectSerializer

@api_view(['GET'])
def api_projects(request):
    projects = Project.objects.all().order_by('order')
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)