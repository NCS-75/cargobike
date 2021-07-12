from odoo.exceptions import UserError
from odoo import models, fields, api



#class purchase_order(models.Model):
#    _inherit = 'stock.move'
#    state = fields.Selection(selection_add=[('merge', "merge")])

    #def action_quotation_approve(self):
     #   self.state = 'merge'

class StockPicking(models.Model):
    _inherit = "stock.picking"
    merge_in = fields.Char(string="Merge in")
    is_merged = fields.Boolean(string="Is merged ?", default=False)
    #sale_ids = fields.One2many('merge.pickingline', 'sale_id')

class StockMoveLine(models.Model):
    _inherit = "stock.move.line"
    importednum = fields.Boolean(string="Imported num", default=False)


class MergePicking(models.TransientModel):
    _name = 'merge.picking'

    merge_picking_line = fields.One2many('merge.pickingline','partner_id',string="New Line")

    @api.model
    def default_get(self, vals):
        res = super(MergePicking,self).default_get(vals)
        picking_obj = self.env['stock.picking']
        stock_ids=self.env.context.get('active_ids')
        stock_vals=[]
        stock_info=picking_obj.browse(stock_ids)
        test = 'TNT'
        for stock in stock_info:
            if stock.state=='done':
                    raise UserError(('Merging is not allowed on done picking.'))			
            stock_vals.append((0,0,{
            'pick_name':stock.name,
            'partner_id':stock.partner_id.id,
            'origin':stock.origin,
            'state':stock.state,
            'carrier_id':stock.carrier_id.id,
            'sale_id': stock.sale_id.id
            }))

            res.update({'merge_picking_line': stock_vals})
        return res


    def Create_new_picking_record(self):
        picking_obj = self.env['stock.picking']
        wizard_stock=self.env.context.get('active_ids')
        if len(wizard_stock)==1:
            raise UserError(('Please select multiple picking to create a list view.'))	
        stock_info=picking_obj.browse(wizard_stock)
        partner_list=[]
        carrier_list=[]
        state_list=[]
        picking_type_list=[]
        merge_list = []
        for partner_li in stock_info:
            partner_list.append(partner_li.partner_id.id)
        for carrier_li in stock_info:
            carrier_list.append(carrier_li.carrier_id.id)
        for picking_type_li in stock_info:
            picking_type_list.append(picking_type_li.picking_type_id.id)
        for state_li in stock_info:
            state_list.append(state_li.state)
        if state_list[1:] != state_list[:-1]:
            raise UserError(('Merging is only allowed on picking of same state'))
        if stock_info:
            move_line_val=[]
            origin=''
            for info in stock_info:
                if partner_list[0] !=info.partner_id.id :
                    raise UserError(('Merging is only allowed on picking of same partner.'))
                if picking_type_list[0] !=info.picking_type_id.id :
                    raise UserError(('Merging is only allowed on picking of same Types.'))
                if carrier_list[0] !=info.carrier_id.id :
                    raise UserError(('Merging is only allowed on same carrier.'))
                if origin:
                    origin = origin + '-' + '('+ info.origin + ')'+ info.name
                else:
                    origin = '('+ info.origin + ')'+ info.name
                for product_line in info.move_lines:
                    move_line_val.append((0,0,{
                        'product_id':product_line.product_id.id,
                        'product_uom_qty':product_line.product_uom_qty,
                        'state':'confirmed',#product_line.state,
                        'product_uom':product_line.product_id.uom_id.id,
                        'name':product_line.product_id.name,
                        'date_expected':product_line.date_expected
                        }))
                #info.action_cancel()
                merge_list.append(info.id) 

                #info.merge_in = str(picking.name) 
                info.is_merged = True
                self.env.cr.execute('select last_value from ir_sequence_091')
                id_returned = self.env.cr.fetchone()
                last_value = int(id_returned[0]) + 1
                self.env.cr.execute('select sequence_code from stock_picking_type where id=' + str(picking_type_list[0]))
                code = self.env.cr.fetchone()
                info.merge_in = "ECTRA/" + str(code[0]) + "/" + str(last_value)
                
            vals={
            'partner_id':stock_info[0].partner_id.id,
            'origin':origin,
            'scheduled_date':stock_info[0].scheduled_date,
            'move_lines':move_line_val,
            'move_type':stock_info[0].move_type,
            'picking_type_id':stock_info[0].picking_type_id.id,
            'priority':stock_info[0].priority,
            'location_id':stock_info[0].location_id.id,
            'location_dest_id':stock_info[0].location_dest_id.id,
            'carrier_id':stock_info[0].carrier_id.id,
            'sale_id':stock_info[0].sale_id.id,
            'state': 'draft'
            }
            #TODO VERIFIE QUE TOUS LES QUANTS SONT BIEN ANNULES SUR LES BP PRECEDENTS VOIR SI POSSIBLE DE LES RECCUP
            picking = picking_obj.create(vals)
            for old_picking in merge_list: #
                self.env.cr.execute('select MAX(id) from stock_picking')
                id_returned = self.env.cr.fetchone()
                last_value = int(id_returned[0])
                self.env.cr.execute('DELETE from stock_move_line where picking_id ='+ str(old_picking) +';')
                #self.env.cr.execute('update stock_move_line set picking_id =' + str(last_value) + ' where picking_id ='+ str(old_picking) +';')
            #info.note = str(info.note)  + str(picking.name)
            

        return True

class MergePickingLine(models.Model):
    _name='merge.pickingline'


    partner_id = fields.Many2one(
        'res.partner', 'Partner',
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]})

    origin = fields.Char(
        'Source Document', index=True,
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
        help="Reference of the document")	

    pick_name=fields.Char('Reference')
    carrier_id = fields.Many2one("delivery.carrier", 'Carrier',
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]})
    sale_id = fields.Char(
        'Source Document id', index=True,
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
        help="id of the document")
    picking_id = fields.Char(
        'new Document id', index=True,
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
        help="id of the document")	        
    state = fields.Selection([
        ('draft', 'Draft'), ('cancel', 'Cancelled'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting Availability'),
        ('partially_available', 'Partially Available'),
        ('assigned', 'Available'), ('done', 'Done')], string='Status', compute='_compute_state',
        copy=False, index=True, readonly=True, store=True, track_visibility='onchange',
        help=" * Draft: not confirmed yet and will not be scheduled until confirmed\n"
             " * Waiting Another Operation: waiting for another move to proceed before it becomes automatically available (e.g. in Make-To-Order flows)\n"
             " * Waiting Availability: still waiting for the availability of products\n"
             " * Partially Available: some products are available and reserved\n"
             " * Ready to Transfer: products reserved, simply waiting for confirmation.\n"
             " * Transferred: has been processed, can't be modified or cancelled anymore\n"
             " * Cancelled: has been cancelled, can't be confirmed anymore")


	

   
