from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


def send_simple_mail(recipient, subject, template, context):
    from_email = settings.FROM_EMAIL
    recipient_list = [recipient]
    msg_plain = render_to_string('email/{}.txt'.format(template), context)
    msg_html = render_to_string('email/{}.html'.format(template), context)
    send_mail(subject, msg_plain, from_email, recipient_list, html_message=msg_html,)