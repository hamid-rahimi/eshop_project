from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from django.forms.models import model_to_dict
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import login, logout, tokens
from django.utils.crypto import get_random_string
from .models import User, UserProfile
from .forms import (
    RegisterForm, LoginForm, ForgetPasswordForm,
    ResetPasswordForm, EditUserProfileForm, ChangePasswordForm
)
from tools.email_service import SendEmailTools


class RegisterView(View):
    
    def get(self, request:HttpRequest):
        if request.user.is_authenticated:
            return redirect(reverse("home_module:home-page"))
        register_form = RegisterForm()
        return render(request, "account_module/signup.html", {
            'form': register_form
        })

    def post(self, request:HttpRequest):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # print(register_form.cleaned_data)
            email = register_form.cleaned_data['email']
            password_2 = register_form.cleaned_data['password_2']
            
            user:User = User(email=email)
            user.active_code = get_random_string(length=32)
            user.set_password(password_2)
            user.save()
            
            se = SendEmailTools("فعال سازی حساب کاربری",
                                [user.email],
                                {'user':user},
                                "new-email.html")
            if se.send_email():
                return redirect(reverse("account_module:login_page"))
        
        return render(request, "account_module/signup.html", {
            'form': register_form
        })

class ActiveAccountView(View):
    
    def get(self, request:HttpRequest, active_code):
        user:User = User.objects.filter(active_code__iexact=active_code).first()
        if user is not None:
            user.is_active = True
            user.active_code = get_random_string(length=32)
            user.save()
            
            return redirect(reverse("account_module:login_page"))
        else:
            return HttpResponse(content="<h1 class='text-danger text-center'>active code is expired</h1>")

class LoginView(View):
    def get(self, request:HttpRequest):
        if request.user.is_authenticated:
            return redirect(reverse("home_module:home-page"))
        login_form = LoginForm()
        return render(request, "account_module/login.html", {
            'form': login_form
        })
    
    def post(self, request:HttpRequest):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data.get('email')
            password = login_form.cleaned_data.get('password')
            
            user:User = get_object_or_404(User, email=email)
            if user.is_active:
                if user.check_password(password):
                    login(request=request, user=user)
                    return redirect(reverse("home_module:home-page"))
                else:
                    login_form.add_error('password', "password wrong")
            else:
                login_form.add_error('email', "your account is'nt ACTIVE")
        
        return render(request, "account_module/login.html", {
            'form': login_form
        })
        
class LogoutView(View):
    
    def get(self, request:HttpRequest):
        if request.user.is_authenticated:
            logout(request=request)
            return redirect(reverse("home_module:home-page"))
        else:
            return redirect(reverse("account_module:login_page"))

class ForgetPasswordView(View):
    
    def get(self, request:HttpRequest):
        if request.user.is_authenticated:
            return redirect(reverse("home_module:home-page"))
        forget_pass_form = ForgetPasswordForm()
        return render(request, "account_module/forget-pass.html", {
            'form': forget_pass_form
        })
        
    def post(self, request:HttpRequest):
        forget_pass_form = ForgetPasswordForm(request.POST)
        if forget_pass_form.is_valid():
            email = forget_pass_form.cleaned_data.get('email')
            if email:
                user:User = User.objects.filter(email__iexact=email).first()
                if user is not None:
                    # TODO: Send Email with Token and link recovery page.
                    se = SendEmailTools(
                        subject="بازیابی رمز ورود",
                        to= [user.email],
                        context= {'user': user},
                        template_name= "forget-email.html"
                    )
                    if se.send_email():
                        return redirect(reverse("account_module:login_page"))
                else:
                    forget_pass_form.add_error(field='email', error="ایمیل وارد شده یافت نشد")
        return render(request, "account_module/forget-pass.html", {
            'form': forget_pass_form
        })

