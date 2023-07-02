from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'content',
        ]

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("content")
        if content is not None and len(content) < 20:
            raise ValidationError({
                "content": "Описание не может быть менее 20 символов."
            })

        title = cleaned_data.get("title")
        if title == content:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data


class NewsForm(PostForm):
    pass


class ArticleForm(PostForm):
    pass

