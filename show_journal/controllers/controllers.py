# -*- coding: utf-8 -*-
# from odoo import http


# class ShowJournal(http.Controller):
#     @http.route('/show_journal/show_journal/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/show_journal/show_journal/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('show_journal.listing', {
#             'root': '/show_journal/show_journal',
#             'objects': http.request.env['show_journal.show_journal'].search([]),
#         })

#     @http.route('/show_journal/show_journal/objects/<model("show_journal.show_journal"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('show_journal.object', {
#             'object': obj
#         })
