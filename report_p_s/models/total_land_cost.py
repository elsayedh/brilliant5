# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _


class StockLandCostTotal(models.Model):
    _inherit = "stock.landed.cost"

    # total_quantity = fields.Float(string='Total Quantity', store=True, readonly=True, compute='_amount_all',
    #                               tracking=4)
    # total_original_value = fields.Monetary(string='Total Original Value', store=True, readonly=True,
    #                                        compute='_amount_all', tracking=4)
    # total_new_value = fields.Monetary(string='Total New Value', store=True, readonly=True, compute='_amount_all',
    #                                   tracking=4)
    # total_additional_landed_cost = fields.Monetary(string='Total Additional', store=True, readonly=True,
    #                                                compute='_amount_all', tracking=4)
    #
    # @api.depends('valuation_adjustment_lines.quantity', 'valuation_adjustment_lines.former_cost',
    #              'valuation_adjustment_lines.final_cost', 'valuation_adjustment_lines.additional_landed_cost')
    # def _amount_all(self):
    #     for total in self:
    #         # total.total_quantity = sum(line.quantity for line in total.valuation_adjustment_lines)
    #         total.total_original_value = sum(line.former_cost for line in total.valuation_adjustment_lines)
    #         total.total_new_value = sum(line.final_cost for line in total.valuation_adjustment_lines)
    #         total.total_additional_landed_cost = sum(line.additional_landed_cost for line in
    #                                                  total.valuation_adjustment_lines)
