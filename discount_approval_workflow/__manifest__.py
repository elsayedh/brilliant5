# -*- coding: utf-8 -*-
{
    'name': 'Sale Order Discount Approval Workflow',
    'summary': "Sale Order Discount Approval Workflow",
    'description': "Sale Order Discount Approval Workflow",

    'author': 'iPredict IT Solutions Pvt. Ltd.',
    'website': 'http://ipredictitsolutions.com',
    'support': 'ipredictitsolutions@gmail.com',

    'category': 'Sales',
    'version': '14.0.0.1.0',
    'depends': ['sale_management'],

    'data': [
        'security/discount_approval_security.xml',
        'data/validate_order_line_email_template.xml',
        'views/res_users_view.xml',
        'views/sale_order_view.xml',
    ],

    'license': "OPL-1",
    'price': 15,
    'currency': "EUR",

    'auto_install': False,
    'installable': True,

    'images': ['static/description/banner.png'],
    'pre_init_hook': 'pre_init_check',
}
