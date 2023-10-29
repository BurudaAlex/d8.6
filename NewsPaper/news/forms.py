from django import forms
from .models import Post
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'author',
            'category',
            'title',
            'text',
        ]
    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        if text is not None and len(text) < 20:
            raise ValidationError({
                "text": "記述は20字以下入力が出来ません。"
            })

        title = cleaned_data.get("title")
        if title == text:
            raise ValidationError(
                "タイトルは記述と同一であってはなりません。"
            )

        return cleaned_data
