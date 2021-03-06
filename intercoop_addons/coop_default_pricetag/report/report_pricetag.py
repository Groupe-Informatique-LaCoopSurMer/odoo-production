# -*- coding: utf-8 -*-

from openerp import api, models


class ReportPricetagBase(models.AbstractModel):
    _name = 'report.coop_default_pricetag.report_pricetag_base'

    @api.model
    def _get_products(self, lines, fields):
        result = []
        line_ids = self.env['product.pricetag.wizard.line'].browse(lines)
        for line in line_ids:
            val = {}
            val['line'] = line
            val['product'] = line.product_id
            result.append(val)
        return result

    @api.multi
    def render_html(self, data):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))

        line_ids = data['form'].get('line_ids', [])
        fields = data['form'].get('fields', [])

        report_context = self._context.copy()
        report_context.update(data['form'].get('used_context', {}))
        product_res = self.with_context(report_context)._get_products(
            line_ids, fields)
        pricetag_model = self.env['product.category.print'].browse(
            data['form']['category_print_id']).pricetag_model_id
        report_model = pricetag_model.report_model

        docargs = {
            'doc_ids': self.ids,
            'partner_id': self.env.user.partner_id,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'Products': product_res,
        }
        return self.env['report'].render(
            report_model, docargs)


class ReportPricetag(models.AbstractModel):
    _name = 'report.coop_default_pricetag.report_pricetag'
    _inherit = 'report.coop_default_pricetag.report_pricetag_base'


class ReportPricetagBarcode(models.AbstractModel):
    _name = 'report.coop_default_pricetag.report_pricetag_barcode'
    _inherit = 'report.coop_default_pricetag.report_pricetag_base'


class ReportPricetagSimpleBarcode(models.AbstractModel):
    _name = 'report.coop_default_pricetag.report_pricetag_simple_barcode'
    _inherit = 'report.coop_default_pricetag.report_pricetag_base'
