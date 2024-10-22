# -*- coding: utf-8 -*-

from odoo import fields, models, api

class Reports (models.Model):
    _name = "reports"
    name = fields.Char()