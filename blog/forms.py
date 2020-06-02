from django import forms
from crispy_forms.helper import FormHelper

from .models import Comment

'''
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)'''


"""class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    Send_to = forms.EmailField()
    subject = forms.CharField(max_length=45)
    comments = forms.CharField(required=False, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(EmailPostForm, self).__init__(*args, **kwargs)

"""


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('comment',)


class SearchForm(forms.Form):
    query = forms.CharField()
  
