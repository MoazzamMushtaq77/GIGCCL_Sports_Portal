from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Player
from sports_base.models import Sport
import re
from django.contrib.auth import authenticate

class PlayerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, label="First Name", widget=forms.TextInput(attrs={'placeholder': 'Enter First Name'}))
    last_name = forms.CharField(max_length=50, required=False, label="Last Name", widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name'}))
    cnic = forms.CharField(max_length=15, required=True, label="CNIC", widget=forms.TextInput(attrs={'placeholder': '12345-1234567-1'}))
    email = forms.EmailField(required=True, label="Email", widget=forms.EmailInput(attrs={'placeholder': 'Enter Email'}))
    phone_number = forms.CharField(max_length=12, required=True, label="Phone Number", widget=forms.TextInput(attrs={'placeholder': '1234-1234567'}))
    profile_picture = forms.ImageField(required=False, label="Profile Picture")
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}), label="Confirm Password")
    father_name = forms.CharField(max_length=100, required=True, label="Father Name", widget=forms.TextInput(attrs={'placeholder': 'Enter Father Name'}))
    father_cnic = forms.CharField(max_length=15, required=True, label="Father CNIC", widget=forms.TextInput(attrs={'placeholder': '12345-1234567-1'}))
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Select Date of Birth'}), required=True, label="Date of Birth")
    whatsapp_number = forms.CharField(max_length=15, required=True, label="WhatsApp Number", widget=forms.TextInput(attrs={'placeholder': '+92 3000000000'}))
    province = forms.CharField(max_length=100, required=True, label="Province", widget=forms.TextInput(attrs={'placeholder': 'Select Province'}))
    city = forms.CharField(max_length=100, required=True, label="City", widget=forms.TextInput(attrs={'placeholder': 'Select City'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter Address', 'rows': '3'}), required=True, label="Address")
    sport = forms.ModelChoiceField(queryset=Sport.objects.all(), required=True, label="Sport", empty_label="Select Sport")
    height = forms.FloatField(required=True, label="Height (ft)", widget=forms.NumberInput(attrs={'placeholder': 'Enter Height', 'step': '0.01', 'min': '3.00', 'max': '8.00'}))
    weight = forms.FloatField(required=True, label="Weight (kg)", widget=forms.NumberInput(attrs={'placeholder': 'Enter Weight', 'step': '0.1', 'min': '30.0', 'max': '150.0'}))
    college_roll_no = forms.CharField(max_length=50, required=True, label="College Roll No", widget=forms.TextInput(attrs={'placeholder': 'Enter College Roll No'}))
    blood_group = forms.ChoiceField(choices=[('', 'Select Blood Group')] + Player.BLOOD_GROUP_CHOICES, required=True, label="Blood Group")
    disability = forms.ChoiceField(choices=[('', 'Select Disability')] + Player.DISABILITY_CHOICES, required=False, label="Disability")
    disability_detail = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter Disability Detail', 'rows': '3'}), required=False, label="Disability Detail")

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'cnic', 'email', 'phone_number', 'profile_picture',
            'password1', 'confirm_password'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password2' in self.fields:
            del self.fields['password2']
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if field_name in ('disability', 'sport', 'blood_group'):
                field.widget.attrs.update({'class': 'form-select'})
            if field_name in ('address', 'disability_detail'):
                field.widget.attrs.update({'rows': '3'})
            if field_name in ('height', 'weight'):
                field.widget.attrs.update({'class': 'form-control number-input'})

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('confirm_password')
        if password1 and confirm_password and password1 != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")
        
        cnic = cleaned_data.get('cnic')
        if cnic and not cnic_pattern.match(cnic):
            self.add_error('cnic', "CNIC must be in the format 12345-1234567-1")
        
        father_cnic = cleaned_data.get('father_cnic')
        if father_cnic and not cnic_pattern.match(father_cnic):
            self.add_error('father_cnic', "Father CNIC must be in the format 12345-1234567-1")
        
        whatsapp_number = cleaned_data.get('whatsapp_number')
        if whatsapp_number and not whatsapp_pattern.match(whatsapp_number.replace(' ', '')):
            self.add_error('whatsapp_number', "WhatsApp number must be in the format +92 3000000000")
        
        disability = cleaned_data.get('disability')
        disability_detail = cleaned_data.get('disability_detail')
        if disability == 'Yes' and not disability_detail:
            self.add_error('disability_detail', "Disability detail is required if disability is selected as Yes")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_player = True
        user.is_coach = False
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            Player.objects.create(
                user=user,
                father_name=self.cleaned_data['father_name'],
                father_cnic=self.cleaned_data['father_cnic'],
                dob=self.cleaned_data['dob'],
                whatsapp_number=self.cleaned_data['whatsapp_number'],
                province=self.cleaned_data['province'],
                city=self.cleaned_data['city'],
                address=self.cleaned_data['address'],
                sport=self.cleaned_data['sport'],
                height=self.cleaned_data['height'],
                weight=self.cleaned_data['weight'],
                college_roll_no=self.cleaned_data['college_roll_no'],
                blood_group=self.cleaned_data['blood_group'],
                disability=self.cleaned_data.get('disability', ''),
                disability_detail=self.cleaned_data.get('disability_detail', '')
            )
        return user

cnic_pattern = re.compile(r'^\d{5}-\d{7}-\d$')
whatsapp_pattern = re.compile(r'^\+923\d{9}$')

class PlayerLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter Email', 'class': 'form-control'}),
        label="Email",
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'class': 'form-control'}),
        label="Password",
        required=True
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if not self.user_cache:
                raise forms.ValidationError("Invalid email or password.")
        return cleaned_data

    def get_user(self):
        return self.user_cache

class PlayerProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, label="Name")
    father_name = forms.CharField(max_length=100, required=True, label="Father Name")
    cnic = forms.CharField(max_length=15, required=True, label="CNIC")
    dob = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}), label="Date of Birth")
    phone_number = forms.CharField(max_length=12, required=True, label="Phone")
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': '3'}), required=True, label="Address")
    profile_picture = forms.ImageField(required=False, label="Profile Picture")

    class Meta:
        model = CustomUser
        fields = ['first_name', 'cnic', 'phone_number', 'profile_picture']

    def __init__(self, *args, **kwargs):
        self.player_instance = kwargs.pop('player_instance', None)
        super().__init__(*args, **kwargs)
        if self.player_instance:
            self.fields['father_name'].initial = self.player_instance.father_name
            self.fields['dob'].initial = self.player_instance.dob
            self.fields['address'].initial = self.player_instance.address
            self.fields['cnic'].initial = self.instance.cnic
            self.fields['phone_number'].initial = self.instance.phone_number
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if field_name == 'address':
                field.widget.attrs.update({'rows': '3'})
            if field_name == 'cnic':
                field.widget.attrs.update({'maxlength': '15'})
            if field_name == 'phone_number':
                field.widget.attrs.update({'maxlength': '12'})

    def clean(self):
        cleaned_data = super().clean()
        cnic = cleaned_data.get('cnic')
        if cnic:
            # Normalize CNIC by removing non-digits and reformatting
            cnic_clean = re.sub(r'\D', '', cnic)
            if len(cnic_clean) != 13:
                self.add_error('cnic', "CNIC must contain exactly 13 digits")
            else:
                # Reformat to 12345-1234567-1
                cleaned_data['cnic'] = f"{cnic_clean[:5]}-{cnic_clean[5:12]}-{cnic_clean[12]}"
        
        phone_number = cleaned_data.get('phone_number')
        if phone_number:
            # Normalize phone number by removing non-digits and reformatting
            phone_clean = re.sub(r'\D', '', phone_number)
            if len(phone_clean) != 11:
                self.add_error('phone_number', "Phone number must contain exactly 11 digits")
            else:
                # Reformat to 1234-1234567
                cleaned_data['phone_number'] = f"{phone_clean[:4]}-{phone_clean[4:]}"
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.cnic = self.cleaned_data['cnic']
            user.phone_number = self.cleaned_data['phone_number']
            user.first_name = self.cleaned_data['first_name']
            if 'profile_picture' in self.cleaned_data and self.cleaned_data['profile_picture']:
                user.profile_picture = self.cleaned_data['profile_picture']
            elif self.data.get('profile_picture_clear'):
                user.profile_picture = None
            user.save()
            if self.player_instance:
                self.player_instance.father_name = self.cleaned_data['father_name']
                self.player_instance.dob = self.cleaned_data['dob']
                self.player_instance.address = self.cleaned_data['address']
                self.player_instance.save()
        return user

class PlayerChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Old Password'}), label="Old Password")
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter New Password'}), label="New Password")
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'}), label="Confirm New Password")

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')

        if old_password and not self.user.check_password(old_password):
            self.add_error('old_password', "Old password is incorrect.")

        if new_password and confirm_new_password and new_password != confirm_new_password:
            self.add_error('confirm_new_password', "New passwords do not match.")

        if new_password and len(new_password) < 6:
            self.add_error('new_password', "New password must be at least 6 characters.")

        return cleaned_data