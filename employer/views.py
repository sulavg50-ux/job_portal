from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Employer, AddJob
from user.models import JobApplication


def home(request):
    return render(request, 'home.html')


@ensure_csrf_cookie
def register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        age = request.POST.get('age')
        study = request.POST.get('study')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if Employer.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('register')

        employer = Employer(
            name=name,
            age=age,
            study=study,
            email=email,
        )
        employer.set_password(password)
        employer.save()

        messages.success(request, "Registration successful! Please wait for admin approval before login.")
        return redirect('login')

    return render(request, 'emp_reg.html')


@ensure_csrf_cookie
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email') or request.POST.get('username')
        password = request.POST.get('password')

        try:
            employer = Employer.objects.get(email=email)
            if employer.check_password(password):
                if not employer.is_approved:
                    request.session.pop('employer_id', None)
                    messages.error(request, "Admin must approve your account first.")
                    return redirect('login')

                request.session['employer_id'] = employer.id
                messages.success(request, f"Welcome {employer.name}!")
                return redirect('emp_dash')
            messages.error(request, "Invalid password!")
        except Employer.DoesNotExist:
            messages.error(request, "Email not registered!")

    return render(request, 'emp_login.html')


def emp_dash(request):
    employer_id = request.session.get('employer_id')
    if not employer_id:
        messages.error(request, "Please login first.")
        return redirect('login')

    try:
        employer = Employer.objects.get(id=employer_id)
    except Employer.DoesNotExist:
        request.session.pop('employer_id', None)
        messages.error(request, "Please login again.")
        return redirect('login')

    if not employer.is_approved:
        request.session.pop('employer_id', None)
        messages.error(request, "Admin must approve your account first.")
        return redirect('login')

    jobs = AddJob.objects.filter(employer=employer).order_by("-created_at")
    applications = JobApplication.objects.filter(job__employer=employer).select_related("job", "user").order_by("-created_at")
    recent_jobs = jobs[:10]
    total_jobs = jobs.count()
    active_jobs = jobs.filter(is_active=True).count()

    context = {
        "employer": employer,
        "jobs": recent_jobs,
        "total_jobs": total_jobs,
        "active_jobs": active_jobs,
        "total_applicants": applications.count(),
        "applications": applications[:20],
    }
    return render(request, "emp_dash.html", context)


def update_application_status(request, application_id, action):
    if request.method != "POST":
        return redirect("emp_dash")

    employer_id = request.session.get("employer_id")
    if not employer_id:
        messages.error(request, "Please login first.")
        return redirect("login")

    employer = get_object_or_404(Employer, id=employer_id)
    application = get_object_or_404(
        JobApplication.objects.select_related("job"),
        id=application_id,
        job__employer=employer,
    )

    if action == "approve":
        application.status = JobApplication.STATUS_APPROVED
        message = "Application approved."
    elif action == "reject":
        application.status = JobApplication.STATUS_REJECTED
        message = "Application rejected."
    else:
        messages.error(request, "Invalid action.")
        return redirect("emp_dash")

    application.save(update_fields=["status"])
    messages.success(request, message)
    return redirect("emp_dash")

@ensure_csrf_cookie
def add_job(request):
    employer_id = request.session.get('employer_id')
    if not employer_id:
        messages.error(request, "Please login first.")
        return redirect('login')

    try:
        employer = Employer.objects.get(id=employer_id)
    except Employer.DoesNotExist:
        request.session.pop('employer_id', None)
        messages.error(request, "Please login again.")
        return redirect('login')

    if not employer.is_approved:
        request.session.pop('employer_id', None)
        messages.error(request, "Admin must approve your account first.")
        return redirect('login')

    if request.method == "POST":
        AddJob.objects.create(
            employer=employer,
            job_title=request.POST.get("job_title", "").strip(),
            company_name=request.POST.get("company_name", "").strip(),
            job_image=request.FILES.get("job_image"),
            location=request.POST.get("location", "").strip(),
            job_description=request.POST.get("description", "").strip(),
            salary=request.POST.get("salary", "").strip(),
        )
        messages.success(request, "Job posted successfully.")
        return redirect("emp_dash")
    

    
    return render(request, "add_job.html", {"employer": employer})
 
def emp_job(request):
    employer_id = request.session.get('employer_id')
    if not employer_id:
        messages.error(request, "Please login first.")
        return redirect('login')
    try:
        employer = Employer.objects.get(id=employer_id)
    except Employer.DoesNotExist:
        request.session.pop('employer_id', None)
        messages.error(request, "Please login again.")
        return redirect('login')

    if not employer.is_approved:
        request.session.pop('employer_id', None)
        messages.error(request, "Admin must approve your account first.")
        return redirect('login')

    jobs = AddJob.objects.filter(employer=employer).order_by('-created_at')
    return render(request, 'emp_job.html', {'jobs': jobs, 'employer': employer})

@ensure_csrf_cookie
def edit(request, job_id):
    employer_id = request.session.get("employer_id")
    if not employer_id:
        messages.error(request, "Please login first.")
        return redirect("login")

    employer = get_object_or_404(Employer, id=employer_id)
    if not employer.is_approved:
        request.session.pop("employer_id", None)
        messages.error(request, "Admin must approve your account first.")
        return redirect("login")

    job = get_object_or_404(AddJob, id=job_id, employer=employer)

    if request.method == "POST":
        job.job_title = request.POST.get("job_title", "").strip()
        job.company_name = request.POST.get("company_name", "").strip()
        job.location = request.POST.get("location", "").strip()
        job.salary = request.POST.get("salary", "").strip()
        job.job_description = request.POST.get("job_description", "").strip()
        job.is_active = request.POST.get("is_active") == "on"

        new_image = request.FILES.get("job_image")
        if new_image:
            job.job_image = new_image

        job.save()
        messages.success(request, "Job updated successfully.")
        return redirect("emp_job")

    return render(request, "edit.html", {"job": job, "employer": employer})

def delete(request, job_id):
    employer_id = request.session.get("employer_id")
    if not employer_id:
        messages.error(request, "Please login first.")
        return redirect("login")

    employer = get_object_or_404(Employer, id=employer_id)
    job = get_object_or_404(AddJob, id=job_id, employer=employer)
    job.delete()
    messages.success(request, "Job deleted successfully.")
    return redirect("emp_job")
