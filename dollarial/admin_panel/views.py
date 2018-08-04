from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView

from dollarial.constants import DOLLARIAL_COMPANY
from dollarial.currency import Currency
from dollarial.mixins import ClerkRequiredMixin

from user_management.models import User


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
    fields = ['username', 'first_name', 'last_name', 'account_number', 'email',  'phone_number',
              'is_active', 'is_staff']
    success_url = reverse_lazy('admin_costumer_list')


def reviewer_list(request):
    # TODO: read from db
    data = {
        "reviewers": [
            {
                "id": "1",
                "username": "soroush",
                "salary": "200000",
            },
            {
                "id": "2",
                "username": "parand",
                "salary": "210000",
            },
            {
                "id": "3",
                "username": "kosar",
                "salary": "100000",
            }
        ]
    }
    return render(request, 'admin_panel/admin_reviewer_list.html', data)


def reviewer_view(request, reviewer_id):
    data = {
        'reviewer': {
            "id": reviewer_id,
            "username": "soroushe",
            "salary": "20000"
        }
    }
    return render(request, 'admin_panel/admin_reviewer_view.html', data)


def reviewer_add(request):
    return render(request, 'admin_panel/admin_reviewer_add.html')


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


def transaction_type_list(request):
    data = {
        "transaction_types": [
            {
                "id": "1",
                "name": "Toefl",
                "fixed_price": True,
                "price": 200,
                "currency": "$",
                "minimum": 1000,
                "maximum": 2000,
                "wage": 10
            },
            {
                "id": "2",
                "name": "IELTS",
                "fixed_price": True,
                "price": 200,
                "currency": "$",
                "minimum": None,
                "maximum": None,
                "wage": 10
            },
            {
                "id": "3",
                "name": "Europe University",
                "fixed_price": False,
                "price": None,
                "currency": "€",
                "minimum": 1000,
                "maximum": 2000,
                "wage": 10
            },
            {
                "id": "4",
                "name": "America University",
                "fixed_price": False,
                "price": None,
                "currency": "$",
                "minimum": 1000,
                "maximum": 2000,
                "wage": 10
            },
        ]
    }
    return render(request, 'admin_panel/admin_transaction_type_list.html', data)


def transaction_type_add(request):
    data = {
        "currencies": [
            "dollar", "euro", "rial"
        ]
    }
    return render(request, 'admin_panel/admin_transaction_type_add.html', data)


def transaction_type_view(request, transaction_type_id):
    data = {
        "transaction_type": {
            "id": transaction_type_id,
            "name": "Toefl",
            "description": "Toefl kheili khube!\nNice :))\n\n\nSo what?",
            "fixed_price": True,
            "price": None,
            "minimum": 1000,
            "maximum": 2000,
            "wage": 10,
            "currency": "rial",
            "required_information": {
                "personal": True,
                "public": True,
                "university": True,
                "quiz": False
            }
        },
        "currencies": [
            "dollar", "euro", "rial"
        ]
    }
    return render(request, 'admin_panel/admin_transaction_type_view.html', data)


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


def send_notification(request):
    return render(request, 'admin_panel/admin_send_notification.html')


class Index(ClerkRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        data = {
            "wallets": [
                {"name": currency.sign, "credit": DOLLARIAL_COMPANY.get_credit(currency.char)}
                for currency in Currency.get_all_currencies()
            ]
        }
        return render(request, 'admin_panel/admin_index.html', data)
