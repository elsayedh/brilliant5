# -*- coding: utf-8 -*-
# from odoo import http


# class ProductDetails(http.Controller):
#     @http.route('/product_details/product_details/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_details/product_details/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_details.listing', {
#             'root': '/product_details/product_details',
#             'objects': http.request.env['product_details.product_details'].search([]),
#         })

#     @http.route('/product_details/product_details/objects/<model("product_details.product_details"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_details.object', {
#             'object': obj
#         })
