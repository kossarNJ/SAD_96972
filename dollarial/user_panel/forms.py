from django import forms

from finance.models import BankPayment, FormPayment, Exchange


class ExchangeForm(forms.ModelForm):
    def make_read_only(self):
        for field in self.fields:
            self.fields[field].widget.attrs['readonly'] = True

    class Meta:
        model = Exchange
        fields = ('currency', 'final_currency', 'final_amount',)


class BankPaymentForm(forms.ModelForm):
    class Meta:
        model = BankPayment
        fields = ('amount', )


class ServicePaymentForm(forms.ModelForm):
    def __init__(self, payment_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for flag, value in payment_type.required_fields:
            for field in FormPayment.flag_related_fields[flag]:
                if value:
                    self.fields[field].required = True
                else:
                    del self.fields[field]
        if payment_type.fixed_price:
            del self.fields['amount']

    def make_read_only(self):
        for field in self.fields:
            self.fields[field].widget.attrs['readonly'] = True

    class Meta:
        model = FormPayment
        fields = (
            'first_name', 'last_name', 'phone_number',
            'security_number', 'passport_number',
            'exam_username', 'exam_password', 'exam_date', 'exam_country', 'exam_city', 'exam_center',
            'university_link', 'university_username', 'university_password',
            'amount',
        )
