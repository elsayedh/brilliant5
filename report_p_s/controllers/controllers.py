# -*- coding: utf-8 -*-
# from odoo import http


# class ReportPS(http.Controller):
#     @http.route('/report_p_s/report_p_s/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/report_p_s/report_p_s/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('report_p_s.listing', {
#             'root': '/report_p_s/report_p_s',
#             'objects': http.request.env['report_p_s.report_p_s'].search([]),
#         })

#     @http.route('/report_p_s/report_p_s/objects/<model("report_p_s.report_p_s"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('report_p_s.object', {
#             'object': obj
#         })
