from odoo import models, fields, api, exceptions
from odoo.exceptions import RedirectWarning, UserError, ValidationError


class Course(models.Model):
    _name = 'course'
    _description = 'Course'

    name = fields.Char('Course Name')
    class_code = fields.Char('Class Code')
    description = fields.Text('Description')
    level = fields.Char('Level')
    age_range = fields.Char('Age Range')
    subject = fields.Char('Subjects')
    category = fields.Char('Category')
    class_type = fields.Char('Class Type / Audience')
    modality = fields.Char('Modality')
    pace = fields.Char('Learning Pace')
    location = fields.Char('Location')
    aecID = fields.Char('AEC Course ID')
    class_price = fields.Float('Class Price')
    expected_duration = fields.Float('Scheduled Hours (hr)')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    state = fields.Char('Status')
    term_ids = fields.Many2many('course.term', string='Terms')
    session_ids = fields.One2many('course.session', 'course_id', 'Session')
    participant_ids = fields.One2many('course.participant', 'course_id', string='Participant')


class CourseParticipant(models.Model):
    _name = 'course.participant'
    _description = 'Registered Students'

    course_id = fields.Many2one('course', 'Course', ondelete='cascade')
    price = fields.Float('Registration Price')
    absence_rate = fields.Float('Absence rate')
    registration_date = fields.Date('Registration date')
    registration_type = fields.Char('Registration type')
    student_id = fields.Many2one('res.partner', 'Student')
    student_firstname = fields.Char(related='student_id.firstname', string='First Name', readonly=True)
    student_lastname = fields.Char(related='student_id.lastname', string='Last Name', readonly=True)
    customer_id = fields.Many2one('res.partner', 'Customer', help='The customer is the entity or individual paying for the course')


class CourseSession(models.Model):
    _name = 'course.session'
    _description = 'Session'
    _rec_name = 'date'

    sessionID = fields.Char('Session ID')
    teacher_id = fields.Many2one('res.partner', 'Teacher')
    classroom = fields.Char('Classroom')
    course_id = fields.Many2one('course', 'Course', ondelete='cascade')
    date = fields.Date('Date')
    start_time = fields.Char('Start Time')
    end_time = fields.Char('End Time')
    session_attended = fields.Boolean('Attended')
    attendance_ids = fields.One2many('course.session.attendance', 'session_id', 'Attendance')


class CourseSessionAttendance(models.Model):
    _name = 'course.session.attendance'
    _description = 'Attendance'

    session_id = fields.Many2one('course.session', 'Session', ondelete='cascade')
    attendee_id = fields.Many2one('res.partner', 'Attendee')
    attend = fields.Boolean('Attendance', default=False)
    note = fields.Char('Comment')


class CourseTerm(models.Model):
    _name = 'course.term'
    _description = 'Terms'

    name = fields.Char('Term name')
