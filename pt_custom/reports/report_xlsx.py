# coding: utf-8
import io

from odoo import fields, models, api, _
import time
from datetime import datetime, date, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
import xlsxwriter
from io import BytesIO


# class AccountDailyBook(models.TransientModel):
#     _name = "account.daily.book"


class DoctorReferralXlsx(models.AbstractModel):
    _name = 'report.pt_custom.property_report_template_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        for obj in partners:
            report_name = obj.name
            # One sheet for xlsx
            sheet = workbook.add_worksheet("one")
            bold = workbook.add_format({'bold': True})
            sheet.write(0, 0, 'ID', bold)
            sheet.write(1, 0, obj.ref, bold)
            sheet.write(0, 1, 'Name', bold)
            sheet.write(1, 1, obj.name, bold)
            sheet.write(0, 2, 'Selling Price', bold)
            sheet.write(1, 2, obj.selling_price, bold)
            sheet.write(0, 3, 'No. Bedroom', bold)
            sheet.write(1, 3, obj.bedrooms, bold)
            sheet.write(0, 4, 'Owner Name', bold)
            sheet.write(1, 4, obj.owner_id.name, bold)
            sheet.write(0, 5, 'Garden', bold)
            sheet.write(1, 5, obj.garden, bold)
