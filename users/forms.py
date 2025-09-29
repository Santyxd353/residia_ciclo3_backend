from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'national_id', 'phone', 'photo_url', 'role', 'is_active')

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # username se autogenera en models.save() si está vacío
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text="No se muestra. Usa 'Change password' para cambiarla."
    )

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'national_id',
                  'phone', 'photo_url', 'role', 'is_active', 'is_superuser')

    def clean_password(self):
        # no cambiar la contraseña aquí
        return self.initial["password"]
