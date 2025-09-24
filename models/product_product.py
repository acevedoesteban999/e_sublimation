from odoo import fields,models,api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    file = fields.Binary(string='File')
    
    def _compute_display_name(self):
        self.ensure_one()
        display_name = super()._compute_display_name()
        if self.sublimation_ok:
            display_name = self.product_tmpl_sublimation_id.name + " " + self.name
        return display_name


    def open_product_template(self):
        self.ensure_one()
        if self.sublimation_ok:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'product.template',
                'view_mode': 'form',
                'res_id': self.product_tmpl_sublimation_id.id,
                'target': 'new'
            }
        return super().open_product_template()
    
    

    
    @api.depends('product_template_attribute_value_ids')
    def _compute_combination_indices(self):
        for product in self:
            if product.sublimation_ok and self.product_tmpl_sublimation_id:
                product.combination_indices = f"{product.name.lower().replace(" ",'_')}_{product.product_tmpl_sublimation_id.id}"
            else:
                product.combination_indices = product.product_template_attribute_value_ids._ids2str()
