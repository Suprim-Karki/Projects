from rest_framework import serializers
from .models import Project, Experience, Skill
from django.urls import reverse

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'type', 'proficiency', 'icon_class', 'order']
        read_only_fields = ['id']

class ExperienceSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()
    is_current = serializers.BooleanField(source='current', read_only=True)
    
    class Meta:
        model = Experience
        fields = [
            'id', 'type', 'title', 'company', 'location', 
            'start_date', 'end_date', 'is_current', 'duration',
            'description', 'order'
        ]
        read_only_fields = ['id', 'duration']
    
    def get_duration(self, obj):
        if obj.current:
            return "Present"
        return f"{obj.start_date.year} - {obj.end_date.year}"

class ProjectImageSerializer(serializers.Field):
    def to_representation(self, value):
        request = self.context.get('request')
        if value and hasattr(value, 'url'):
            return request.build_absolute_uri(value.url)
        return None

class ProjectSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    image = ProjectImageSerializer()
    absolute_url = serializers.SerializerMethodField()
    technologies_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'description', 'short_description',
            'image', 'technologies', 'technologies_list', 'project_url',
            'github_url', 'featured', 'order', 'created_at', 'skills',
            'absolute_url'
        ]
        read_only_fields = ['id', 'created_at', 'slug']
        extra_kwargs = {
            'technologies': {'write_only': True}
        }
    
    def get_absolute_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('project-detail', kwargs={'slug': obj.slug}))
    
    def get_technologies_list(self, obj):
        return obj.technologies.split(',') if obj.technologies else []
    
    def validate_technologies(self, value):
        if not value:
            raise serializers.ValidationError("Technologies field cannot be empty")
        return value
    
    def create(self, validated_data):
        # Custom creation logic if needed
        return Project.objects.create(**validated_data)

class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    subject = serializers.CharField(max_length=100)
    message = serializers.CharField()
    
    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long")
        return value.strip()
    
    def validate_message(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Message must be at least 10 characters long")
        return value.strip()

class ResumeSerializer(serializers.Serializer):
    work_experiences = ExperienceSerializer(many=True)
    educations = ExperienceSerializer(many=True)
    skills = SkillSerializer(many=True)
    
    def to_representation(self, instance):
        return {
            'work_experiences': ExperienceSerializer(
                Experience.objects.filter(type='WORK').order_by('-end_date'),
                many=True
            ).data,
            'educations': ExperienceSerializer(
                Experience.objects.filter(type='EDU').order_by('-end_date'),
                many=True
            ).data,
            'skills': SkillSerializer(
                Skill.objects.all().order_by('order'),
                many=True
            ).data
        }

# API Versioning
class ProjectSerializerV2(ProjectSerializer):
    detailed_description = serializers.CharField(source='description')
    preview_description = serializers.CharField(source='short_description')
    
    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + ['detailed_description', 'preview_description']
        extra_kwargs = {
            'description': {'write_only': True},
            'short_description': {'write_only': True}
        }