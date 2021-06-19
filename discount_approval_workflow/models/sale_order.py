# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
#
class SaleOrderInheritIP(models.Model):
    _inherit = "sale.order.line"

    is_need_approve =fields.Boolean(string="Need Approve",default=False)
    is_duplicate =fields.Boolean(string="duplicate",default=False)

#
#     price_unit = fields.Float('Unit Price', required=True, digits='Product Price', default=0.0, read=)

    # def _getgroup(self):
    #     user = self.env.user
    #
    #     for record in self:
    #         record.restrict_user_price = False
    #         if not ( user.has_group('discount_approval_workflow.discount_approval_manager')
    #                  and   user.has_group('discount_approval_workflow.discount_approval_director') ):
    #             record.restrict_user_price  = True
    #
    # restrict_user_price=fields.Boolean(string="user restrict", compute="_getgroup")

class SaleOrderInheritIP(models.Model):
    _inherit = "sale.order"


    discount_approve_by = fields.Many2one(
        'res.users', string='Discount Approve By', readonly=True, tracking=True)

    discount_approve_director_by = fields.Many2one(
        'res.users', string='Director Approval', readonly=True, tracking=True)

    state = fields.Selection(selection_add=[('waiting', 'Approval by Manager'),('waiting2', 'Approval by Director'),])

    def action_check_stock(self):
        if self.order_line:
            raise_warning = False
            message = '''You can't confirm this order because of\
               following reasons:\n\n'''
            for line in self.order_line:
                 available_product_qty = line.product_id.with_context(
                    {'warehouse': line.order_id.warehouse_id.id}).qty_available

                 if line.product_uom_qty > available_product_qty:
                            available_product_qty = line.product_id.with_context(
                                {'warehouse': line.order_id.warehouse_id.id}
                            ).qty_available
                            message += _('You have added %s %s of %s but you only have\
                               %s %s available in %s warehouse.\n\n') % \
                                       (line.product_uom_qty,
                                        line.product_uom.name,
                                        line.product_id.name,
                                        available_product_qty,
                                        line.product_uom.name,
                                        line.order_id.warehouse_id.name)
                            raise_warning = True
            if raise_warning:
                raise ValidationError(message)

    def get_product_str(self):
        str=""
        if self.partner_id and self.pricelist_id:

            for rec in self.order_line:
                found=False
                for line in self.pricelist_id.item_ids:

                   if line.applied_on =='1_product':
                        # print("line.apply_on ", line.applied_on)
                        # print("line.product_tmp_id ", line.product_tmpl_id)
                        # print("line.product_tmp_id. price", line.product_tmpl_id.list_price)
                        # print("line.compute_price ", line.compute_price)
                        # print("line.prcent_price ", line.percent_price)

                                  if rec.product_id.product_tmpl_id.id ==  line.product_tmpl_id.id :
                                    found= True

                                    if line.compute_price =='percentage':

                                        if (rec.discount != line.percent_price ):
                                            str+="Product "+ rec.product_id.name + "has differenct price or discount than price list "+"\n"

                                            rec.is_need_approve=True
                                            break
                                        else :
                                          rec.is_need_approve=False
                                    elif  line.compute_price =='fixed':
                                        if ( rec.price_unit != line.fixed_price):
                                            str += "Product " + rec.product_id.name + "has differenct price or discount than price list " + "\n"
                                            rec.is_need_approve = True
                                            break
                                        else :
                                          rec.is_need_approve=False
                   elif line.applied_on =='0_product_variant':
                        # print("line.apply_on ", line.applied_on)
                        # print("line.product_tmp_id ", line.product_tmpl_id)
                        # print("line.product_tmp_id. price", line.product_tmpl_id.list_price)
                        # print("line.compute_price ", line.compute_price)
                        # print("line.prcent_price ", line.percent_price)

                                  if rec.product_id.id ==  line.product_id.id :
                                    found= True

                                    if line.compute_price =='percentage':

                                        if (rec.discount != line.percent_price ):
                                            str+="Product "+ rec.product_id.name + "has differenct price or discount than price list "+"\n"

                                            rec.is_need_approve=True
                                            break
                                        else :
                                          rec.is_need_approve=False
                                    elif  line.compute_price =='fixed':
                                        if ( rec.price_unit != line.fixed_price):
                                            str += "Product " + rec.product_id.name + "has differenct price or discount than price list " + "\n"
                                            rec.is_need_approve = True
                                            break
                                        else :
                                          rec.is_need_approve=False
                if found == False :
                    str += "Product " + rec.product_id.name + "has not Found price list " + "\n"
                    rec.is_need_approve = True

        return str


    def action_confirm_check_discount(self):

        str =""

        str = self.get_product_str()
        print(str)
        # This check stock
        self.action_check_stock()

        if str !="" :
            ctx = {}

            # email_to_list = [user.email for user in self.env['res.users'].sudo().search(
            #     []) if user.has_group('discount_approval_workflow.discount_approval_manager')]
            obj_user=self.env.user
            obj_emp= self.env['hr.employee'].sudo().search( [('user_id','=',obj_user.id)])
            email_to_list = []
            if obj_emp.parent_id.user_id :
                obj_emp_manager_user =obj_emp.parent_id.user_id
                if obj_emp_manager_user.email:
                    email_to_list.append(obj_emp_manager_user.email)


            print("email list", email_to_list)
            if email_to_list:
                ctx['email_to'] = ','.join([email for email in email_to_list if email])
                ctx['email_from'] = self.env.user.email
                ctx['lang'] = self.env.user.lang
                template = self.env.ref('discount_approval_workflow.validate_order_line_email_template')
                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                db = self.env.cr.dbname
                ctx['action_url'] = "{}/web?db={}#id={}&model=sale.order&view_type=form".format(base_url, db, self.id)
                obj_id = template.with_context(ctx).sudo().send_mail(self.id, force_send=True, raise_exception=False)
                print("obj_id", obj_id)
            self.write({'state': 'waiting'})
        else:
            self.action_confirm()

    def action_discount_approval_director(self):
        self.discount_approve_director_by = self.env.user.id
        self.action_confirm()




    def action_discount_approval(self):
        self.discount_approve_by = self.env.user.id
        ctx = {}
        # email_to_list = [user.email for user in self.env['res.users'].sudo().search(
        #     []) if user.has_group('discount_approval_workflow.discount_approval_director')]
        obj_user = self.env.user
        obj_emp = self.env['hr.employee'].sudo().search([('user_id', '=', obj_user.id)])
        email_to_list = []
        if obj_emp.parent_id.user_id:
            obj_emp_manager_user = obj_emp.parent_id.user_id
            if obj_emp_manager_user.email:
                email_to_list.append(obj_emp_manager_user.email)

        print("email list2", email_to_list)
        if email_to_list:
            ctx['email_to'] = ','.join([email for email in email_to_list if email])
            ctx['email_from'] = self.env.user.email
            ctx['lang'] = self.env.user.lang
            template = self.env.ref('discount_approval_workflow.validate_order_line_email_template')
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            db = self.env.cr.dbname
            ctx['action_url'] = "{}/web?db={}#id={}&model=sale.order&view_type=form".format(base_url, db, self.id)
            template.with_context(ctx).sudo().send_mail(self.id, force_send=True, raise_exception=False)
        self.write({'state': 'waiting2'})


    @api.constrains('order_line')
    def _check_exist_product_in_line(self):
        str=""
        for rec in self:
            exist_product_list = []
            for line in rec.order_line:
                if line.product_id.id in exist_product_list:
                    str+=  "\n"+line.product_id.name
                    line.is_duplicate=True
                exist_product_list.append(line.product_id.id)
        print(str)
        if str !="":
            raise ValidationError(_('Product should be one per line.'+ str) )

