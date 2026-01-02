from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_comment_notification(comment):
    subject = f'New comment on your post: {comment.post.title}'
    html_message = render_to_string('blog/emails/comment_notification.html', {
        'comment': comment,
        'post': comment.post
    })
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [comment.post.author.email],
        html_message=html_message
    )

def send_welcome_email(user):
    subject = 'Welcome to Django Blog!'
    html_message = render_to_string('blog/emails/welcome.html', {
        'user': user
    })
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message
    )