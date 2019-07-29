# -*- encoding: utf-8 -*-

from odoo import models, fields, api, exceptions
from odoo.exceptions import RedirectWarning, UserError, ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    aec_contact_type = fields.Selection([('b2c', 'Individual'),
                                         ('b2b', 'Corporate'),
                                         ('staff', 'Staff')], string='AEC Contact Type', default=False)

    actual_customer = fields.Boolean('Actual Customer', default=False)
    aec_customer_type = fields.Char('Customer type', help='It will contain ACTIVE_STUDENT and/or ACTIVE_MEMBER')

    membership_status = fields.Selection([('na', 'N/A'),
                                          ('former', 'Former member'),
                                          ('member', 'Member')], string='Membership status', default='na')
    membership_end_date = fields.Date('Membership End Date')
    student_status = fields.Selection([('na', 'N/A'),
                                       ('former', 'Former Student'),
                                       ('student', 'Student')], string='Student Status', default='na')
    staff_type = fields.Selection([('na', 'N/A'),
                                   ('former', 'Former Teacher'),
                                   ('teacher', 'Teacher'),
                                   ('admin', 'Administration'),
                                   ('former_admin', 'Former Admin')], string='Staff type', default='na')
    aec_student_ID = fields.Char('AEC Student ID')
    aec_company_ID = fields.Char('AEC Company ID')
    aec_staff_ID = fields.Char('AEC Staff ID')
    aec_country = fields.Char('Country Name')
    aec_account_creation_date = fields.Datetime('Account creation Date')
    aec_family_ID = fields.Integer('AEC Family ID')
    gender = fields.Char('Gender')
    civil_status = fields.Char('Civil Status')
    nationality = fields.Char('Nationality')
    mother_tongue = fields.Char('Mother Tongue')
    academic_level = fields.Char('Academic level')
    academic_establishment = fields.Char('Academic Establishment')
    birthday = fields.Date('Birthday')
    birth_country = fields.Char('Birth Country')
    company_size_id = fields.Many2one('partner.size', string='Company size')
    job_level_id = fields.Many2one('partner.job.level', string='Job Level')
    how_hear = fields.Char('How did you hear about us')

    linkedin = fields.Char('Linkedin')
    opt_in_out = fields.Boolean('Opt-in', default=True)


class PartnerSize(models.Model):
    _name = 'partner.size'
    _description = 'Business Size'
    _order = 'sequence,name'

    sequence = fields.Integer('Sequence', default=10)
    name = fields.Char('Name')
    active = fields.Boolean('Active', default=True)


class PartnerJobLevel(models.Model):
    _name = 'partner.job.level'
    _description = 'Job Level'
    _order = 'sequence,name'

    sequence = fields.Integer('Sequence', default=10)
    name = fields.Char('Name')
    active = fields.Boolean('Active', default=True)
