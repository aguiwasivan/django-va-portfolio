from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.TextInput(attrs={'tabindex':'-1','autocomplete':'off'}))
    class Meta:
        model = ContactMessage
        fields = ['name','email','subject','message']
        labels = {'name':'Full name','email':'Email address'}
        widgets = {'name':forms.TextInput(attrs={'autocomplete':'name','placeholder':'Your full name'}),'email':forms.EmailInput(attrs={'autocomplete':'email','placeholder':'you@company.com'}),'subject':forms.TextInput(attrs={'placeholder':'How can I help?'}),'message':forms.Textarea(attrs={'rows':6,'placeholder':'Tell me a little about your opportunity…','maxlength':5000})}
    def clean_website(self):
        if self.cleaned_data.get('website'):
            raise forms.ValidationError('Unable to submit this form.')
        return ''
