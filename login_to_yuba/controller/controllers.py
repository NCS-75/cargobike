# -*- coding: utf-8 -*-
from odoo.http import request, route
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.portal.controllers.web import Home
from odoo import http, models, fields, _

class Website(Home):

    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        if not request.session.uid:
            return request.redirect('/web/login?redirect=/')
        else:
            homepage = request.website.homepage_id
            if homepage and (homepage.sudo().is_visible or request.env.user.has_group('base.group_user')) and homepage.url != '/':
                return request.env['ir.http'].reroute(homepage.url)

            website_page = request.env['ir.http']._serve_page()
            if website_page:
                return website_page
            else:
                top_menu = request.website.menu_id
                first_menu = top_menu and top_menu.child_id and top_menu.child_id.filtered(lambda menu: menu.is_visible)
                if first_menu and first_menu[0].url not in ('/', '', '#') and (not (first_menu[0].url.startswith(('/?', '/#', ' ')))):
                    return request.redirect(first_menu[0].url)

            raise request.not_found()

class Home(Home):

    def _login_redirect(self, uid, redirect=None):
        if not redirect and not request.env['res.users'].sudo().browse(uid).has_group('base.group_user'):
            return '/'
        return super(Home, self)._login_redirect(uid, redirect=redirect)
