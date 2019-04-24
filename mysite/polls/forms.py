from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from polls.models import Poll, Question, Choice

def validate_even(value):
    if value % 2 != 0:
        raise ValidationError('%(value)s ไม่ใช่เลขคู่', params={'value': value})

class PollForm(forms.Form):
    title = forms.CharField(label="ชื่อโพล", max_length=100, required=True)
    email = forms.CharField(validators=[validators.validate_email])
    no_question = forms.IntegerField(label="จำนวนคำถาม", min_value=0, max_value=10, required=True, validators=[validate_even])
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)

    def clean_title(self):
        data = self.cleaned_data['title']
        if "ไอทีหมีแพนด้า" not in data:
            raise forms.ValidationError("คุณลืมชื่อคณะ")
        return data

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')

        if start and not end:
            #raise forms.ValidationError('โปรดเลือกวันที่สิ้นสุด')
            self.add_error('end_date', 'โปรดเลือกวันที่สิ้นสุด')
        elif end and not start:
            #raise forms.ValidationError('โปรดเลือกวันที่เริ่มต้น')
            self.add_error('start_date', 'โปรดเลือกวันที่เริ่มต้น')

class CommentForm(forms.Form):
    title = forms.CharField(max_length=100)
    body = forms.CharField(max_length=500, widget=forms.Textarea)
    email = forms.EmailField(required=False)
    tel = forms.CharField(max_length=10, required=False)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        tel = cleaned_data.get('tel')

        if not email and not tel:
            raise forms.ValidationError('ต้องกรอก email หรือ Mobile Number')
            #self.add_error('end_date', 'โปรดเลือกวันที่สิ้นสุด')
        if tel:
            if len(tel) < 10:
                self.add_error('tel', 'หมายเลขโทรศัพท์ต้องเป็น 10 หลักเท่านั้น')

                self.add_error('tel', 'หมายเลขโทรศัพท์ต้องเป็นตัวเลขเท่านั้น')

class ChangePasswordForm(forms.Form):
    def __init__(self, *arg, **kwargs):
        self.user = kwargs.pop("user")
        super(ChangePasswordForm, self).__init__(*arg, **kwargs)

    old_pw = forms.CharField(label='รหัสผ่านเก่า', widget=forms.PasswordInput)
    new_pw = forms.CharField(label='รหัสผ่านใหม่', min_length=8, widget=forms.PasswordInput)
    new_pw_chk = forms.CharField(label='ยืนยันรหัสผ่าน', min_length=8, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        old_pw = cleaned_data.get('old_pw')
        new_pw = cleaned_data.get('new_pw')
        new_pw_chk = cleaned_data.get('new_pw_chk')

        if self.user.check_password('{}'.format(old_pw)) == False:
            raise forms.ValidationError('รหัสผ่านผิด')
        if new_pw != new_pw_chk:
            raise forms.ValidationError('รหัสผ่านใหม่ไม่ตรงกัน')

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    lineid = forms.CharField(required=False)
    facebook = forms.CharField(required=False)
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'X'
    GENDERS = (
        (MALE, 'ชาย'),
        (FEMALE, 'หญิง'),
        (OTHER, 'อื่นๆ')
    )
    gender = forms.ChoiceField(choices=GENDERS)
    birthdate = forms.DateField(required=False)

class QuestionForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    type = forms.ChoiceField(choices=Question.TYPES, initial='01')
    question_id = forms.IntegerField(widget=forms.HiddenInput, required=False)

class PollModelForm(forms.ModelForm):
    email = forms.CharField(validators=[validators.validate_email])
    no_question = forms.IntegerField(label="จำนวนคำถาม", min_value=0, max_value=10, required=True)
    class Meta:
        model = Poll
        exclude = ['del_flag']

    def clean_title(self):
        data = self.cleaned_data['title']
        if "ไอทีหมีแพนด้า" not in data:
            raise forms.ValidationError("คุณลืมชื่อคณะ")
        return data

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')

        if start and not end:
            #raise forms.ValidationError('โปรดเลือกวันที่สิ้นสุด')
            self.add_error('end_date', 'โปรดเลือกวันที่สิ้นสุด')
        elif end and not start:
            #raise forms.ValidationError('โปรดเลือกวันที่เริ่มต้น')
            self.add_error('start_date', 'โปรดเลือกวันที่เริ่มต้น')

class ChoiceModelForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = '__all__'
