from django.contrib.auth import get_user_model
from django.db.models.query import Q, QuerySet

from bank.models.account import Transfer

User = get_user_model()


class AccountSelector:
    """Account selector"""

    @staticmethod
    def get_transfers_history(iban: str, only_income: bool, only_outcome: bool) -> QuerySet[Transfer]:
        """Get account transfers history

        :param str iban: Account for which transfer you are looking for
        :param bool only_income: if true, returns only income transfers
        :param bool only_outcome: if true, returns only outcome transfers

        :return Queryset[Transfer]: Given page ancestors
        """
        query = Transfer.objects.all()
        if only_income:
            query = query.filter(destination=iban)
        elif only_outcome:
            query = query.filter(source=iban)
        else:
            query = query.filter(Q(source=iban) | Q(destination=iban))
        return query
