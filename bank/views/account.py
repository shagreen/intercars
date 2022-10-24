from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import exceptions, serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from bank.models.account import Account
from bank.paginators import AccountTransferHistoryPagination
from bank.selectors.account import AccountSelector
from bank.services.account import AccountService
from intercars.utils.inline_serializer import inline_serializer
from intercars.utils.views import get_paginated_response


class AccountCreateView(APIView):
    """Account create view"""

    permission_classes = (IsAuthenticated,)

    class InputSerializer(serializers.Serializer):
        """Account create input serializer"""
        name = serializers.CharField(max_length=500)
        description = serializers.CharField(max_length=500)

        class Meta:
            """Meta Class"""
            ref_name = None

    @swagger_auto_schema(
        request_body=InputSerializer,
        responses={201: openapi.Response('Account created', None)})
    def post(self, request):
        """Creates new account for token user"""
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        AccountService.account_create(**serializer.validated_data, user=self.request.user)

        return Response(status=status.HTTP_201_CREATED)


class AccountUpdateView(APIView):
    """Account edit view"""

    permission_classes = (IsAuthenticated,)

    class InputSerializer(serializers.Serializer):
        """Account create input serializer"""
        name = serializers.CharField(max_length=500)
        description = serializers.CharField(max_length=500)

        class Meta:
            """Meta Class"""
            ref_name = None

    @swagger_auto_schema(
        request_body=InputSerializer,
        responses={200: openapi.Response('Account updated')})
    def post(self, request, account_iban):
        """Creates new account for token user"""
        account = Account.objects.get(iban=account_iban)

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        AccountService.account_update(account, user=self.request.user, data=serializer.validated_data)

        return Response(status=status.HTTP_200_OK)


class AccountDashboardView(APIView):
    """Bank account user dashboard"""

    permission_classes = (IsAuthenticated,)

    class OutputSerializer(serializers.Serializer):
        """Account create input serializer"""

        alert = serializers.CharField()
        accounts = inline_serializer(many=True, fields={
            "name": serializers.CharField(max_length=500),
            "description": serializers.CharField(max_length=500),
            "balance": serializers.DecimalField(decimal_places=2, max_digits=12),
            "iban": serializers.CharField(max_length=28)
        })
        ads = inline_serializer(many=True, required=False, fields={  # TODO: Personalized user ads service

        })

        class Meta:
            """Meta Class"""
            ref_name = None

    @swagger_auto_schema(
        responses={200: openapi.Response('User account dashboard', OutputSerializer)})
    def get(self, request):
        """Creates new account for token user"""

        accounts = AccountService.account_user_list(user=request.user)
        alert = "Dziś 8-16 trwają prace serwisowe bla bla"  # TODO: Make Alert service
        output = self.OutputSerializer(data={
            "alert": alert,
            "accounts": list(accounts.values("name", "description", "balance", "iban"))
        })
        output.is_valid(raise_exception=True)

        return Response(output.data, status=status.HTTP_200_OK)


class AccountTransferView(APIView):
    """Account transfer View"""
    permission_classes = (IsAuthenticated,)

    class InputSerializer(serializers.Serializer):
        """Account create input serializer"""
        amount = serializers.DecimalField(decimal_places=2, max_digits=12)
        source_account = serializers.CharField(max_length=28, help_text="source account iban")
        destination = serializers.CharField(max_length=28, help_text="destination account iban")

        class Meta:
            """Meta Class"""
            ref_name = None

    @swagger_auto_schema(
        request_body=InputSerializer,
        responses={201: openapi.Response('Transfer created')})
    def post(self, request):
        """Creates transfer between accounts"""

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            account = Account.objects.get(iban=serializer.validated_data['source_account'])
        except Account.DoesNotExist:
            raise exceptions.ValidationError("Invalid source account iban!")
        if account.user != self.request.user:
            raise exceptions.PermissionDenied("You are not account owner!")
        if account.balance < serializer.validated_data['amount']:
            raise exceptions.ValidationError("Not enough money!")

        AccountService.account_transfer(
            account=account.iban,
            user=self.request.user,
            amount=serializer.validated_data['amount'],
            destination=serializer.validated_data['destination']
        )

        return Response(status=status.HTTP_201_CREATED)


class AccountDepositView(APIView):
    """Account deposit View"""
    permission_classes = (IsAuthenticated,)

    class InputSerializer(serializers.Serializer):
        """Account create input serializer"""
        amount = serializers.DecimalField(decimal_places=2, max_digits=12, required=True)
        iban = serializers.CharField(max_length=28, required=True)

        class Meta:
            """Meta Class"""
            ref_name = None

    @swagger_auto_schema(
        request_body=InputSerializer,
        responses={201: openapi.Response('Deposit created')})
    def post(self, request):
        """Creates account deposit"""

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            account = Account.objects.get(iban=serializer.validated_data.get("iban", ""), user=request.user)
        except Account.DoesNotExist:
            raise exceptions.ValidationError("Given Account does not exists")

        AccountService.account_deposit(
            account=account.iban,
            amount=serializer.validated_data['amount'],
        )

        return Response(status=status.HTTP_201_CREATED)


class AccountTransferHistoryView(APIView):
    """Bank account transfer history view"""

    only_income = openapi.Parameter(
        'only_income',
        openapi.IN_QUERY,
        description="if true, returns only income transfers",
        type=openapi.TYPE_BOOLEAN
    )
    only_outcome = openapi.Parameter(
        'only_outcome',
        openapi.IN_QUERY,
        description="if true, returns only outcome transfers",
        type=openapi.TYPE_BOOLEAN
    )
    iban = openapi.Parameter(
        'iban',
        openapi.IN_QUERY,
        description="Account iban which transfers relates",
        type=openapi.TYPE_STRING,
    )

    class OutputSerializer(serializers.Serializer):
        """Account create input serializer"""

        source = serializers.CharField(max_length=28)
        destination = serializers.CharField(max_length=28)
        amount = serializers.DecimalField(decimal_places=2, max_digits=12)

        class Meta:
            """Meta Class"""
            ref_name = None

    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        manual_parameters=[iban, only_income, only_outcome],
        responses={200: openapi.Response('Filtered account transfers', OutputSerializer)})
    def get(self, request):
        """Return filtered account transfers"""
        iban = self.request.query_params.get('iban')
        only_income = self.request.query_params.get('only_income', False) == 'true'
        only_outcome = self.request.query_params.get('only_outcome', False) == 'true'

        try:
            Account.objects.get(iban=iban, user=request.user)
        except Account.DoesNotExist:
            raise exceptions.ValidationError("Given Account does not exists")
        if only_outcome and only_income:
            raise exceptions.ValidationError("You can't use both only flags")

        return get_paginated_response(
            pagination_class=AccountTransferHistoryPagination,
            serializer_class=self.OutputSerializer,
            queryset=AccountSelector.get_transfers_history(iban, only_income, only_outcome),
            request=request,
            view=self
        )
