from django import forms


# Форма ввода купона
class CouponApplyForm(forms.Form):
    code = forms.CharField()