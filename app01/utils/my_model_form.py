from django import forms
from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from app01.utils.bootstrap import *
from app01.utils.encrypt import md5

class UserModelForm(forms.ModelForm):
    """用户"""
    name = forms.CharField(min_length=2, label='用户名')   # 重写属性，附加校验设置

    class Meta:
        model = models.UserInfo
        fields = ['name', 'pwd', 'age', 'sal', 'crt_time', 'gender', 'dept']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 循环找到所有的插件，添加"class="
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

class PrettyNumModelForm(forms.ModelForm):
    """靓号"""
    mobile = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'),],
    )

    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']
        #fields = "__all__"  # 默认显示所有字段
        #exclude = ['level']     # 排除特定字段

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_mobile(self):
        """实现更复杂的数据校验"""
        txt_mobile = self.cleaned_data['mobile']

        # pk : primary key
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError('该手机号已存在')

        return txt_mobile

class AdminModelForm(BootstrapModelForm):
    """管理员"""
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = models.Admin
        fields = ['username', 'password']
        widgets = {
            "password": forms.PasswordInput(render_value=True),
        }

    def clean_password(self):
        # 对密码进行md5加密之后返回
        pwd = md5(self.cleaned_data.get('password'))
        return pwd

    def clean_confirm_password(self):
        """校验确认密码是否与前一个输入密码一致"""
        pwd = self.cleaned_data.get('password')
        con_pwd = md5(self.cleaned_data.get('confirm_password'))
        if pwd != con_pwd:
            raise ValidationError("密码不一致!")
        return con_pwd

class AdminResetModelForm(AdminModelForm):
    """管理员重置密码"""
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = models.Admin
        fields = ['password', 'confirm_password']
        widgets = {
            "password": forms.PasswordInput(render_value=True),
        }

    def clean_password(self):
        # 对密码进行md5加密之后返回
        pwd = md5(self.cleaned_data.get('password'))
        exists = models.Admin.objects.filter(id=self.instance.pk, password=pwd).exists()
        if exists:
            raise ValidationError('不能与之前的密码一致！')
        return pwd
    
class LoginForm(SuperForm):
    """用户登录 Form"""
    username = forms.CharField(
        label='USER NAME',
        widget=forms.TextInput,
        required=True,  # 不能为空
        # widget=forms.TextInput(attrs={"class": "e", "placeholder": "USER NAME"}),
    )
    password = forms.CharField(
        label='PASSWORD',
        widget=forms.PasswordInput(render_value=True),
        required=True,  # 不能为空
        # widget=forms.PasswordInput(attrs={"class": "e", "placeholder": "PASSWORD"}),
    )
    code = forms.CharField(
        label='VALIDATION CODE',
        widget=forms.TextInput,
        required=True,  # 不能为空
        # widget=forms.TextInput(attrs={"class": "e", "placeholder": "USER NAME"}),
    )

    def clean_password(self):
        """转化成md5加密"""
        pwd = md5(self.cleaned_data.get('password'))
        return pwd
