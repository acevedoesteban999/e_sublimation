from odoo import fields, models

class SublimationAttributeLine(models.Model):
    _name = 'sublimation.attribute'
    _description = 'Línea de atributo de sublimación'

    design_id = fields.Many2one('sublimation.design')
    attribute_id = fields.Many2one('product.attribute', string='Atributo (talla, color, etc.)')
    value_ids = fields.Many2many('product.attribute.value', string='Valores')