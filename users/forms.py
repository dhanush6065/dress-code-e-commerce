from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User , Address



class RegistrationForm(UserCreationForm):
    field_order = [
    'full_name',
    'email',
    'phone_number',
    'password1',
    'password2',
]

    full_name = forms.CharField(
        max_length=150,
        required=True,
        label="Full Name"
    )

    email = forms.EmailField(
        required=True,
        error_messages={
            'invalid': 'Enter a valid email address.',
        }
    )

    phone_number = forms.CharField(
        max_length=15,
        required=True,
        label="Phone Number"
    )

    class Meta:
        model = User
        fields = ('email', 'phone_number')

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'An account with this email already exists.'
            )

        return email

    def save(self, commit=True):
        user = super().save(commit=False)

        full_name = self.cleaned_data['full_name'].strip()
        name_parts = full_name.split(maxsplit=1)

        user.first_name = name_parts[0]
        user.last_name = name_parts[1] if len(name_parts) > 1 else ''
        user.phone_number = self.cleaned_data['phone_number']

        if commit:
            user.save()

        return user




class ProfileUpdateForm(forms.ModelForm):

    full_name = forms.CharField(
        max_length=150,
        required=True,
        label="Full Name"
    )

    phone_number = forms.CharField(
        max_length=15,
        required=False,
        label="Phone Number"
    )

    class Meta:
        model = User
        fields = ['phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['full_name'].initial = (
                f"{self.instance.first_name} {self.instance.last_name}"
            ).strip()

    def save(self, commit=True):
        user = super().save(commit=False)

        full_name = self.cleaned_data['full_name'].strip()
        name_parts = full_name.split(maxsplit=1)

        user.first_name = name_parts[0] if name_parts else ''
        user.last_name = name_parts[1] if len(name_parts) > 1 else ''

        if commit:
            user.save()

        return user
class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = [
            'full_name',
            'phone',
            'house_name',
            'street',
            'city',
            'state',
            'pincode',
        ]      