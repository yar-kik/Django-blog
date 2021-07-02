from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from .models import Comment, Article


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("title", "text", "category", "related_item")
        widgets = {
            "text": CKEditorUploadingWidget(),
            # 'related_item': autocomplete.ModelSelect2('articles:item_autocomplete')
        }


class SearchForm(forms.Form):
    query = forms.CharField(max_length=50)
