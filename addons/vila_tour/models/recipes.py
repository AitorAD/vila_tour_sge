# -*- coding: utf-8 -*-
from odoo import fields, models, api

class Recipes(models.Model):
    _name = "recipes"
    _inherit = ['image.mixin']
    name = fields.Char(string="Nombre")
    rating = fields.Integer(string='Puntuación')
    description = fields.Text(string="Descripción")
    ingredients = fields.Many2many(
        comodel_name="ingredients",
        string="Ingredientes"
    )
    approved = fields.Boolean(string='Aprobada', default=True)
