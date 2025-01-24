# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime

class Recipes(models.Model):
    _name = "recipes"
    _inherit = ['image.mixin']

    name = fields.Char(string="Name", required=True, placeholder="Recipe Name", help="Enter the recipe name")
    description = fields.Text(string="Description", help="Provide a detailed description of the recipe")
    image = fields.Image(string="Image", max_width=1024, max_height=1024, help="Upload an image of the recipe")
    creation_date = fields.Datetime(
        string="Creation Date",
        default=lambda self: fields.Datetime.now(),
        readonly=True
    )
    last_modification_date = fields.Datetime(
        string="Last Modification Date",
        default=lambda self: fields.Datetime.now(),
        readonly=True
    )
    average_score = fields.Float(string="Average Score", default=0.0, help="Average rating of the recipe")
    approved = fields.Boolean(string='Approved', default=False)
    is_recent = fields.Boolean(
        string="Is Recent?",
        compute="_compute_is_recent",
        help="Computed field indicating if the recipe was recently created."
    )
    ingredients = fields.Many2many(
        comodel_name="ingredients",
        string="Ingredients",
        help="Select the ingredients for this recipe"
    )
    creator_id = fields.Many2one(
        comodel_name='res.users',
        string='Creator',
        ondelete='cascade',
        default=lambda self: self.env.uid,
        help="The user who created this recipe"
    )

    @api.depends('creation_date')
    def _compute_is_recent(self):
        for record in self:
            record.is_recent = (datetime.now() - record.creation_date).days <= 7

    @api.onchange('average_score')
    def _onchange_average_score(self):
        if self.average_score < 0 or self.average_score > 5:
            return {
                'warning': {
                    'title': _("Invalid Average Score"),
                    'message': _("The average score must be between 0 and 5."),
                }
            }

    @api.model
    def create(self, vals):
        vals['last_modification_date'] = datetime.now()
        vals['creator_id'] = self.env.uid
        return super(Recipes, self).create(vals)

    def write(self, vals):
        vals['last_modification_date'] = datetime.now()
        return super(Recipes, self).write(vals)

    _sql_constraints = [
        ('unique_recipe_name', 'unique(name)', "The recipe name must be unique."),
    ]

    @api.constrains('name')
    def _check_name_length(self):
        for record in self:
            if len(record.name) < 3:
                raise ValidationError("The recipe name must be at least 3 characters long.")