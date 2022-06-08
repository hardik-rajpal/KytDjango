from django import forms
class UploadFileForm(forms.Form):
    data=forms.FileField()
    def clean(self):
        cd = self.cleaned_data
        if(True):
            return cd
