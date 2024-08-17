from odoo import models,fields
from odoo.tools.misc import xlsxwriter
from odoo.exceptions import UserError, ValidationError
from datetime import date, timedelta
import io
import base64



class ReportInvoices(models.TransientModel):
    _name = 'report.package.calculation'

    def search_package_register(self):
            
        package_calculation_ids = self.env['package.calculation'].search([])
        return package_calculation_ids

    def report_action_xls(self):
        package_calculation_ids = self.search_package_register()
        return self._generate_xlsx_report(package_calculation_ids)

    def _generate_xlsx_report(self, data):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True, 'border': 1})
        center_across_format = workbook.add_format({
            'align': 'center_across',
            'valign': 'vcenter',
            'bold': True,
            'border': 1
        })
        date_format = workbook.add_format({'num_format': 'yyyy-mm-dd', 'border': 1})
        numeric_format = workbook.add_format({'num_format': '#,##0.00', 'border': 1})
        header_format = workbook.add_format({
            'bold': True,
            'border': 1,
            'bg_color': '#DCE6F1',
            'align': 'center',
            'valign': 'vcenter'
        })
        cell_format = workbook.add_format({'border': 1, 'align': 'left', 'valign': 'vcenter'})
        
        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 30)
        worksheet.set_column('C:C', 20)
        worksheet.set_column('D:D', 23)

        worksheet.merge_range('A2:E2', f"Paquetes Registrados", center_across_format)

        headers = [
            'Nombre del usuario', 'Paquete a enviar', 'costo de envio', 'Pais de envio',
        ]

        for col_num, header in enumerate(headers):
            worksheet.write(4, col_num, header, bold)

        row = 5
        for rec in data:
            for lines in rec.packages:
                worksheet.write(row, 0, rec.name)
                worksheet.write(row, 1, lines.name)
                worksheet.write(row, 2, rec.shipping_cost,numeric_format)
                worksheet.write(row, 3, rec.country_id.name)
                row += 1

        workbook.close()
        xlsx_data = base64.b64encode(output.getvalue())

        attachment = self.env['ir.attachment'].create({
            'name': 'Paquetes_registrados_XLS.xlsx',
            'type': 'binary',
            'datas': xlsx_data,
            'store_fname': 'Paquetes_registrados_XLS.xlsx',
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % (attachment.id),
            'target': 'new',
        }