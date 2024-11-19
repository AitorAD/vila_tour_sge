# -*- coding: utf-8 -*-
from odoo import fields, models

class Categories(models.Model):
    _name = "categories"
    name = fields.Char(string="Nombre")
