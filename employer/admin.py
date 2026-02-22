from django.contrib import admin

from .models import Employer, AddJob


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "study", "email", "is_approved")
    list_editable = ("is_approved",)
    search_fields = ("name", "email", "study")
    list_filter = ("is_approved", "study")
    fields = ("name", "age", "study", "email", "is_approved")

    actions = ("approve_employers", "disapprove_employers")

    @admin.action(description="Approve selected employers")
    def approve_employers(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description="Disapprove selected employers")
    def disapprove_employers(self, request, queryset):
        queryset.update(is_approved=False)


@admin.register(AddJob)
class AddJobAdmin(admin.ModelAdmin):
    list_display = ("job_title", "company_name", "location", "employer", "is_active", "created_at")
    search_fields = ("job_title", "company_name", "location", "employer__name", "employer__email")
    list_filter = ("is_active", "created_at")
