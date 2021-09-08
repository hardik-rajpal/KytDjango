from django import forms
class UploadFileForm(forms.Form):
    username=forms.CharField(max_length=50)
    data=forms.FileField()
    def clean(self):
        cd = self.cleaned_data
        us = cd.get('username')
        if(us=='hardik'):
            return cd
        else:
            raise ValueError("You're not hardik")