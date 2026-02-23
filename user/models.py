from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from employer.models import AddJob

# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField(unique=True)
    password = models.CharField(max_length=256, default='')
    user_age = models.IntegerField()
    user_city = models.CharField(max_length=100)
    user_study = models.CharField(max_length=100)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.user_name


class JobApplication(models.Model):
    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    job = models.ForeignKey(AddJob, on_delete=models.CASCADE, related_name="applications")
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    city = models.CharField(max_length=100)
    study = models.CharField(max_length=150)
    skills = models.TextField()
    resume = models.FileField(upload_to="resumes/")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} -> {self.job.job_title}"

