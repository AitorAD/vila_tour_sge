# -*- coding: utf-8 -*-

from odoo import fields, models, api

class Reviews (models.Model):
    _name = "reviews"
    name = fields.Char()