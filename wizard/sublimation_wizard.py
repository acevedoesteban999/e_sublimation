from odoo import fields,models,api

class SublimationWizard(models.TransientModel):
    _name = 'sublimation.wizard'
    _description = 'Product Product Wizard'

    name = fields.Char(string='Name', required=True)
    product_tmpl_sublimation_id = fields.Many2one('product.template', string='Product', required=True, domain=[('sublimation_ok','=',True)])
    file = fields.Binary(string='File')
    image_1920 = fields.Image("Image", max_width=1920, max_height=1920)
    price_extra = fields.Float(string='Extra Price', default=0.0)
    
    def action_create_sublimation(self):
        self.ensure_one()
        
        self.env['product.product'].create({
            'name': self.product_tmpl_sublimation_id.name + " " + self.name,
            'sublimation_ok':True,
            'product_tmpl_sublimation_id': self.product_tmpl_sublimation_id.id,
            'default_code': f'SUB-{self.id}',
            'list_price': self.product_tmpl_sublimation_id.list_price + self.price_extra,
            'price_extra': self.price_extra,
            'image_1920': self.image_1920,
            'file': self.file,
        })
        

        return {
            'type': 'ir.actions.act_window_close',
        }