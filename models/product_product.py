from odoo import fields,models,api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    attachment_ids = fields.Many2many(
        'ir.attachment',
        string="Attachments",
        compute='_compute_attachment_ids',
        store=False
    )

    def _compute_attachment_ids(self):
        for product in self:
            product.attachment_ids = self.env['ir.attachment'].search([
                ('res_model', '=', 'product.product'),
                ('res_id', '=', product.id)
            ])

    def _compute_display_name(self):
        self.ensure_one()
        display_name = super()._compute_display_name()
        if self.sublimation_ok and self.product_tmpl_sublimation_id:
            display_name = self.product_tmpl_sublimation_id.name + " " + self.name
        return display_name


    def open_product_template(self):
        self.ensure_one()
        if self.sublimation_ok and self.product_tmpl_sublimation_id:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'product.template',
                'view_mode': 'form',
                'res_id': self.product_tmpl_sublimation_id.id,
                'target': 'new'
            }
        return super().open_product_template()
    
    def action_open_sublimation_attachment_wizard(self):
        return {
            'name': 'Create Sublimation Attachments',
            'type': 'ir.actions.act_window',
            'res_model': 'sublimation.attachment.wizard',
            'view_mode': 'form',
            'target': 'new',
            'views': [(self.env.ref('e_sublimation.sublimation_attachment_wizard_view_form').id,'form')],
            'context': {'default_product_tmpl_sublimation_id': self.id}
        }

    

    
    @api.depends('product_template_attribute_value_ids')
    def _compute_combination_indices(self):
        for product in self:
            if product.sublimation_ok and self.product_tmpl_sublimation_id:
                product.combination_indices = f"{product.name.lower().replace(' ','_')}_{product.product_tmpl_sublimation_id.id}"
            else:
                product.combination_indices = product.product_template_attribute_value_ids._ids2str()
