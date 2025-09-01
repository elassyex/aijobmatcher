from django.db import models
from django.contrib.auth.models import User

class JobRole(models.Model):
    name = models.CharField(max_length=100)
    required_skills = models.JSONField()
    description = models.TextField()
    experience_level = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.JSONField(default=list)
    experience_years = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class AnalysisResult(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    job_role = models.ForeignKey(JobRole, on_delete=models.CASCADE)
    match_percentage = models.FloatField()
    skill_matches = models.JSONField()
    missing_skills = models.JSONField()
    recommendations = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']