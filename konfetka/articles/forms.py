from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from .models import Comment, Article


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea, label="")

    class Meta:
        model = Comment
        fields = ('body',)


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'text', 'tags')
        widgets = {
            'text': CKEditorUploadingWidget()
        }
