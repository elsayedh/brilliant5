# -*- coding: utf-8 -*-

from odoo import fields, models, api


class MailMail(models.Model):
    _inherit = 'mail.mail'

    @api.model
    def create(self, values):
        if 'uid' in self._context:
            uid = self._context.get('uid')
            user_id = self.env['res.users'].browse(uid)
            if user_id:
                mail_server_id = self.env['ir.mail_server'].search([('user_id', '=', uid)])
                if mail_server_id:
                    email_from = '%s <%s>' % (user_id.partner_id.name, mail_server_id.smtp_user)
                    reply_to = '%s <%s>' % (user_id.partner_id.name, user_id.partner_id.email or mail_server_id.smtp_user)
                    values.update({'mail_server_id': mail_server_id.id, 'email_from': email_from, 'reply_to': reply_to})
        res = super(MailMail, self).create(values)
        return res
