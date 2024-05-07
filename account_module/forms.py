from django import forms
from django.core import validators
from django.contrib.auth import password_validation
from .models import User


class RegisterForm(forms.Form):
    email = forms.CharField(label="ایمییل", max_length=120, required=True,
                            validators=[validators.EmailValidator(),
                                validators.MaxLengthValidator(120),
                            ], 
                            widget=forms.EmailInput(
                                attrs={'placeholder':"Email", 'class':"rtl"}
                            ))
    password_1 = forms.CharField(label="رمـز عبـور", max_length=150, required=True,
                                    widget=forms.PasswordInput(
                                     attrs={'placeholder':"password"}
                                 ))
    password_2 = forms.CharField(label="تکرار رمـز عبـور", max_length=150, required=True,
                                 widget=forms.PasswordInput(
                                     attrs={'placeholder':"confirm password"}
                                 ))

    def clean(self):
        email = self.cleaned_data.get('email')
        if email:
            is_email:bool = User.objects.filter(email__iexact=email).exists()
            if is_email:
                self.add_error('email', "This Email is Exist !!!")
            
        pass_1 = self.cleaned_data.get('password_1')
        pass_2 = self.cleaned_data.get('password_2')
        if pass_1 and pass_2:
            if (pass_1 != pass_2):
                self.add_error('password_2', "password don't match !!!")
            else:
                password_validation.validate_password(password=pass_2, user=email)
            
        return self.cleaned_data
    
class LoginForm(forms.Form):
    email = forms.CharField(label="ایمییل", max_length=120, required=True,
                            validators=[validators.EmailValidator(),
                                validators.MaxLengthValidator(120),
                            ], 
                            widget=forms.EmailInput(
                                attrs={'placeholder':"Email", 'class':"rtl"}
                            ))
    password = forms.CharField(label="رمـز عبـور", max_length=150, required=True,
                                    widget=forms.PasswordInput(
                                     attrs={'placeholder':"password"}
                                 ))
    
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        
        if email and password:
            is_exists = User.objects.filter(email__iexact=email).exists()
            if not is_exists:
                self.add_error('email', "email not exists")
        return self.cleaned_data

class ForgetPasswordForm(forms.Form):
    email = forms.CharField(
        max_length=120,
        required=True,
        label="آدرس ایمیل",
        validators=[validators.EmailValidator()],
        widget=forms.EmailInput(attrs={
            'placeholder':"Email"
        }))
    
class ResetPasswordForm(forms.Form):
    password_1 = forms.CharField(label="رمز عبور", max_length=150, required=True,
                                widget=forms.PasswordInput(attrs={
                                        'placeholder':"Password" }))
    password_2 = forms.CharField(label="تکرار رمز عبور", max_length=150, required=True,
                                widget=forms.PasswordInput(attrs={
                                        'placeholder':"Confirm Password" }))
    
    def clean(self):
        pass_1 = self.cleaned_data.get('password_1')
        pass_2 = self.cleaned_data.get('password_2')
        if pass_1 and pass_2:
            if (pass_1 != pass_2):
                self.add_error('password_2', "password don't match !!!")
            else:
                password_validation.validate_password(password=pass_2)
            
        return self.cleaned_data

class EditUserProfileForm(forms.Form):
    first_name = forms.CharField(label="نام", max_length=120, required=False,
                                widget=forms.TextInput(attrs={
                                        'placeholder':"First Name", 'class': "form-control"}))
    last_name = forms.CharField(label="نام خانوادگی", max_length=120, required=False,
                                widget=forms.TextInput(attrs={
                                        'placeholder':"Last Name", 'class': "form-control" }))
    age = forms.IntegerField(label="سن", required=False,widget=forms.NumberInput(attrs={
                                        'placeholder':"Age", 'class': "form-control" }))
    email = forms.EmailField(max_length=300, widget=forms.EmailInput(attrs={
                                        'placeholder':"Email", 'class': "form-control" }))
    mobile = forms.CharField(label="شماره موبایل", max_length=120, required=False,
                                widget=forms.TextInput(attrs={
                                        'placeholder':"mobile", 'class': "form-control" }))
    address = forms.CharField(label="آدرس", max_length=420, required=False,
                                widget=forms.TextInput(attrs={
                                        'placeholder':"Address", 'class': "form-control" }))
    gender = forms.ChoiceField(label="جنسیت", required=False, choices=[(1, 'مرد'), (0, 'زن')],
                               widget=forms.RadioSelect(attrs={'placeholder':"Gender", 'class': " radio" }))
    avatar = forms.ImageField(label="تصویر", required=False, widget=forms.FileInput(attrs={
                                        'placeholder':"Image", 'class': "form-control" }))
    abut_user = forms.CharField(label="درباره من", required=False, widget=forms.Textarea(attrs={
                                        'placeholder':"Bio", 'class': "form-control" }))

    def clean(self):
        return self.cleaned_data

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=120, required=True, label="کلمه عبور جاری",
                                   widget=forms.PasswordInput(
                                       attrs={'placeholder':"old password", 'class':"form-control"}
                                   ))
    password_1 = forms.CharField(max_length=120, required=True, label="کلمه عبور جدید",
                                 widget=forms.PasswordInput(
                                     attrs={'placeholder':"new password", 'class':"form-control"}
                                 ))
    password_2 = forms.CharField(max_length=120, required=True, label="تکرار کلمه عبور جدید",
                                 widget=forms.PasswordInput(
                                     attrs={'placeholder':"confirm new password", 'class':"form-control"}
                                 ))
    
    def clean(self):
        # current_user: User = User.objects.filter(id=request.user.id).first()
        # old_password = self.cleaned_data.get('old_password')
        # if current_user.check_password(old_password):
        password_1 = self.cleaned_data.get('password_1')
        password_2 = self.cleaned_data.get('password_2')
        if password_1 and password_2 and password_1 == password_2:
            password_validation.validate_password(password_2)
        else:
            self.add_error('password_2', "pass not match")
        return self.cleaned_data