from django.shortcuts import get_object_or_404, render,redirect
from .models import User
from django.contrib import messages
from employer.models import AddJob
from .models import JobApplication

# Create your views here.
def user_reg(request):
    if request.method=="POST":
        user_name = request.POST.get('name')
        user_email = request.POST.get('email')
        password = request.POST.get('password')
        user_city = request.POST.get('city')
        user_age = request.POST.get('age')
        user_study = request.POST.get('study')

        if user_name and user_email and password:
            if User.objects.filter(user_email=user_email).exists():
                messages.error(request, "Email already registered.")
            else:
                user = User(
                    user_name=user_name,
                    user_email=user_email,
                    user_city=user_city or '',
                    user_age=user_age or 0,
                    user_study=user_study or '',
                )
                user.set_password(password)
                user.save()
                messages.success(request, "Success")
                return redirect('user_log')
    return render(request,'user_reg.html')

def user_log(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(user_email=email)
            if user.check_password(password):
                request.session['user_id'] = user.id
                messages.success(request, f"Welcome {user.user_name}!")
                return redirect('user_dash')
            messages.error(request, "Invalid password.")
        except User.DoesNotExist:
            messages.error(request, "Email not found.")

    return render(request, 'user_log.html')


def user_dash(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "Please login first.")
        return redirect('user_log')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        request.session.pop('user_id', None)
        messages.error(request, "Session expired. Please login again.")
        return redirect('user_log')
    applications = JobApplication.objects.filter(user=user).select_related("job")
    context = {
        "user": user,
        "total_applications": applications.count(),
        "pending": applications.filter(status=JobApplication.STATUS_PENDING).count(),
        "accepted": applications.filter(status=JobApplication.STATUS_APPROVED).count(),
        "applications": applications,
    }
    return render(request, 'user_dash.html', context)

def application(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "Please login first.")
        return redirect('user_log')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        request.session.pop('user_id', None)
        messages.error(request, "Session expired. Please login again.")
        return redirect('user_log')

    jobs = AddJob.objects.filter(is_active=True).order_by("-created_at")

    if request.method == "POST":
        job_id = request.POST.get("job_id")
        job = AddJob.objects.filter(id=job_id, is_active=True).first()
        if not job:
            messages.error(request, "Please select a valid active job.")
            return render(request, 'application.html', {"jobs": jobs, "user": user})

        JobApplication.objects.create(
            user=user,
            job=job,
            full_name=request.POST.get("name", "").strip(),
            email=request.POST.get("email", "").strip(),
            phone=request.POST.get("phone", "").strip(),
            city=request.POST.get("city", "").strip(),
            study=request.POST.get("study", "").strip(),
            skills=request.POST.get("skills", "").strip(),
            resume=request.FILES.get("resume"),
        )
        messages.success(request, "Application submitted successfully.")
        return redirect('user_dash')

    return render(request, 'application.html', {"jobs": jobs, "user": user})
def view_app(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "Please login first.")
        return redirect('user_log')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        request.session.pop('user_id', None)
        messages.error(request, "Session expired. Please login again.")
        return redirect('user_log')

    applications = JobApplication.objects.filter(user=user).select_related("job").order_by("-created_at")
    return render(request, 'view_app.html', {"applications": applications, "user": user})


def delete_application(request, application_id):
    if request.method != "POST":
        return redirect("view_app")

    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "Please login first.")
        return redirect('user_log')

    application = get_object_or_404(JobApplication, id=application_id, user_id=user_id)
    application.delete()
    messages.success(request, "Application deleted successfully.")
    return redirect("view_app")
