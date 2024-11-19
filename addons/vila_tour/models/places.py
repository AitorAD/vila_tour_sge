# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import models, fields, api

class Places(models.Model):
    _name = "places"

    name = fields.Char()
    description = fields.Text()
    creator = fields.Text()
    image_1920 = fields.Binary(string="Image")
    rating = fields.Integer()
    place_category = fields.Selection([
        ('beach', 'Playa'),
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
    last_modification = fields.Datetime(string="Última Modificación", readonly=True)  # Campo de tipo fecha y hora

    @api.model
    def create(self, vals):
        """Set last_modification o creation"""
        vals['last_modification'] = datetime.now()
        return super(Places, self).create(vals)
    
    def write(self, vals):
        """Update last_modification on edit"""
        vals['last_modification'] = datetime.now()
        return super(Places, self).write(vals)
