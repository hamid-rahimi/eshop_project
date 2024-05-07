from django.core.mail import send_mail
from django.template import loader
from django.utils.html import strip_tags
from django.conf import settings
# import os


class SendEmailTools():
    
    def __init__(self, subject:str, to:list, context:dict, template_name:str):
        
        self.SUBJECT = subject
        self.TO = to
        self.CONTEXT = context
        self.TEMPLATE_NAME = template_name
        
    def send_email(self):
        try:
            # template = loader.get_template(self.TEMPLATE_NAME)
            html_message = loader.render_to_string(self.TEMPLATE_NAME, self.CONTEXT)
            plain_message = strip_tags(html_message)
            from_email = settings.EMAIL_HOST_USER
            is_send_mail = send_mail(
                                    subject=self.SUBJECT,
                                    recipient_list=self.TO,
                                    message=plain_message,
                                    from_email=from_email,
                                    html_message=html_message)
        except Exception as e:
            raise e
        return is_send_mail
        