# class SaleOrderline(models.Model):
#     _inherit = "sale.order.line"
#
#     _sql_constraints = [('order_product_uniq', 'unique (order_id,product_id)',
#                          'Duplicate products in order line not allowed !')]
    # @api.onchange('price_unit')
    # def price_unit_change(self):
    #     if self.order_id.pricelist_id:
    #         price_unit = self.price_unit
    #         price_unit_sale = self.price_unit
    #         price_subtotal=self.price_subtotal
    #         # Check if price has been changed manually
    #         if self.order_id.pricelist_id and self.product_id \
    #             and not (self.user_has_groups('discount_approval_workflow.discount_approval_manager')
    #                      and self.user_has_groups('discount_approval_workflow.discount_approval_director')):
    #             product_context = dict(self.env.context,
    #                                    partner_id=self.order_id.partner_id.id,
    #                                    date=self.order_id.date_order,
    #                                    uom=self.product_uom.id)
    #             # Here variable price calculates the price of product after
    #             # applying pricelist on it and rule_id is the id of the rule
    #             # of pricelist which is applied on product
    #             price, rule_id = self.order_id.pricelist_id.with_context(
    #                 product_context).get_product_price_rule(
    #                 self.product_id, self.product_uom_qty or 1.0,
    #                 self.order_id.partner_id)
    #
    #             print("Price",price , rule_id , price_unit_sale,price_subtotal,  )
    #             # if ((self.price_unit < (price*(1+(discount/100))))  or (self.discount <discount )) and rule_id:
    #             if  (self.price_unit < price_unit_sale)  and rule_id:
    #                 raise UserError(
    #                     _('You don\'t have Access to change the Price less than %s ') %(price_unit_sale))
    #
    #             if  (self.price_unit < price_unit_sale)  and rule_id:
    #                 raise UserError(
    #                     _('You don\'t have Access to change the Price less than %s ') %(price_unit_sale))
