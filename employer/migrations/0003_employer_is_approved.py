from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employer", "0002_employer_profile_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="employer",
            name="is_approved",
            field=models.BooleanField(default=False),
        ),
    ]
