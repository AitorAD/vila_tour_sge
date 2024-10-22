# -*- coding: utf-8 -*-

from odoo import fields, models, api

class Festivals (models.Model):
    _name = "festivals"
    name = fields.Char()