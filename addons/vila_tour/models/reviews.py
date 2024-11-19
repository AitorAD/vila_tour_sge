# -*- coding: utf-8 -*-
from odoo import fields, models, api

class Reviews(models.Model):
    _name = "reviews"
    _description = "Review"
    _sql_constraints = [
        ('unique_user_article', 'unique(user_id, article_id)', 'Each user can only have one review per article.')
    ]

    user_id = fields.Many2one('res.users', string="User", required=True, ondelete='cascade')
    article_id = fields.Many2one('articles', string="Article", required=True, ondelete='cascade')
    rating = fields.Integer(string="Rating", required=True)
    comment = fields.Text(string="Comment")

