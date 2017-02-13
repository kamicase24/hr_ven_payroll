# -*- coding: utf-8 -*-
{
    'name' : 'Module for Venelezuelan payroll',
    'version' : '1.0',
	'author' : 'kamicase24',
    'description' : """ Add fields in hr_payroll module for the Venezuelan payroll
 * Amount of Monday that owns a month
 * Month name and number
 * Final number day that owns a month
 * Extra hours
""",
    'sequence' : 39,
    'category' : 'Human Resources',
    'website' : '',
    'depends' : ['hr_payroll'],
    'data' : [
        'views/hr_payroll_views.xml',
    ],
    'demo' : [],
}