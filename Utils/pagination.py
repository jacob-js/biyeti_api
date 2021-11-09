from rest_framework import pagination

from .helpers import sendRes

class Pagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'p_size'
    page_query_param = 'p'

    def get_paginated_response(self, data):
        results = {}
        results['count'] = self.page.paginator.count
        results['rows'] = data
        return sendRes(200, data=results)