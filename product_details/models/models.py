# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions, _


class ProductCategory(models.Model):
    _inherit = 'product.category'

    name = fields.Char('Name', index=True, required=True, translate=True)

    @api.depends('name')
    def name_get(self):
        print("hi",self.env.lang)
        res = []
        for record in self:
            name =  record.name
            print("name",record.name)
            res.append((record.id, name))
        return res

class ProductTemplatedetails(models.Model):
    _name='product.color'
    name = fields.Char('Color', index=True, translate=True)

    @api.depends('name')
    def name_get(self):
        print("hi", self.env.lang)
        res = []
        for record in self:
            name = record.name
            print("name", record.name)
            res.append((record.id, name))
        return res

class ProductTemplatedetailsb(models.Model):
    _name='product.brand'

    name = fields.Char('Brand', index=True, translate=True)

    @api.depends('name')
    def name_get(self):
        print("hi", self.env.lang)
        res = []
        for record in self:
            name = record.name
            print("name", record.name)
            res.append((record.id, name))
        return res

class ProductTemplate(models.Model):
    _inherit = "product.template"

    color_id = fields.Many2one('product.color', 'Color',  ondelete='cascade')
    brand_id = fields.Many2one('product.brand', 'Brand',ondelete='cascade')




#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
