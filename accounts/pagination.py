from rest_framework.pagination import PageNumberPagination

class Pagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_query_param = 'next_page'  # change the query parameter name
    max_page_size = 1000

