from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("employer", "0003_employer_is_approved"),
    ]

    operations = [
        migrations.CreateModel(
            name="AddJob",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("job_title", models.CharField(max_length=150)),
                ("company_name", models.CharField(max_length=150)),
                ("location", models.CharField(max_length=150)),
                ("job_description", models.TextField()),
                ("salary", models.CharField(blank=True, max_length=100)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "employer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="jobs",
                        to="employer.employer",
                    ),
                ),
            ],
        ),
    ]
