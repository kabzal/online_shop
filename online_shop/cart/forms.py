from django import forms

# Диапазон доступного количества товара
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


# Форма добавления в корзину некоторого количества товара
class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int)
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)