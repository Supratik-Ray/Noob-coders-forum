from django import forms
from .models import Post, Comment


class CreatePost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body','topic','post_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'title':
                field.widget.attrs.update({'class': 'form-control border-2','placeholder': 'Enter title'})
            elif field_name == 'body':
                field.widget.attrs.update({'class': 'form-control border-2','placeholder': 'Enter the content'})
            elif field_name == 'topic':
                field.widget.attrs.update({'class': 'form-control border-2','placeholder': 'Ex: Python'})
            else:
                field.widget.attrs.update({'class': 'form-control border-2'})

        

class CreateComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control border-2','placeholder': 'your comment','style':"height:100px"})
            

  