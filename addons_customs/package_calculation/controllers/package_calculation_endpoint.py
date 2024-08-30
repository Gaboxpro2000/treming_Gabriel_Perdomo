# -*- coding: utf-8 -*-

import json
from odoo import http
from odoo.http import request, Response

class TestApi(http.Controller):

    @http.route("/api/test", methods=["GET"],type="http",auth="none",csrf=False)
    def test_endpoint(self):
        print("HOLA!")

    @http.route('/api/package_calculation/external_api/', type='json', auth='none', methods=['POST'], csrf=False)
    def data_external_api(self, **kwargs):
        try:
            # Extraer el JSON recibido
            data = json.loads(request.httprequest.data)
            # Aquí puedes manejar el JSON recibido
            print('JSON recibido:', data)

            # Respuesta de éxito
            response_data = {
                "status": "success",
                "data": data  # O cualquier otra respuesta que desees
            }
            return response_data
        except Exception as e:
            # Manejo de errores
            return Response("Error procesando la solicitud: {}".format(e), status=400)