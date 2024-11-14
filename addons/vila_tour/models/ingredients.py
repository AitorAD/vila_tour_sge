# -*- coding: utf-8 -*-

from odoo import fields, models, api

class Ingredients(models.Model):
    _name = "ingredients"
    name = fields.Char(string="Nombre")
    category_id = fields.Many2one(
        comodel_name="categories",
        string="Categoría"
    )