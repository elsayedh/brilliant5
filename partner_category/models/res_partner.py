from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_category_id = fields.Many2one('partner.category', 'Category Channel'  )
    partner_cr = fields.Char(string='CR' )
    ref = fields.Char(string='Reference', index=True  )


    def get_is_customer(self):
        for rec in self:
            search_partner_mode = rec.env.context.get('res_partner_search_mode')

            rec.is_customer = search_partner_mode == 'customer'


    is_customer = fields.Boolean(string="Customer", compute="get_is_customer" )



class ResPartnerHCategory(models.Model):
    _name = 'partner.category'
    _description = 'Category Channel'

    name = fields.Char("Category Channel", required=True)
    parent_id = fields.Many2one('partner.category', 'Parent Category')
    child_category_ids = fields.One2many('partner.category', 'parent_id', 'Child Category')
    partner_ids = fields.One2many('res.partner', 'partner_category_id', 'Partners')
