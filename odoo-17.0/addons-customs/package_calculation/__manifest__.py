# -*- coding: utf-8 -*-
{
    'name': "package_calculation",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','sale'],

    # always loaded
    'data': [

        'security/ir.model.access.csv',
        'data/product_data.xml',
        'views/package_calculation.xml',
        'wizard/report_package_calculation.xml',
        'report/repot_invoice_pdf.xml',
        'wizard/report_invoice.xml'
        # 'views/templates.xml',
    ],
    'installable': True,
    'application': True,
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

