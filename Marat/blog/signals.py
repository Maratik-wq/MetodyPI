from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Comment

@receiver(post_save, sender=Comment)
def send_comment_notification(sender, instance, created, **kwargs):
    if created:  
        subject = f"Новый комментарий на пост \"{instance.post.title}\""
        message = f"""
        Новый комментарий от {instance.author}:
        
        Тема: {instance.subject}
        Текст: {instance.text}
        
        Пост: {instance.post.title}
        Ссылка: {settings.SITE_URL}/post/{instance.post.id}/
        """
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],  # Твоя почта
            fail_silently=False,
        )