class ResetPasswordView(View):
    
    def get(self, request:HttpRequest, pass_ok):
        is_pass_ok = User.objects.filter(active_code__iexact=pass_ok).exists()
        if not is_pass_ok:
            return HttpResponse(content="<h1 class='text-danger text-center'>pass code wrong</h1>")
        else:
            reset_pass_form = ResetPasswordForm()
            return render (request, "account_module/reset-pass.html", {
                'form': reset_pass_form
            })
            
    def post(self, request:HttpRequest, pass_ok):
        reset_pass_form = ResetPasswordForm(request.POST)
        if reset_pass_form.is_valid():
            password_2 = reset_pass_form.cleaned_data.get('password_2')
            user:User = get_object_or_404(User, active_code=pass_ok)
            user.set_password(password_2)
            user.is_active = True
            
            CODE = get_random_string(32)
            while User.objects.filter(active_code__iexact=CODE).exists():
                CODE = get_random_string(32)
                
            user.active_code = CODE
            user.save()
            return redirect(reverse("account_module:login_page"))
        return render(request, "account_module/reset-pass.html", {
            'form': reset_pass_form
        })

class ChangePasswordView(View):
    
    def get(self, request: HttpRequest):
        form = ChangePasswordForm()
        return render(request, "account_module/dashboards/change_user_password_panel.html", {
            'form': form,
        })
    
    def post(self, request: HttpRequest):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            current_user: User = User.objects.filter(id=request.user.id).first()
            old_password = form.cleaned_data.get('old_password')
            if current_user.check_password(old_password):
                password = form.cleaned_data.get('password_2')
                current_user.set_password(password)
                current_user.save()
                logout(request)
                return redirect(reverse("account_module:login_page"))
            else:
                form.add_error('old_password', "کلمه عبور اشتباه است.")
        return render(request, "account_module/dashboards/change_user_password_panel.html", {
            'form': form,
        })

class UserPanelDashboardView(TemplateView):
    template_name = "account_module/dashboards/user_panel_dashboard.html"

class EditUserProfileView(View):
    def get(self, request:HttpRequest):
        current_user:User = User.objects.get(id=request.user.id)
        dict_of_model = model_to_dict(instance=current_user.userprofile,
                                      fields=['age', 'address', 'abut_user', 'gender', 'avatar', 'mobile'])
        print("1 => ",dict_of_model)
        dict_of_model.update(model_to_dict(instance=current_user,
                                           fields=['first_name', 'last_name', 'email']))
        print("2 => ",dict_of_model)
        edit_user_profile_form = EditUserProfileForm(initial=dict_of_model)
        context = {
            'form': edit_user_profile_form,
            'fields': dict_of_model,
        }
        return render(request, "account_module/dashboards/edit_user_profile_panel.html", context)
    
    def post(self, request:HttpRequest):
        edit_user_profile_form = EditUserProfileForm(data=request.POST, files=request.FILES)
        if edit_user_profile_form.is_valid():
            print(edit_user_profile_form.cleaned_data)
            first_name = edit_user_profile_form.cleaned_data.get('first_name')
            last_name = edit_user_profile_form.cleaned_data.get('last_name')
            age = edit_user_profile_form.cleaned_data.get('age')
            email = edit_user_profile_form.cleaned_data.get('email')
            mobile = edit_user_profile_form.cleaned_data.get('mobile')
            address = edit_user_profile_form.cleaned_data.get('address')
            gender = edit_user_profile_form.cleaned_data.get('gender')
            abut_user = edit_user_profile_form.cleaned_data.get('abut_user')
            avatar = edit_user_profile_form.cleaned_data.get('avatar')
            
            user:User = User.objects.get(id=request.user.id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            
            user_profile:UserProfile = user.userprofile
            user_profile.age = age
            user_profile.mobile = mobile
            user_profile.address = address
            user_profile.gender = gender
            user_profile.abut_user = abut_user
            if avatar:
                user_profile.avatar = avatar
            user_profile.save()
            
            return redirect(reverse("account_module:user_panel_dashboard_page"))
            
        context = {
            'form': edit_user_profile_form,
        }
        return render(request, "account_module/dashboards/edit_user_profile_panel.html", context)
    
def dashboard_loader_component(request):
    return render(request, "account_module/components/dashboard_render_partial.html")