from django import forms


class SettingForm(forms.Form):
    first_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        self.context = kwargs.pop('context', {})
        super(SettingForm, self).__init__(*args, **kwargs)

    def save(self):
        user = self.context['request'].user
        user.first_name = self.cleaned_data.get('first_name')
        user.email = self.cleaned_data.get('email')
        user.save()
        return user