from django import forms

class BootstrapModelForm(forms.ModelForm):
    """带有bootstrap样式的 modelform"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field.widget.attrs:
                field.widget.attrs['class'] = "form-control"
                field.widget.attrs['placeholder'] = field.label
            else:
                field.widget.attrs = {"class": "form-control", "placeholder": field.label}

class SuperForm(forms.Form):
    """停车场样式的 form"""
    def __init__(self, my_class, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.my_class = my_class
        for name, field in self.fields.items():
            if field.widget.attrs:
                field.widget.attrs['class'] = self.my_class
                field.widget.attrs['placeholder'] = field.label
            else:
                field.widget.attrs = {"class": self.my_class, "placeholder": field.label}

