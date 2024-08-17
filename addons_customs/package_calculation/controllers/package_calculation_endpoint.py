# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request, Response

class PackageCalculation(http.Controller):
    # @http.route('/package_calculation/external_api/', auth='public')
    @http.route('/package_calculation/external_api/', type='json', auth='public', methods=['POST'], csrf=False)
    def data_external_api(self, **kwargs):
        print('LLEGALLEGA')
        print('LLEGALLEGA')
        print('LLEGALLEGA')
        # api_key = request.httprequest.headers.get('X-Api-Key')

        # # Validar la API key
        # user = request.env['res.users'].search([('api_key', '=', api_key)], limit=1)
        # if not user:
        #     return Response("Unauthorized", status=401)

        # data = {
        #     'name':'Gabriel Perdomo'
        # }
        return '{"status": "success", "data": data}'
