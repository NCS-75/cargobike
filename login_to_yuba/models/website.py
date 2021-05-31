from odoo import fields, api, models, _

class WebsitePage(models.Model):

	_inherit = 'website.page'

	user_login_reqired = fields.Boolean(string="User Login Required")

class WebsiteMenu(models.Model):

	_inherit = "website.menu"

	user_login_reqired = fields.Boolean(string="User Login", compute="onchangeUserLogin")	

	@api.depends('page_id.user_login_reqired')
	def onchangeUserLogin(self):	
		if self.page_id.user_login_reqired == True:
			self.user_login_reqired = True
		else:
			self.user_login_reqired = False