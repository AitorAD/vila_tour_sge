# -*- coding: utf-8 -*-

from odoo import fields, models, api

class Places (models.Model):
    _name = "places"
    name = fields.Char()