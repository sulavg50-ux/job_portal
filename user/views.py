from django.shortcuts import render,redirect
from .models import User
from django.contrib import messages

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
    return render(request, 'user_dash.html', {'user': user})

