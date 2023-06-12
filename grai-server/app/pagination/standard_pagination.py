from rest_framework.pagination import PageNumberPagination


class StandardResultsPagination(PageNumberPagination):
    page_size = 100  # default page size

    page_size_query_param = "size"  # query param to allow user to set page size

    max_page_size = 1000  # max page size allowed
