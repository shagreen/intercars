from rest_framework.pagination import PageNumberPagination


class AccountTransferHistoryPagination(PageNumberPagination):
    """
    Custom pagination class for Account Transfer history view.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
