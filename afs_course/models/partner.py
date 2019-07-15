from odoo import models, fields, api, exceptions
from odoo.exceptions import RedirectWarning, UserError, ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    course_ids = fields.One2many('res.partner.course', 'partner_id', string='Courses')

    @api.model
    def cron_update_enrollment(self):
        print(1)
        partner_id = self.env['course.participant'].search([(1, '=', 1)]).mapped('student_id')
        partner_id.update_partner_enrollment()

    @api.multi
    def update_partner_enrollment(self):
        for rec in self:
            rec.course_ids.unlink()
            participation_ids = self.env['course.participant'].search([('student_id', '=', rec.id)])
            vals = [(0, 0, {'course_id': p.course_id and p.course_id.id,
                            'category': p.course_id and p.course_id.category,
                            'term': p.course_id and p.course_id.term,
                            'registration_date': p.registration_date,
                            'registration_price': p.price,
                            'registration_type': p.registration_type}) for p in participation_ids]
            rec.write({'course_ids': vals})


class ResPartnerCourse(models.Model):
    _name = 'res.partner.course'
    _description = 'Courses per student'

    partner_id = fields.Many2one('res.partner', 'Student', ondelete='cascade')
    course_id = fields.Many2one('course')
    category = fields.Char('Category')
    term = fields.Char('Term')

    registration_date = fields.Date('Registration date')
    registration_price = fields.Float('Registration Price')
    registration_type = fields.Char('Registration Type')
