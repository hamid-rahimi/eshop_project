from django import forms
from .models import ContactUs


class ContactUsForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':"عنوان"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':"ایمیل"}))
    fullname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':"نام و نام خانوادگی"}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':"پیغام شما", 'row':8}))

class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        # fields = ''
        # fields = '__all__'
        # fields = forms.ALL_FIELDS
        exclude = ['created_time', 'response', 'response_time', 'is_read_by_admin']
        widgets = {
            'title': forms.TextInput(attrs={
                'class':"form-control",
                'placeholder':"عنوان",
            }),
            'email': forms.EmailInput(attrs={
                'class':"form-control",
                'placeholder':"ایمیل",
            }),
            'fullname': forms.TextInput(attrs={
                'class':"form-control",
                'placeholder':"نام و نام خانوادگی"
            }),
            'message': forms.Textarea(attrs={
                'class':"form-control",
                'id':"message",
                'placeholder':"پیام شما"
            })
        }
        labels = {
            'title':"عنوان",
            'email':"آدرس ایمیل",
            'fullname':"نام و نام خانوادگی",
            'message':"متن پیام"
        }
        error_messages = {
            'title': {'required':"its elzamist"}
        }