# Copyright 2015-2017 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
# Copyright 2017 ForgeFlow <http://www.forgeflow.com>
# Copyright 2018 Hai Dinh <haidd.uit@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    @api.model
    def message_route(
        self, message, message_dict, model=None, thread_id=None, custom_values=None
    ):
        res=None
        try:
            res = super(MailThread, self).message_route(
                message,
                message_dict,
                model=model,
                thread_id=thread_id,
                custom_values=custom_values,
            )
        except ValueError as ve:
            pass
        return res
