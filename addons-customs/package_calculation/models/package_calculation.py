from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError
import requests



class PackageCalculation(models.Model):
    _name = 'package.calculation'
    _description = 'Cálculo de Paquetes'
    
    name = fields.Char(string='Nombre del Usuario', required=True)
    address = fields.Text(string='Dirección del Usuario', required=True)
    packages = fields.Many2many('product.product', string='Paquetes Seleccionados')
    current_location = fields.Many2one('res.country', string='Ubicacion Actual', required=True)
    country_id = fields.Many2one('res.country', string='País de Envío', required=True)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('done', 'Hecho'),
        ('cancelled', 'Cancelado'),
    ], string='Estado', default='draft')
    shipping_cost = fields.Float(string='Costo de Envío', readonly=True)
    delivery_time = fields.Char(string='Tiempo de Entrega Estimado', readonly=True)
    timezone_now = fields.Char(string='Zona Horaria Actual')
    timezone_delivery = fields.Char(string='Zona Horaria de entrega')
    sale_order_id = fields.Many2one('sale.order', string="Orden de Venta", readonly=True)

    def action_cancel(self):
        self.state = 'cancelled'

    def get_timezone(self,country_id):
        try:
            key = 'NOTYU7R98HUR'
            country_name = country_id.code
            url = f"http://api.timezonedb.com/v2.1/list-time-zone?key={key}&format=json&country={country_name}"
            
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('zones'):
                    return data['zones'][0]['zoneName']
                else:
                    return "No se encontraron zonas horarias para el país: " + country_name
            else:
                _logger.error("Error al consultar la API de TimeZoneDB: %s", response.text)
                return "Error al consultar la API"
        except:
            raise ValidationError(_('ERROR DE CONEXION'))

    def action_done(self):
        self.state = 'done'
        var_status = False

        if self.current_location:
            self.timezone_now = self.get_timezone(self.current_location)
            var_status = True
        
        if self.country_id:
            self.timezone_delivery = self.get_timezone(self.country_id)
            var_status = True
        
        if var_status:
            self.calculate_shipping()
            self.create_sale_order()
        else:
            raise ValidationError(_('ERROR AL CALCULAR'))
            

    def calculate_time_difference(self,offset1, offset2):
        def parse_offset(offset):
            sign = 1 if offset[0] == '+' else -1
            hours, minutes = map(int, offset[1:].split(':'))
            return timedelta(hours=sign * hours, minutes=sign * minutes)

        offset1_timedelta = parse_offset(offset1)
        offset2_timedelta = parse_offset(offset2)

        difference = offset2_timedelta - offset1_timedelta
        return difference.total_seconds() / 3600

    def calculate_shipping(self):
        if self.timezone_now and self.timezone_delivery:
            try:
                user_time_current = requests.get(f'https://worldtimeapi.org/api/timezone/{self.timezone_now}').json().get('utc_offset')
                user_time_delivery = requests.get(f'https://worldtimeapi.org/api/timezone/{self.timezone_delivery}').json().get('utc_offset')
                
                if user_time_current and user_time_delivery:
                    difference = self.calculate_time_difference(user_time_current, user_time_delivery)
                    if difference > 4:
                        self.shipping_cost = 10
                    else:
                        self.shipping_cost = 0
                    self.delivery_time = "3-5 días"
                else:
                    raise ValidationError("No se pudieron obtener las zonas horarias UTC.")
                    
            except requests.RequestException as e:
                raise ValidationError(f"Error al realizar la solicitud a la API: {e}")

    def create_sale_order(self):
        SaleOrder = self.env['sale.order']
        SaleOrderLine = self.env['sale.order.line']

        sale_order = SaleOrder.create({
            'partner_id': self.env.user.partner_id.id,
            'date_order': fields.Datetime.now(),
            'origin': self.name,  
        })
        for package in self.packages:
            SaleOrderLine.create({
                'order_id': sale_order.id,
                'product_id': package.id,
                'product_uom_qty': 1,
                'price_unit': package.lst_price,
            })

            if self.shipping_cost > 0:
                shipping_product = self.env.ref('package_calculation.product_shipping_service')  
                SaleOrderLine.create({
                    'order_id': sale_order.id,
                    'product_id': shipping_product.id,
                    'product_uom_qty': 1,
                    'price_unit': self.shipping_cost,
                })

        self.sale_order_id = sale_order.id

        return sale_order