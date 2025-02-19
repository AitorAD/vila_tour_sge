# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Places(models.Model):
    _name = "places"
    _inherit = ['image.mixin']

    name = fields.Char()
    # image = fields.Image(string="Image")
    description = fields.Text()
    # image = fields.Image(string="Image")
    average_score = fields.Float(string="Average Score", default=0.0, help="Average rating of the place")
    progress_percentage = fields.Integer('Progress Percentage', compute='_compute_progress_percentage')  # Nuevo campo calculado

    @api.depends('average_score')
    def _compute_progress_percentage(self):
        for record in self:
            # Calcula el porcentaje en base al average_score
            record.progress_percentage = int(record.average_score * 20)  # 5 estrellas = 100% => 1 estrella = 20%

    place_category = fields.Selection([
        ('beach', 'Playa'),
        ('monument', 'Monumento'),
        ('cultural_center', 'Centro Cultural'),
        ('historical_zone', 'Zona Historica'),
        ('mountain', 'Montaña'),
        ('museum', 'Museo'),
        ('park', 'Parque'),
        ('park_natural', 'Parque Natural'),
        ('theater', 'Teatro'),
        ('temple', 'Templo'),
        ('market', 'Mercado'),
        ('plaza', 'Plaza'),
        ('bridge', 'Puente'),
        ('botanical_garden', 'Jardín Botánico'),
    ], string="Tipo de Lugar")
    location = fields.Text()
    creation_date = fields.Datetime(string="Fecha de Creación", readonly=True, default=fields.Datetime.now)  # Campo de tipo fecha
    last_modification_date = fields.Datetime(string="Última Modificación", readonly=True, default=fields.Datetime.now)  # Campo de tipo fecha y hora
    
    creator_id = fields.Many2one(
        comodel_name='res.users',
        string='Creator',
        ondelete='cascade',
        default=lambda self: self.env.uid,
        required=True,
        help="The user who created this recipe"
    )

    @api.model
    def create(self, vals):
        """Set last_modification o creation"""
        vals['last_modification_date'] = datetime.now()
        vals['creator_id'] = self.env.uid
        return super(Places, self).create(vals)
    
    def write(self, vals):
        """Update last_modification on edit"""
        vals['last_modification_date'] = datetime.now()
        return super(Places, self).write(vals)

    _sql_constraints = [
        ('unique_place_name', 'unique(name)', "The place name must be unique."),
    ]

    @api.constrains('name')
    def _check_name_length(self):
        for record in self:
            if len(record.name) < 3:
                raise ValidationError("The recipe name must be at least 3 characters long.")