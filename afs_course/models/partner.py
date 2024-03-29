from odoo import models, fields, api, exceptions
from odoo.exceptions import RedirectWarning, UserError, ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    course_ids = fields.One2many('res.partner.course', 'partner_id', string='Courses')

    @api.model
    def cron_update_enrollment(self):
        # partner_id = self.env['course.participant'].search([(1, '=', 1)]).mapped('student_id')
        self.update_partner_enrollment()

    @api.multi
    def update_partner_enrollment(self, date_from=None, date_to=None):
        domain = [('synced_on_partner', '=', False), ('student_id', '!=', False)]
        if date_from and date_to:
            domain_partner_course = [('registration_date', '>=', date_from),
                                     ('registration_date', '<=', date_to)]
            course_to_delete_ids = self.env['res.partner.course'].search(domain_partner_course)
            course_to_delete_ids.unlink()
            domain = domain_partner_course
            domain.append(('student_id', '!=', False))

        participation_ids = self.env['course.participant'].search(domain)
        partner_ids = participation_ids.mapped('student_id')
        for rec in partner_ids:
            prt_id = participation_ids.filtered(lambda r: r.student_id == rec)

            vals = [(0, 0, {'course_id': p.course_id and p.course_id.id,
                            'category': p.course_id and p.course_id.category,
                            'term_ids': p.course_id and p.course_id.term_ids and [(4, i.id, 0) for i in p.course_id.term_ids] or False,
                            'registration_date': p.registration_date,
                            'registration_price': p.price,
                            'registration_type': p.registration_type}) for p in prt_id]
            prt_id.write({'synced_on_partner': True})
            rec.write({'course_ids': vals})
            self.env.cr.commit()


class ResPartnerCourse(models.Model):
    _name = 'res.partner.course'
    _description = 'Courses per student'

    partner_id = fields.Many2one('res.partner', 'Student', ondelete='cascade')
    course_id = fields.Many2one('course')
    category = fields.Char('Category')
    term_ids = fields.Many2many('course.term', string='Course Term(s)')

    registration_date = fields.Date('Registration date')
    registration_price = fields.Float('Registration Price')
    registration_type = fields.Char('Registration Type')
