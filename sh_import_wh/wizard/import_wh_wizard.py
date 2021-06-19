# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models, _
from odoo.exceptions import UserError
import csv
# import base64
import xlrd
from odoo.tools import ustr
import logging

#========For Excel========
from io import BytesIO
import xlwt
from xlwt import easyxf
import base64
from datetime import datetime
from datetime import timedelta
# =====================

_logger = logging.getLogger(__name__)


class ImportSOLWizard(models.TransientModel):
    _name = "import.wh.wizard"
    _description = "Import Delivery Stock Wizard"

    import_type = fields.Selection([
        ('csv', 'CSV File'),
        ('excel', 'Excel File')
    ], default="excel", string="Import File Type", required=True)
    file = fields.Binary(string="File", )
    product_by = fields.Selection([
        ('name', 'Name'),
        ('int_ref', 'Internal Reference'),
        ('barcode', 'Barcode')
    ], default="int_ref", string="Product By", required=True)
    excel_file = fields.Binary('Excel File')

    def validate_field_value(self, field_name, field_ttype, field_value, field_required, field_name_m2o):
        """ Validate field value, depending on field type and given value """
        self.ensure_one()

        try:
            checker = getattr(self, 'validate_field_' + field_ttype)
        except AttributeError:
            _logger.warning(
                field_ttype + ": This type of field has no validation method")
            return {}
        else:
            return checker(field_name, field_ttype, field_value, field_required, field_name_m2o)

    def validate_field_many2many(self, field_name, field_ttype, field_value, field_required, field_name_m2o):
        self.ensure_one()
        if field_required and field_value in (None, ""):
            return {"error": " - " + field_name + " is required. "}
        else:
            name_relational_model = self.env['stock.move.line'].fields_get()[
                field_name]['relation']

            ids_list = []
            if field_value.strip() not in (None, ""):
                for x in field_value.split(','):
                    x = x.strip()
                    if x != '':
                        record = self.env[name_relational_model].sudo().search([
                            (field_name_m2o, '=', x)
                        ], limit=1)

                        if record:
                            ids_list.append(record.id)
                        else:
                            return {"error": " - " + x + " not found. "}
                            break

            return {field_name: [(6, 0, ids_list)]}

    def validate_field_many2one(self, field_name, field_ttype, field_value, field_required, field_name_m2o):
        self.ensure_one()
        if field_required and field_value in (None, ""):
            return {"error": " - " + field_name + " is required. "}
        else:
            name_relational_model = self.env['stock.move.line'].fields_get()[
                field_name]['relation']
            record = self.env[name_relational_model].sudo().search([
                (field_name_m2o, '=', field_value)
            ], limit=1)
            return {field_name: record.id if record else False}

    def validate_field_text(self, field_name, field_ttype, field_value, field_required, field_name_m2o):
        self.ensure_one()
        if field_required and field_value in (None, ""):
            return {"error": " - " + field_name + " is required. "}
        else:
            return {field_name: field_value or False}

    def validate_field_integer(self, field_name, field_ttype, field_value, field_required, field_name_m2o):
        self.ensure_one()
        if field_required and field_value in (None, ""):
            return {"error": " - " + field_name + " is required. "}
        else:
            return {field_name: field_value or False}

    def validate_field_float(self, field_name, field_ttype, field_value, field_required, field_name_m2o):
        self.ensure_one()
        if field_required and field_value in (None, ""):
            return {"error": " - " + field_name + " is required. "}
        else:
            return {field_name: field_value or False}

    def validate_field_char(self, field_name, field_ttype, field_value, field_required, field_name_m2o):
        self.ensure_one()
        if field_required and field_value in (None, ""):
            return {"error": " - " + field_name + " is required. "}
        else:
            return {field_name: field_value or False}

    def validate_field_boolean(self, field_name, field_ttype, field_value, field_required, field_name_m2o):
        self.ensure_one()
