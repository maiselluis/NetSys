from django import forms
from .models import (Pc_tablet_server,PcIpAddress,Department,
                     Branch,Switch_router, Email,
                     Printer,CustomUser,Department)

from django.forms import inlineformset_factory
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.forms import PasswordChangeForm



class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar clases Tabler
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})


class PcTabletServerForm(forms.ModelForm):
   
    class Meta:
        model = Pc_tablet_server
        fields = ['department', 'name', 'mac_address', 'any_desk', 'rust_desk', 'remote_desktop']   
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),              
            'mac_address': forms.TextInput(attrs={'class': 'form-control'}),
            'any_desk': forms.TextInput(attrs={'class': 'form-control'}),
            'rust_desk': forms.TextInput(attrs={'class': 'form-control'}),
            'remote_desktop': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }   
        

# FormSet para IPs
PcIpAddressFormSet = inlineformset_factory(
    Pc_tablet_server, PcIpAddress,
    fields=('ip_address',),
    extra=1,  # Cuántos campos extra mostrar
    can_delete=True,
    widgets={
        'ip_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'IP Address'})
    }
)


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name', 'address', 'phone_number', 'email'] 
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }   


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'branch'] 
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'branch': forms.Select(attrs={'class': 'form-control'}),
        } 
        
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        branch = cleaned_data.get('branch')

        if Department.objects.filter(name=name, branch=branch).exists():
            raise forms.ValidationError(
                "This department already exists in this branch."
            )

        return cleaned_data  
    
    
class SwitchRouterForm(forms.ModelForm):
    class Meta:
        model = Switch_router
        fields = ['branch','name', 'ip_address', 'username', 'password', 'mac_address', 'file_settings']   
        widgets = {
            'branch': forms.Select(attrs={'class': 'form-control'}),           
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'ip_address': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'}),
            'mac_address': forms.TextInput(attrs={'class': 'form-control'}),
            'file_settings': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        

class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['department', 'email_address', 'password']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control'}),          
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }       
        



class PrinterForm(forms.ModelForm):
    class Meta:
        model = Printer
        fields = ['department', 'name', 'ip_address', 'username', 'password'] 
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'ip_address': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),   
            'password': forms.TextInput(attrs={'class': 'form-control'}),
        }   
    
    
class CustomUserForm(forms.ModelForm):
    is_active = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    is_staff = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    is_superuser = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select'})
    )

    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select'})
    )

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'department',
            'pictures',
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'pictures': forms.ClearableFileInput(attrs={'class': 'form-control'}),
           
        }

    def save(self, commit=True):
        user = super().save(commit=False)

        # 🔥 PASSWORD SEGURO
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
            self.save_m2m()  # 🔥 guarda groups y permissions

        return user
        
        
class CustomUserUpdateForm(forms.ModelForm):
   
     

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'department',
            'pictures',
           
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'pictures': forms.ClearableFileInput(attrs={'class': 'form-control'}),            
        }
              

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'branch']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'branch': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        branch = cleaned_data.get('branch')

        qs = Department.objects.filter(name=name, branch=branch)

        # 🔥 EXCLUIR EL MISMO OBJETO EN EDIT
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                "This department already exists in this branch."
            )

        return cleaned_data
    

class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }