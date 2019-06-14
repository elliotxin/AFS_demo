# -*- encoding: utf-8 -*-

from odoo import models, fields, api, exceptions
from odoo.exceptions import RedirectWarning, UserError, ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    aec_contact_type = fields.Selection([('b2c', 'Contacts'),
                                         ('b2b', 'Corporate'),
                                         ('teach', 'Teacher')], string='AEC Contact Type', default=False)

    actual_customer = fields.Boolean('Actual Customer', default=False)
    membership_status = fields.Selection([('na', 'N/A'),
                                          ('former', 'Former member'),
                                          ('member', 'Member')], string='Membership status', default='na')
    student_status = fields.Selection([('na', 'N/A'),
                                       ('former', 'Former Student'),
                                       ('student', 'Student')], string='Student Status', default='na')
    teacher_status = fields.Selection([('na', 'N/A'),
                                       ('former', 'Former Teacher'),
                                       ('teacher', 'Teacher')], string='Teaching Status', default='na')
    aec_ID = fields.Char('AEC ID')
    gender = fields.Char('Gender')
    civil_status = fields.Char('Civil Status')
    nationality = fields.Char('Nationality')
    mother_tongue = fields.Char('Mother Tongue')
    academic_level = fields.Char('Academic level')
    academic_establishment = fields.Char('Academic Establishment')
    birthday = fields.Date('Birthday')
    birth_country = fields.Char('Birth Country')
    profession = fields.Char('Profession')

    company_type = fields.Char('Company type')
    industry = fields.Char('Industry')

