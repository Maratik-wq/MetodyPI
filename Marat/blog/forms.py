# forms.py
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'text']  # author теперь берётся из request.user
        labels = {
            'subject': _('Тема комментария'),
            'text': _('Текст комментария'),
        }
        widgets = {
            'subject': forms.TextInput(attrs={
                'placeholder': _('Тема (обязательно)'),
                'class': 'form-input'
            }),
            'text': forms.Textarea(attrs={
                'placeholder': _('Ваш комментарий...'),
                'rows': 5,
                'class': 'form-textarea'
            }),
        }

    def clean_subject(self):
        subject = self.cleaned_data.get('subject', '').strip()
        if not subject:
            raise forms.ValidationError(_("Тема комментария обязательна."))
        return subject

    def clean_text(self):
        text = self.cleaned_data.get('text', '').strip()
        if not text:
            raise forms.ValidationError(_("Текст комментария не может быть пустым."))
        return text