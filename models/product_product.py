from odoo import fields,models

class ProductProduct(models.Model):
    _inherit = 'product.product'

    sublimation_design_id = fields.Many2one('sublimation.design', string='Diseño')
