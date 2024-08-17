from odoo import models,fields
from odoo.tools.misc import xlsxwriter, formatLang
from odoo.exceptions import UserError, ValidationError
from datetime import date, timedelta
import io
import base64



class ReportInvoices(models.TransientModel):
    _name = 'report.payment.invoices'

    start_date = fields.Date(string='Desde',required=True)
    end_date = fields.Date(string='Hasta',required=True)

    def search_account_move_ids(self):
        if self.start_date>date.today():
            raise ValidationError('La Fecha inicial no puede ser mayor al dia de hoy ')
        if self.start_date > self.end_date:
            raise ValidationError('La Fecha inicial no puede ser mayor a la fecha final ')
            
        account_move_ids = self.env['account.move'].search([
            ('invoice_date', '>=', self.start_date),
            ('invoice_date', '<=', self.end_date)
        ])
        return account_move_ids

    def report_action_pdf(self):
        account_move_ids = self.search_account_move_ids()
        
        list_move_ids = []

        for move_id in account_move_ids:
            dict_move_ids = {
                'name':move_id.name,
                'cliente':move_id.partner_id.name,
                'invoice_date':move_id.invoice_date,
                'amount_untaxed':move_id.amount_untaxed,
                'amount_total':move_id.amount_total,
            }
        list_move_ids.append(dict_move_ids)
        data = {
            'records': list_move_ids,
            'start_date': self.start_date,
            'end_date': self.end_date,
        }
        return self.env.ref('package_calculation.print_invoices').report_action(self, data=data)

    def report_action_xls(self):
        account_move_ids = self.search_account_move_ids()
        return self._generate_xlsx_report(account_move_ids)

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
        worksheet.set_column('E:E', 23)

        worksheet.merge_range('A2:E2', f"Facturas desde: {self.start_date} hasta: {self.end_date}", center_across_format)

        headers = [
            'Numero de factura', 'Cliente', 'Fecha de Factura', 'Importe sin impuestos',
            'Total con impuestos' 
        ]

        for col_num, header in enumerate(headers):
            worksheet.write(4, col_num, header, bold)

        row = 5
        for rec in data:
            worksheet.write(row, 0, rec.name)
            worksheet.write(row, 1, rec.partner_id.name)
            worksheet.write(row, 2, rec.invoice_date,date_format)
            worksheet.write(row, 3, rec.amount_untaxed,numeric_format)
            worksheet.write(row, 4, rec.amount_total,numeric_format)
            row += 1

        workbook.close()
        xlsx_data = base64.b64encode(output.getvalue())

        attachment = self.env['ir.attachment'].create({
            'name': 'Facturas_XLS.xlsx',
            'type': 'binary',
            'datas': xlsx_data,
            'store_fname': 'Facturas_XLS.xlsx',
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % (attachment.id),
            'target': 'new',
        }