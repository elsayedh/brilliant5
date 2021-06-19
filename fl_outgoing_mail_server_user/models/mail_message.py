# -*- coding: utf-8 -*-

from odoo import api, models


class Message(models.Model):
    _inherit = 'mail.message'

    @api.model
    def create(self, values):
        uid = self._uid
        user_id = self.env['res.users'].browse(uid)
        mail_server_id = self.env['ir.mail_server'].sudo().search([('user_id', '=', uid)])
        if mail_server_id:
            email_from = '%s <%s>' % (user_id.partner_id.name, mail_server_id.smtp_user)
            reply_to = '%s <%s>' % (user_id.partner_id.name, user_id.partner_id.email or mail_server_id.smtp_user)
            values.update({'mail_server_id': mail_server_id.id, 'email_from': email_from, 'reply_to': reply_to})
        res = super(Message, self).create(values)
        return res
