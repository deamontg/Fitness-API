"""
Filename: body_parser.py
Author: George Deamont <deamontg@gmail.com>
Description: Middleware for parsing the request body.
"""

import json, falcon


class JSONBodyParser(object):
    """
    Middleware for parsing a JSON request body.
    """
    error_messages = {
        'decode_error': "Request body is not valid 'application/json'"
    }

    def process_request(self, req, resp):
        """
        Attempts to parse the request body assuming a JSON structure. Will set the
        req.context['data'] to the converted JSON data on success, and raise an
        HTTPBadRequest exception on error.
        """
        if req.method == 'POST':
            body = req.stream.read(req.content_length or 0).decode('utf-8')

            try:
                data = json.loads(body)
                
                if isinstance(data, dict):
                    req.context['data'] = data
                else:
                    message = self.error_messages['decode_error']
                    raise falcon.HTTPBadRequest('Bad Request', message)
            
            except:
                message = self.error_messages['decode_error']
                raise falcon.HTTPBadRequest('Bad Request', message)