# -*- coding: utf-8 -*-
from odoo import fields, models

class Recipes(models.Model):
    _name = "recipes"
    name = fields.Char(string="Nombre")
    rating = fields.Integer(string='Puntuación')
    description = fields.Text(string="Descripción")
    ingredients = fields.Many2many(
        comodel_name="ingredients",
        string="Ingredientes"
    )
    image = fields.Binary(string='Imagen', attachment=True)  # Asegura que "attachment=True" esté configurado.
    approved = fields.Boolean(string='Aprobada', default=True)
