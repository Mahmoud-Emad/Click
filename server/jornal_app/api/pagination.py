from rest_framework import pagination
from rest_framework.response import Response
from collections import OrderedDict

class CustomPagination(pagination.CursorPagination):    
    """Custom pagination to add extra responses"""
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('message', 'Success'),
            ('data', data),
            ('error' , False ),
            ('next' , self.get_next_link()),
            ('previous',self.get_previous_link())
        ]))
