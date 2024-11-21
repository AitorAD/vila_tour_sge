# -*- coding: utf-8 -*-
from odoo import fields, models, api
from datetime import datetime

class Recipes(models.Model):
    _name = "recipes"
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
    
    approved = fields.Boolean(string='Aprobada', default=True)
    recent = fields.Char()
    ingredients = fields.Many2many(
        comodel_name="ingredients",
        string="Ingredientes"
    )

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
        return super(Recipes, self).create(vals)
    
    def write(self, vals):
        """
        Actualiza el campo 'last_modification_date' al guardar cualquier cambio.
        """
        vals['last_modification_date'] = datetime.now()
        return super(Recipes, self).write(vals)
    