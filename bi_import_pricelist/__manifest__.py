# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Import Pricelist from Excel or CSV File',
    'version': '14.0.0.5',
    'sequence': 4,
    'summary': 'Apps helps to Import pricelist import multiple pricelist lines import vendor pricelist import sales pricelist import product pricelists import customer pricelist  import from excel pricelist import from csv import Price list import Pricelist item import',
    'category': 'sales',
    "price": 29,
    "currency": 'EUR',
    'description': """
    odoo Import vendor and sale pricelist from Excel and CSV import sale pricelist import
    odoo import pricelist from excel import pricelist from csv import vendor pricelist from excel
    odoo import vendor pricelist from csv import supplier pricelist from excel
    odoo import supplier pricelist from csv import purchase pricleist from excel import purchase pricelist from csv
    odoo import sales pricelist from excel import customer pricelist from excel odoo
    odoo import sales pricelist from csv pricelist import multiple pricelist Price List 
    odoo Price List import odoo import Price List sale Price List import sale pricelist 
    odoo supplier pricelist odoo vendor pricelist import customer pricelist import product pricelist 
odoo price list import item price list import Sales Pricelist import Sales Price List
odoo import Price list diferent prices odoo diferent prices Odoo import PriceLists import
import Customer Pricelist import odoo Import vendors pricelists import Sales Pricelists import inventory pricelist
odoo add pricelist import multiple pricelist import import customer pricelist from csv
    """,
    'author': 'BrowseInfo',
    'website': 'http://www.browseinfo.in',
    'depends': ['base','sale','purchase','sale_management'],
    'data': [
            'security/ir.model.access.csv',
            'views/sale.xml'
        ],
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/EtRDX07PfbE',
    "images":['static/description/Banner.png'],
}
