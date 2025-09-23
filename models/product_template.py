from odoo import fields,models,api

class ProductProduct(models.Model):
    _inherit = 'product.template'

    sublimation_ok = fields.Boolean(string='Sublimable')
    design_ids = fields.One2many('sublimation.design','product_tmpl_id','Diseños')
    total_designs = fields.Integer(
        string='Total de Variantes',
        compute='_compute_total_attribute_line',
    )

    @api.depends('total_designs')
    def _compute_total_attribute_line(self):
        for rec in self:
            rec.total_designs = len(rec.total_designs)

    def unlink(self):
        self.design_ids.unlink()
        return super().unlink()

    