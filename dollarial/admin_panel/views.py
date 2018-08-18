from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView

from dollarial.currency import Currency
from dollarial.mixins import ClerkRequiredMixin, StaffRequiredMixin
from dollarial.models import User, Clerk, get_dollarial_company, get_dollarial_user, PaymentType

from django.views.generic import FormView
from django.shortcuts import render, redirect

from . import forms
from admin_panel.forms import BankPaymentForm, SendNotificationForm

import requests


def transaction_list(request):
    # TODO: read from db
    data = {
        "transactions": [
            {
                "id": "1",
                "transaction_type": "Toefl",
                "amount": "200",
                "currency": "$",
                "owner": "user1",
                "destination": "Toefl Co.",
                "status": "reject"
            },
            {
                "id": "2",
                "transaction_type": "Gaj",
                "amount": "20000000000",
                "currency": "﷼",
                "owner": "user2",
                "destination": "Gaj Co.",
                "status": "unknown"
            },
            {
                "id": "3",
                "transaction_type": "IELTS",
                "amount": "100",
                "currency": "€",
                "owner": "user1",
                "destination": "Soroush Co.",
                "status": "accept"
            },
            {
                "id": "4",
                "transaction_type": "Toefl",
                "amount": "200",
                "currency": "$",
                "owner": "user2",
                "destination": "Toefl Co.",
                "status": "reject"
            },
        ]
    }
    return render(request, 'admin_panel/admin_transaction_list.html', data)


def transaction_view(request, transaction_id):
    data = {
        "transaction": {
            "id": transaction_id,
            "transaction_type": "Toefl",
            "amount": "200",
            "currency": "$",
            "owner": "user1",
            "destination": "Toefl Co.",
            "status": "reject"
        }
    }
    return render(request, 'admin_panel/admin_transaction_view.html', data)


class UserList(ClerkRequiredMixin, ListView):
    model = User
    template_name = 'admin_panel/admin_costumer_list.html'


class UserUpdate(ClerkRequiredMixin, UpdateView):
    model = User
    template_name = 'admin_panel/admin_costumer_view.html'
    fields = ['username', 'first_name', 'last_name', 'account_number', 'email', 'phone_number',
              'is_active', 'is_staff']
    success_url = reverse_lazy('admin_costumer_list')


class ClerkList(StaffRequiredMixin, ListView):
    model = Clerk
    template_name = 'admin_panel/admin_reviewer_list.html'


class ClerkAdd(StaffRequiredMixin, CreateView):
    model = Clerk
    template_name = 'admin_panel/admin_reviewer_add.html'
    success_url = reverse_lazy('admin_reviewer_list')
    form_class = forms.ClerkCreateForm


class ClerkUpdate(StaffRequiredMixin, UpdateView):
    model = Clerk
    template_name = 'admin_panel/admin_reviewer_view.html'
    success_url = reverse_lazy('admin_reviewer_list')
    form_class = forms.ClerkUpdateForm


class PaymentTypeAdd(StaffRequiredMixin, CreateView):
    model = PaymentType
    template_name = 'admin_panel/admin_transaction_type_add.html'
    success_url = reverse_lazy('admin_transaction_type_list')
    form_class = forms.PaymentTypeGeneralForm


class PaymentTypeList(StaffRequiredMixin, ListView):
    model = PaymentType
    template_name = 'admin_panel/admin_transaction_type_list.html'


class PaymentTypeView(StaffRequiredMixin, UpdateView):
    model = PaymentType
    template_name = 'admin_panel/admin_transaction_type_view.html'
    success_url = reverse_lazy('admin_transaction_type_list')
    form_class = forms.PaymentTypeGeneralForm


def skipped_transaction_list(request):
    # TODO: read from db
    data = {
        "skipped_items": [
            {
                "id": "1",
                "reviewer_id": "2",
                "reviewer_username": "soroush",
                "transaction_id": "10",
                "time": "01/01/99"
            },
            {
                "id": "2",
                "reviewer_id": "1",
                "reviewer_username": "parand",
                "transaction_id": "9",
                "time": "01/01/99"
            }
        ]
    }
    return render(request, 'admin_panel/admin_skipped_transaction_list.html', data)


def reviewed_transaction_history(request):
    # TODO: read from db
    data = {
        "reviewed_items": [
            {
                "id": "1",
                "reviewer_id": "2",
                "reviewer_username": "soroush",
                "transaction_id": "10",
                "time": "01/01/99",
                "status": "reject"
            },
            {
                "id": "2",
                "reviewer_id": "1",
                "reviewer_username": "parand",
                "transaction_id": "9",
                "time": "01/01/99",
                "status": "accept"
            }
        ]
    }
    return render(request, 'admin_panel/admin_reviewed_transaction_history.html', data)


def reports_list(request):
    data = {
        "reports": [
            {
                "id": 1,
                "transaction_id": 10,
                "reporter_id": 100,
                "message": "salam modir\n khubi?\nchakeram\nin yaru ekhtelas karde 3000 milion dollar\n"
                           "bebandesh damet garm\n"
            },
            {
                "id": 2,
                "transaction_id": 11,
                "reporter_id": 101,
                "message": "salam modir\nkhubi?\nchakeram\nin yaru ekhtelas karde 3000 milion dollar\n"
                           "bebandesh damet garm\n"
            }
        ]
    }
    return render(request, 'admin_panel/admin_reports_list.html', data)


# TODO login required
def send_notification(request):
    if request.method == 'GET':
        form = SendNotificationForm()
    else:
        form = SendNotificationForm(request.POST)
        if "cancel" in request.POST:
            return redirect('admin_index')
        else:
            if form.is_valid():
                message = form.cleaned_data['notification_text']
                subject = form.cleaned_data['subject']

                data = {
                    "app_id": "c414492c-f6ce-4c68-8691-d9192102118a",
                    "included_segments": ["All"],
                    "contents": {"en": subject + ":  " + message}
                }
                requests.post(
                    "https://onesignal.com/api/v1/notifications",
                    headers={"Authorization": "Basic MWJjY2FkZDMtNzc0Mi00MDBhLTlkYzQtMjIzZGY2MDVmZjZj"},
                    json=data
                )

                return redirect('admin_index')
    return render(request, "admin_panel/admin_send_notification.html", {'form': form})


class Index(ClerkRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        data = {
            "wallets": [
                {"name": currency.sign, "credit": get_dollarial_company().get_credit(currency.char)}
                for currency in Currency.get_all_currencies()
            ]
        }
        return render(request, 'admin_panel/admin_index.html', data)


class ChargeCredit(StaffRequiredMixin, FormView):
    template_name = 'admin_panel/admin_charge.html'
    form_class = BankPaymentForm
    success_url = reverse_lazy('admin_index')

    def form_valid(self, form):
        bank_payment = form.save(commit=False)
        bank_payment.owner = get_dollarial_user()
        bank_payment.status = 'A'
        bank_payment.save()
        return super().form_valid(form)
