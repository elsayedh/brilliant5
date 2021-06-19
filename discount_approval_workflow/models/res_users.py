# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ResUsersInheritIP(models.Model):
    _inherit = 'res.users'

    allow_discount = fields.Float()

    @api.onchange('allow_discount')
    def onchange_discount(self):
        if not 0 < self.allow_discount < 100:
            raise ValidationError(_("Allow discount between 0 to 100 only."))






