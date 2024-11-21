# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import models, fields, api

class Places(models.Model):
    _name = "places"
    _inherit = ['image.mixin']

    name = fields.Char()
    image = fields.Image(string="Image")
    description = fields.Text()
    image = fields.Image(string="Image")
    average_score = fields.Integer()
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
        comodel_name='users', 
        string='Creator',
        required=True,
        ondelete='cascade'
    )

    @api.model
    def create(self, vals):
        """Set last_modification o creation"""
        vals['last_modification_date'] = datetime.now()
        return super(Places, self).create(vals)
    
    def write(self, vals):
        """Update last_modification on edit"""
        vals['last_modification_date'] = datetime.now()
        return super(Places, self).write(vals)
