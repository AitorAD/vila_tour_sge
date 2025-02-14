# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class Festivals(models.Model):
    _name = "festivals"
    _description = "Festivals"
    _inherit = ['image.mixin']

    id = fields.Integer(string="ID", required=True, readonly=True)
    name = fields.Char(string="Name", required=True, placeholder="Festival Name", help="Enter the festival name")
    description = fields.Text(string="Description", help="Provide details about the festival")
    image = fields.Image(string="Image", max_width=1024, max_height=1024, help="Upload an image for the festival")
    creation_date = fields.Datetime(
        string="Creation Date",
        default=lambda self: fields.Datetime.now(),
        readonly=True
    )
    last_modification_date = fields.Datetime(
        string="Last Modification Date",
        default=lambda self: fields.Datetime.now(),
        readonly=True
    )
    average_score = fields.Float(string="Average Score", default=0.0, help="Average rating of the festival")
    progress_percentage = fields.Integer('Progress Percentage', compute='_compute_progress_percentage')  # Nuevo campo calculado

    @api.depends('average_score')
    def _compute_progress_percentage(self):
        for record in self:
            # Calcula el porcentaje en base al average_score
            record.progress_percentage = int(record.average_score * 20)  # 5 estrellas = 100% => 1 estrella = 20%

    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    latitude = fields.Float(string="Latitude", help="Latitude of the festival location")
    longitude = fields.Float(string="Longitude", help="Longitude of the festival location")

    creator_id = fields.Many2one(
        comodel_name='users',
        string='Creator',
        required=True,
        ondelete='cascade',
        help="The user who created this festival"
    )

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date > record.end_date:
                raise ValidationError("The start date must be before the end date.")

    @api.model
    def create(self, vals):
        vals['last_modification_date'] = datetime.now()
        return super(Festivals, self).create(vals)

    def write(self, vals):
        vals['last_modification_date'] = datetime.now()
        return super(Festivals, self).write(vals)

    _sql_constraints = [
        ('unique_festival_name', 'unique(name)', "The festival name must be unique."),
    ]
