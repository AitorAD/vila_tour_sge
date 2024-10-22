# -*- coding: utf-8 -*-

from odoo import fields, models, api

class Recipes (models.Model):
    _name = "recipes"
    name = fields.Char()