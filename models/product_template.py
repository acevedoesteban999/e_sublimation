from odoo import fields,models

class ProductProduct(models.Model):
    _inherit = 'product.template'

    is_sublimation = fields.Boolean(string='Sublimable')