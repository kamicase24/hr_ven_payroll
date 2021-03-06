#-*- coding:utf-8 -*-

import calendar
from datetime import datetime, timedelta, date
from dateutil import relativedelta

from odoo import api, fields, models, tools, _


def actual_date():
    actual = date.today()
    month = actual.month
    year = actual.year

    return [month, year]

class VenHrPayslip(models.Model):
    _name = 'hr.payslip'
    _inherit = 'hr.payslip'

    def _get_month_data(self):

        month = actual_date()[0]
        year = actual_date()[1]
        i = 1
        j = True

        num_day_in_month = calendar.monthrange(year,month)[1]
        monday = 0
        while j:
            if date.isoweekday(date(year,month,i)) == 1:
                monday += 1
            if i == num_day_in_month:
                j = False
            else:
                i = i+1
        return monday

    @api.onchange('date_to')
    def _get_worked_hours(self):
        global ts_sheet
        timesheet_sheet_sheet = self.env['hr_timesheet_sheet.sheet']
        ts_sheet = timesheet_sheet_sheet.search([('date_to','=',self.date_to),
                                                 ('date_from','=',self.date_from),
                                                 ('employee_id','=',self.employee_id.id)])
        ts_sheet.total_difference

        if ts_sheet.total_difference < 0:
            self.no_worked_hours = ts_sheet.total_difference
        else:
            self.daytime_extra_hours = ts_sheet.total_difference
        self.worked_hours = ts_sheet.total_attendance

    @api.onchange('night_extra_hours')
    def _set_night_hours(self):
        self.worked_hours = ts_sheet.total_attendance - self.night_extra_hours

    # @api.depends(trimestral_ded_trig)
    # def _set_trimestral_deduction(self):
    #     if self.trimestral_ded_trig == False:
    #         self.trimestral_ded_value = 0.0
    #     else:
    #         contract = self.env['hr_contract'].search([('employee_id','=',self.employee_id.id)])
    #         contract_wage = contract.wage
    #         self.trimestral_ded_value = (contract_wage * 3) * 0.05
    #
    monday_month = fields.Integer(string='Lunes del mes', default=_get_month_data)
    month = fields.Char(string='Mes', default=calendar.month_name[actual_date()[0]])
    final_day_month = fields.Integer(string='Fin del mes', default=calendar.monthrange(actual_date()[1],actual_date()[0])[1])
    sundays_holidays_worked = fields.Integer(string='Domingos y Feriados laborados')
    worked_hours = fields.Float(string='Horas trabajadas')
    no_worked_hours = fields.Float(string='Diferencia')
    daytime_extra_hours = fields.Float(string='Horas Extras Diurnas')
    night_extra_hours = fields.Float(string='Horas Extras Nocturnas')
    biweekly_days = fields.Integer(string='Dias de la Quincena', default=11)
    rest_days = fields.Integer(string='Días de Descanso', default=4)
    # trimestral_ded_trig = fields.Bool(default = False)
    # trimestral_ded_value = fields.Float(string = 'Aporte Trimestral', compute=_set_trimestral_deduction)









