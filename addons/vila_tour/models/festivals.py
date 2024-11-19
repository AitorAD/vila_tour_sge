# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import datetime

class Festivals(models.Model):
    _name = "festivals"
    _description = "Festivals"
    _inherit = ['image.mixin']

    id = fields.Integer(string="ID", required=True)
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    image = fields.Image(string="Image")
    creation_date = fields.Datetime(
        string="Creation Date", 
        default=fields.Datetime.now,
        readonly=True
    )
    last_modification_date = fields.Datetime(
        string="Last Modification Date", 
        default=fields.Datetime.now,
        readonly=True
    )
    average_score = fields.Float(string="Average Score")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    latitude = fields.Float(string="Latitude")
    longitude = fields.Float(string="Longitude")

    creator_id = fields.Many2one(
        comodel_name='users', 
        string='Creator',
        required=True,
        ondelete='cascade'
    )
    

    @api.model
    def create(self, vals):
        """
        Sobrescribe el método create para que la fecha de última modificación
        sea igual a la fecha de creación al momento de crear un registro.
        """
        vals['last_modification_date'] = datetime.now()
        return super(Festivals, self).create(vals)
    
    def write(self, vals):
        """
        Actualiza el campo 'last_modification_date' al guardar cualquier cambio.
        """
        vals['last_modification_date'] = datetime.now()
        return super(Festivals, self).write(vals)