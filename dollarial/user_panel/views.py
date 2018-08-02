from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from dollarial.currency import Currency


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
                "owner": "user1",
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
                "owner": "user1",
                "destination": "Toefl Co.",
                "status": "reject"
            },
        ]
    }
    return render(request, 'user_panel/user_transaction_list.html', data)


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
    return render(request, 'user_panel/user_transaction_view.html', data)


def edit_profile(request):
    data = {
        "user": {
            "fname": "kossar",
            "lname": "najafi",
            "email": "kossar.najafi@gmail.com",
            "phone": "09351234567"
        }
    }
    return render(request, 'user_panel/user_edit_profile.html', data)


def payment_form(request):

    return render(request, 'user_panel/payment_form.html')


def payment_result(request):
    data = {
        "transaction": {
            "transaction_type": "University",
            "amount": "200",
            "currency": "$",
            "destination": "Stanford University",
        }
    }
    return render(request, 'user_panel/payment_result.html', data)


def exchange(request):
    data = {
        "wallets": {
            "rial": {
                "credit": 1000,
            },
            "dollar": {
                "credit": 2200,
            },
            "euro": {
                "credit": 1020
            }
        }
    }
    return render(request, 'user_panel/user_exchange_credit.html', data)


def exchange_accept(request):
    data = {
        "currencies": [
            "rial", "dollar", "euro"
        ],
        "from": "dollar",
        "to": "rial",
        "amount": {
            "from": 1,
            "to": 75000 * 0.93,
            "wage": 75000 * 0.07,
        }
    }
    return render(request, 'user_panel/user_exchange_acceptance.html', data)


class Index(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        data = {
            "wallets": [
                {"name": currency.sign, "credit": request.user.get_credit(currency.char)}
                for currency in Currency.get_all_currencies()
            ]
        }
        return render(request, 'user_panel/user_index.html', data)

