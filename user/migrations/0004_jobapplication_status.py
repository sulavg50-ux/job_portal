from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0003_jobapplication"),
    ]

    operations = [
        migrations.AddField(
            model_name="jobapplication",
            name="status",
            field=models.CharField(
                choices=[("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")],
                default="pending",
                max_length=20,
            ),
        ),
    ]
