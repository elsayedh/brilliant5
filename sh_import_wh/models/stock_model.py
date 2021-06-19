# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def sh_import_wh(self):
        if self:
            action = self.env.ref(
                'sh_import_wh.sh_import_wh_action').sudo().read()[0]
            return action
