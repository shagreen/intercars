from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError
from django.db.models import F
from django.db.models.query import QuerySet
from rest_framework import exceptions
from faker import Faker

from bank.models.account import Account, Transfer
from intercars.utils.orm import model_update

User = get_user_model()


class AccountService:
    """Account service class"""

    @staticmethod
    def account_create(user: User, **account_data: dict) -> bool:
        """Account create function

        :param account_data: Data for creating account
        :param User user: The user to whom the account belongs

        :return: True whether account is created
        """
        while_flag = True
        while while_flag:
            try:
                iban = Faker(settings.FAKER_LOCALE).iban()
                Account.objects.create(user=user, iban=iban, **account_data)
                while_flag = False
            except IntegrityError:
                pass
        return True

    @staticmethod
    def account_update(account: Account, user: User, data: dict) -> bool:
        """Account update function

        :param Account account: account to update
        :param User user: The user to whom the account belongs
        :param data: Data for updating account

        :return: True whether account is updated
        """
        if account.user != user:
            raise exceptions.PermissionDenied()

        _updated_instance, has_updated = model_update(
            instance=account,
            fields=["name", "description"],
            data=data
        )
        return has_updated

    @staticmethod
    def account_user_list(user: User) -> QuerySet[Account]:
        """Lists users account

        :param User user: User to list accounts

        :return: User accounts
        """
        return Account.objects.filter(user=user)

    @staticmethod
    @transaction.atomic
    def account_transfer(account: str, user: User, amount: Decimal, destination: str) -> Transfer:
        """Make account money transfer

        :param str account: Source account
        :param User user: User making transfer
        :param Decimal amount: Amount
        :param str destination: destination account iban

        :return: Created Transfer
        """
        Account.objects.filter(iban=account).update(balance=F("balance") - amount)
        Account.objects.filter(iban=destination).update(balance=F("balance") + amount)
        return Transfer.objects.create(user=user, source=account, amount=amount, destination=destination)

    @staticmethod
    @transaction.atomic
    def account_deposit(account: str, amount: Decimal) -> bool:
        """Make deposit to account

        :param str account: Account iban
        :param Decimal amount: Amount

        :return bool: True
        """
        Account.objects.filter(iban=account).update(balance=F("balance") + amount)
        return True
