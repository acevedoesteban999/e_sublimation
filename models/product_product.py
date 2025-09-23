from odoo import fields,models,api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    design_id = fields.Many2one('sublimation.design',compute="_compute_design")

    def _compute_display_name(self):
        self.ensure_one()
        display_name = super()._compute_display_name()
        if self.sublimation_ok:
            display_name = self.product_tmpl_id.name + " " + self.design_id.name
        return display_name


    def open_product_template(self):
        self.ensure_one()
        if self.sublimation_ok:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'product.template',
                'view_mode': 'form',
                'res_id': self.design_id.product_tmpl_id.id,
                'target': 'new'
            }
        return super().open_product_template()
    
    def _compute_design(self):
        for rec in self:
            rec.design_id = self.env['sublimation.design'].search([('product_product_id','=',rec.id)])

    
    @api.depends('product_template_attribute_value_ids')
    def _compute_combination_indices(self):
        for product in self:
            if product.sublimation_ok:
                product.combination_indices = f"{product.name.lower().replace(" ",'_')}_{product.design_id.id}"
            else:
                product.combination_indices = product.product_template_attribute_value_ids._ids2str()