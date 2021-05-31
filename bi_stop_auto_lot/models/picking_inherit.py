# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.


from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.tools.misc import split_every
from odoo import api, fields, models, registry, _

import logging
_logger = logging.getLogger(__name__)


class Stockpicking_inherit(models.Model):
    _inherit = "stock.picking"

    def action_assign(self):
        for picking in self:
            for line in picking.move_ids_without_package:
                if line.product_id.tracking == 'serial' or line.product_id.tracking == 'lot':
                    if self._context.get('from_sale') == True :
                        res = super(Stockpicking_inherit, self).action_assign()
                    else :
                        return
                else:
                    res = super(Stockpicking_inherit, self).action_assign()


class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'


    @api.model
    def _run_scheduler_tasks(self, use_new_cursor=False, company_id=False):
        # Minimum stock rules
        self.sudo()._procure_orderpoint_confirm(use_new_cursor=use_new_cursor, company_id=company_id)

        # Search all confirmed stock_moves and try to assign them
        domain = self._get_moves_to_assign_domain(company_id)
        moves_to_assign = self.env['stock.move'].search(domain, limit=None,
            order='priority desc, date_expected asc')
        for moves_chunk in split_every(100, moves_to_assign.ids):
            if use_new_cursor:
                self._cr.commit()

        if use_new_cursor:
            self._cr.commit()

        # Merge duplicated quants
        self.env['stock.quant']._quant_tasks()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: