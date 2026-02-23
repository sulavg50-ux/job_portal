from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("employer", "0004_addjob"),
    ]

    operations = [
        migrations.AddField(
            model_name="addjob",
            name="job_image",
            field=models.FileField(blank=True, null=True, upload_to="job_images/"),
        ),
    ]
