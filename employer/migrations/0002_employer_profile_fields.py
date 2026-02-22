from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employer", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="employer",
            name="name",
            field=models.CharField(default="", max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="employer",
            name="age",
            field=models.PositiveIntegerField(default=18),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="employer",
            name="study",
            field=models.CharField(default="", max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="employer",
            name="email",
            field=models.EmailField(default="temp@example.com", max_length=254, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="employer",
            name="password",
            field=models.CharField(max_length=256),
        ),
    ]
