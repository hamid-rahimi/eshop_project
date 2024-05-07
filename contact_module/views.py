from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic.edit import FormView
from django.urls import reverse, reverse_lazy
from . import models, forms

class ContactUsFormView(FormView):
    form_class = forms.ContactUsModelForm
    message = None
    success_url = None
    template_name = "contact_module/contact-us-page.html"
    
    def form_valid(self, form):
        self.message = form.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        self.success_url = reverse_lazy("contact_module:accepted-page", kwargs={'message_id':self.message.id})
        if not self.success_url:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
        return str(self.success_url)  # success_url may be lazy
    

class ContactUsView(View):
    template_name = "contact_module/contact-us-page.html"
    context = {'form':forms.ContactUsModelForm()}
     
    def get(self, request):
        return render(request, self.template_name, self.context)
           
    def post(self, request):
        contact_form = forms.ContactUsModelForm(request.POST)
        print(contact_form.is_valid())
        if contact_form.is_valid():
            contact_record = models.ContactUs.objects.create(**contact_form.cleaned_data)
            return redirect("contact_module:accepted_page", contact_record.id)
        
        return render(request, self.template_name, {'form':contact_form})
    

def contact_us(request):
    if request.method=='POST':
        contact = forms.ContactUsForm(request.POST)
        if contact.is_valid():
            contact_record = dict(
                title = contact.cleaned_data.get('title'),
                email = contact.cleaned_data['email'],
                fullname = contact.cleaned_data['fullname'],
                message = contact.cleaned_data.get('message')
            )
            print(contact_record)
            sent_message = models.ContactUs.objects.create(**contact_record)
            print(sent_message)
            return redirect("contact_module:accepted_page", sent_message.pk)
    else:
        contact = forms.ContactUsForm()
    return render(request, "contact_module/contact-us-page.html", {'form': contact})
    
def accepted_page(request, message_id):
    message = get_object_or_404(models.ContactUs, id=message_id)
    return render(request, "contact_module/accepted-page.html", {
        'message': message,
    })