#         if field_required and field_value in (None,""):
#             return {"error" : " - " + field_name + " is required. "}
#         else:
        boolean_field_value = False
        if field_value.strip() == 'TRUE':
            boolean_field_value = True

        return {field_name: boolean_field_value}

    def validate_field_selection(self, field_name, field_ttype, field_value, field_required, field_name_m2o):
        self.ensure_one()
        if field_required and field_value in (None, ""):
            return {"error": " - " + field_name + " is required. "}

        #get selection field key and value.
        selection_key_value_list = self.env['stock.move.line'].sudo(
        )._fields[field_name].selection
        if selection_key_value_list and field_value not in (None, ""):
            for tuple_item in selection_key_value_list:
                if tuple_item[1] == field_value:
                    return {field_name: tuple_item[0] or False}

            return {"error": " - " + field_name + " given value " + str(field_value) + " does not match for selection. "}

        #finaly return false
        if field_value in (None, ""):
            return {field_name: False}

        return {field_name: field_value or False}

    def show_success_msg(self, counter, skipped_line_no):
        # open the new success message box
        view = self.env.ref('sh_message.sh_message_wizard')
        context = dict(self._context or {})
        dic_msg = str(counter) + " Records imported successfully"
        if skipped_line_no:
            dic_msg = dic_msg + "\nNote:"
        for k, v in skipped_line_no.items():
            dic_msg = dic_msg + "\nRow No " + k + " " + v + " "
        context['message'] = dic_msg

        return {
            'name': 'Success',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.message.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': context,
        }

    def import_wh_apply(self):
        sol_obj = self.env['stock.move.line']
        ir_model_fields_obj = self.env['ir.model.fields']
        # perform import lead
        if self and self.file and self.env.context.get('sh_wh_id', False):
            wh_id = self.env.context.get('sh_wh_id')
            wh_obj = self.env['stock.picking'].sudo().search([("id", "=", wh_id)], limit=1)
            print(wh_id)
            print(wh_obj)
            # For CSV
            if self.import_type == 'csv' and wh_obj:
                counter = 0
                skipped_line_no = {}
                row_field_dic = {}
                row_field_error_dic = {}
                try:
                    file = str(base64.decodebytes(self.file).decode('utf-8'))
                    myreader = csv.reader(file.splitlines())
                    print("myreaderreader",myreader)
                    skip_header = True

                    for row in myreader:
                        try:
                            if skip_header:
                                skip_header = False

                                for i in range(2, len(row)):
                                    name_field = row[i]
                                    name_m2o = False
                                    if '@' in row[i]:
                                        list_field_str = name_field.split('@')
                                        name_field = list_field_str[0]
                                        name_m2o = list_field_str[1]
                                    search_field = ir_model_fields_obj.sudo().search([
                                        ("model", "=", "stock.move.line"),
                                        ("name", "=", name_field),
                                        ("store", "=", True),
                                    ], limit=1)

                                    if search_field:
                                        field_dic = {
                                            'name': name_field,
                                            'ttype': search_field.ttype,
                                            'required': search_field.required,
                                            'name_m2o': name_m2o
                                        }
                                        row_field_dic.update({i: field_dic})
                                    else:
                                        row_field_error_dic.update(
                                            {row[i]: " - field not found"})

                                continue

                            if row_field_error_dic:
                                res = self.show_success_msg(
                                    0, row_field_error_dic)
                                return res

                            if row[0] != '' and row[1] != '' :
                                product = row[0]

                                qty = row[1]
                                print(product)
                                print(qty)
                                vals = {}


                                found = False
                                print(wh_obj.move_line_ids_without_package)
                                for rec in wh_obj.move_line_ids_without_package:

                                    if self.product_by == 'name' and product == rec.product_id.name:
                                        rec.qty_done = qty
                                        found = True
                                        counter = counter + 1
                                        break;
                                    elif self.product_by == 'int_ref' and product == rec.product_id.default_code:
                                        rec.qty_done = qty
                                        found = True
                                        counter = counter + 1
                                        break;
                                    elif self.product_by == 'barcode' and product == rec.product_id.barcode:

                                        rec.qty_done = qty
                                        found = True
                                        counter = counter + 1
                                        break;

                                if found == False:
                                    skipped_line_no[str(counter)] = "Product " + product + " not found. "




                        except Exception as e:
                            skipped_line_no[str(
                                counter)] = " - Value is not valid " + ustr(e)

                            continue


                except Exception:
                    raise UserError(
                        _("Sorry, Your csv file does not match with our format"))

                if counter > 1:
                    completed_records = (counter )
                    res = self.show_success_msg(
                        completed_records, skipped_line_no)
                    return res

            # For Excel
            if self.import_type == 'excel' and  wh_obj:

                counter = 0
                skipped_line_no = {}
                row_field_dic = {}
                row_field_error_dic = {}
                try:
                    wb = xlrd.open_workbook(
                        file_contents=base64.decodebytes(self.file))
                    sheet = wb.sheet_by_index(0)
                    skip_header = True
                    for row in range(sheet.nrows):
                        try:
                            if skip_header:
                                skip_header = False
                                print("hi",range(3, sheet.ncols))
                                for i in range(3, sheet.ncols):
                                    name_field = sheet.cell(row, i).value
                                    name_m2o = False
                                    if '@' in sheet.cell(row, i).value:
                                        list_field_str = name_field.split('@')
                                        name_field = list_field_str[0]
                                        name_m2o = list_field_str[1]
                                    search_field = ir_model_fields_obj.sudo().search([
                                        ("model", "=", "stock.move.line"),
                                        ("name", "=", name_field),
                                        ("store", "=", True),
                                    ], limit=1)
                                    if search_field:
                                        field_dic = {
                                            'name': name_field,
                                            'ttype': search_field.ttype,
                                            'required': search_field.required,
                                            'name_m2o': name_m2o
                                        }
                                        row_field_dic.update({i: field_dic})
                                    else:
                                        row_field_error_dic.update(
                                            {sheet.cell(row, i).value: " - field not found"})
                                continue

                            if row_field_error_dic:
                                res = self.show_success_msg(
                                    0, row_field_error_dic)
                                return res
                            print("hi value",sheet.cell(row, 0).value ,sheet.cell(row, 1).value)
                            if sheet.cell(row, 0).value != '' and sheet.cell(row, 1).value != '' :
                                product = sheet.cell(row, 0).value

                                qty = sheet.cell(row, 2).value
                                vals = {}

                                field_nm = 'name'
                                if self.product_by == 'name':
                                    field_nm = 'name'
                                elif self.product_by == 'int_ref':
                                    field_nm = 'default_code'
                                elif self.product_by == 'barcode':
                                    field_nm = 'barcode'
                                found=False
                                for rec in wh_obj.move_line_ids_without_package :

                                    if self.product_by == 'name' and product== rec.product_id.name  :
                                        rec.qty_done=qty
                                        found=True
                                        counter = counter + 1
                                        break;
                                    elif self.product_by == 'int_ref' and product== rec.product_id.default_code:
                                        rec.qty_done = qty
                                        found = True
                                        counter = counter + 1
                                        break;
                                    elif self.product_by == 'barcode' and product== rec.product_id.barcode:
                                        rec.qty_done = qty
                                        found = True
                                        counter = counter + 1
                                        break;

                                if found== False :
                                    skipped_line_no[str(  counter)] =  "Product " + product+ " not found. "




                        except Exception as e:
                            skipped_line_no[str(
                                counter)] = " - Value is not valid " + ustr(e)

                            continue

                except Exception:
                    raise UserError(
                        _("Sorry, Your excel file does not match with our format"))

                if counter >= 1:
                    print(skipped_line_no)
                    print(counter)
                    completed_records = (counter )
                    res = self.show_success_msg(
                        completed_records, skipped_line_no)
                    return res

    def get_lines(self):
        product_ids = []
        if self and self.env.context.get('sh_wh_id', False):
            wh_id = self.env.context.get('sh_wh_id')
            wh_obj = self.env['stock.picking'].sudo().search([("id", "=", wh_id)], limit=1)
            print(wh_id)
            print(wh_obj)

            if wh_obj:
                product_ids = wh_obj.move_ids_without_package
        #         print("product_ids" ,product_ids)
        #         result = []
        #         if product_ids:
        #
        #            result = [{ 'values': [x for x in v]} for  v in product_ids]
        #
        # print("result",result)
        return product_ids



    def get_style(self):
        main_header_style = easyxf('font:height 300;'
                                   'align: horiz center;font: color black; font:bold True;'
                                   "borders: top thin,left thin,right thin,bottom thin")

        header_style = easyxf('font:height 200;pattern: pattern solid, fore_color gray25;'
                              'align: horiz right;font: color black; font:bold True;'
                              "borders: top thin,left thin,right thin,bottom thin")

        left_header_style = easyxf('font:height 200;pattern: pattern solid, fore_color gray25;'
                                   'align: horiz left;font: color black; font:bold True;'
                                   "borders: top thin,left thin,right thin,bottom thin")

        text_left = easyxf('font:height 200; align: horiz left;')

        text_right = easyxf('font:height 200; align: horiz right;', num_format_str='0.00')

        text_left_bold = easyxf('font:height 200; align: horiz right;font:bold True;')

        text_right_bold = easyxf('font:height 200; align: horiz right;font:bold True;', num_format_str='0.00')
        text_center = easyxf('font:height 200; align: horiz center;'
                             "borders: top thin,left thin,right thin,bottom thin")

        return [main_header_style, left_header_style, header_style, text_left, text_right, text_left_bold,
                text_right_bold, text_center]

    def create_excel_header(self, worksheet, main_header_style, text_left, text_center, left_header_style, text_right,
                            header_style):
        # worksheet.write_merge(0, 1, 1, 3, 'Stock Card', main_header_style)
        row =0
        col = 1
        # start_date = datetime.strptime(str(self.start_date), '%Y-%m-%d')
        # start_date = datetime.strftime(start_date, "%d-%m-%Y ")
        #
        # end_date = datetime.strptime(str(self.end_date), '%Y-%m-%d')
        # end_date = datetime.strftime(end_date, "%d-%m-%Y ")
        #
        # date = start_date + ' To ' + end_date
        # worksheet.write_merge(row, row, col, col + 2, date, text_center)



        worksheet.write(row, 0, 'Reference', left_header_style)
        worksheet.write(row, 1, 'Product Name', left_header_style)
        worksheet.write(row, 2, 'Qty', left_header_style)


        lines = self.get_lines()

        p_group_style = easyxf('font:height 200;pattern: pattern solid, fore_color ivory;'
                               'align: horiz left;font: color black; font:bold True;'
                               "borders: top thin,left thin,right thin,bottom thin")

        group_style = easyxf('font:height 200;pattern: pattern solid, fore_color ice_blue;'
                             'align: horiz left;font: color black; font:bold True;'
                             "borders: top thin,left thin,right thin,bottom thin")

        group_style_right = easyxf('font:height 200;pattern: pattern solid, fore_color ice_blue;'
                                   'align: horiz right;font: color black; font:bold True;'
                                   "borders: top thin,left thin,right thin,bottom thin", num_format_str='0.00')

        row += 1
        print(row)
        print(lines)
        for line in lines:
            # worksheet.write_merge(row, row, 0, 4, line.get('product'), p_group_style)
            worksheet.write(row, 0, line.product_id.default_code, text_center)
            worksheet.write(row, 1, line.product_id.name, text_center)
            worksheet.write(row, 2, line.product_uom_qty, text_center)
            print (line.product_id.default_code)
            print (line.product_id.name,)
            print (line.product_uom_qty)


            row += 1
        return worksheet, row

    def action_generate_excel(self):
        # ====================================
        # Style of Excel Sheet
        excel_style = self.get_style()
        main_header_style = excel_style[0]
        left_header_style = excel_style[1]
        header_style = excel_style[2]
        text_left = excel_style[3]
        text_right = excel_style[4]
        text_left_bold = excel_style[5]
        text_right_bold = excel_style[6]
        text_center = excel_style[7]
        # ====================================

        workbook = xlwt.Workbook()
        filename = 'Sample of Excel.xls'
        worksheet = workbook.add_sheet('Stock samples', cell_overwrite_ok=True)
        for i in range(0, 3):
            worksheet.col(i).width = 150 * 30

        worksheet, row = self.create_excel_header(worksheet, main_header_style, text_left, text_center,
                                                  left_header_style, text_right, header_style)

        # download Excel File
        fp = BytesIO()
        workbook.save(fp)
        fp.seek(0)
        excel_file = base64.encodebytes(fp.read())
        fp.close()
        self.write({'excel_file': excel_file})

        if self.excel_file:
            active_id = self.ids[0]
            return {
                'type': 'ir.actions.act_url',
                'url': 'web/content/?model=import.wh.wizard&download=true&field=excel_file&id=%s&filename=%s' % (
                    active_id, filename),
                'target': 'new',
            }




