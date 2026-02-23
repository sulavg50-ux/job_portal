from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("employer", "0005_addjob_job_image"),
        ("user", "0002_user_password"),
    ]

    operations = [
        migrations.CreateModel(
            name="JobApplication",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=150)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=30)),
                ("city", models.CharField(max_length=100)),
                ("study", models.CharField(max_length=150)),
                ("skills", models.TextField()),
                ("resume", models.FileField(upload_to="resumes/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("job", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="applications", to="employer.addjob")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="applications", to="user.user")),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
