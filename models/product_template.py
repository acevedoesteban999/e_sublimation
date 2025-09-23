from odoo import fields,models,api

class ProductProduct(models.Model):
    _inherit = 'product.template'

    sublimation_ok = fields.Boolean(string='Sublimable')
    sublimation_ids = fields.One2many('sublimation.sublimation','product_tmpl_id','Sublimaciones')
    product_sublimation_count = fields.Integer(
        string='Total de Variantes',
        compute='_compute_total_attribute_line',
    )

    @api.depends('product_sublimation_count')
    def _compute_total_attribute_line(self):
        for rec in self:
            rec.product_sublimation_count = len(rec.sublimation_ids)

    def unlink(self):
        self.sublimation_ids.unlink()
        return super().unlink()

    