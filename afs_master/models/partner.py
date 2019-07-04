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
    is_student = fields.Boolean('is student', compute='_check_is_student', search='_search_is_student')

    membership_status = fields.Selection([('na', 'N/A'),
                                          ('former', 'Former member'),
                                          ('member', 'Member')], string='Membership status', default='na')
    student_status = fields.Selection([('na', 'N/A'),
                                       ('former', 'Former Student'),
                                       ('student', 'Student')], string='Student Status', default='na')
    staff_type = fields.Selection([('na', 'N/A'),
                                   ('former', 'Former Teacher'),
                                   ('teacher', 'Teacher'),
                                   ('admin', 'Administration')], string='Staff type', default='na')
    aec_ID = fields.Char('AEC ID')
    aec_country = fields.Char('Country Name')
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

    afs_company_type = fields.Char('Company type')
    linkedin = fields.Char('Linkedin')
    opt_in_out = fields.Boolean('Opt-in', default=True)

    @api.multi
    def _check_is_student(self):
        for rec in self:
            rec.is_student = rec.aec_customer_type and ('ACTIVE_STUDENT' in rec.aec_customer_type)

    def _search_is_student(self, operator, value):
        if operator == '=' and value == True:
            return [('aec_customer_type', 'ilike', 'ACTIVE_STUDENT')]


class PartnerSize(models.Model):
    _name = 'partner.size'
    _order = 'sequence,name'

    sequence = fields.Integer('Sequence', default=10)
    name = fields.Char('Name')
    active = fields.Boolean('Active', default=True)


class PartnerJobLevel(models.Model):
    _name = 'partner.job.level'
    _order = 'sequence,name'

    sequence = fields.Integer('Sequence', default=10)
    name = fields.Char('Name')
    active = fields.Boolean('Active', default=True)
