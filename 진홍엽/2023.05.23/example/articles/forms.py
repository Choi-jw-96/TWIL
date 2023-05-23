from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '제목을 입력해주세요.',
            },
        ),
    )
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                'placeholder': '내용을 입력해주세요',
            },
        ),
    )
    
    image = forms.ImageField(
        widget = forms.ClearableFileInput(
            attrs = {
                'class': 'form-control',
            },
        ),
    )
    class Meta:
        model = Article
        fields = '__all__'
