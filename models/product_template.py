from odoo import fields,models,api

class ProductProduct(models.Model):
    _inherit = 'product.template'

    sublimation_ok = fields.Boolean(string='Sublimable')
    sublimation_ids = fields.One2many('sublimation.sublimation','product_tmpl_id','Sublimaciones')
    product_sublimation_count = fields.Integer(
        string='Total de Variantes',
        compute='_compute_total_attribute_line',
    )

    sublimation_id = fields.Many2one('sublimation.sublimation')
    product_tmpl_sublimation_id = fields.Many2one('product.template', 'Product Template Sublimation',compute="_compute_product_tmpl_sublimation_id")
    
    def _compute_product_tmpl_sublimation_id(self):
        for rec in self:
            rec.product_tmpl_sublimation_id = rec.sublimation_id.product_tmpl_id
    

    @api.depends('product_sublimation_count')
    def _compute_total_attribute_line(self):
        self._create_variant_ids()
        for rec in self:
            rec.product_sublimation_count = len(rec.sublimation_ids)

    def unlink(self):
        self.sublimation_ids.unlink()
        return super().unlink()

    