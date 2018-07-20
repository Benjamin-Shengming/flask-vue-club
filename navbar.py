#!/usr/bin/python3
from collections import OrderedDict
from uuid import uuid1
import dash
import dash_html_components as html
import dash_core_components as dcc
from  magic_defines import locale_d
import gettext
zh = gettext.translation("navbar", locale_d(), languages=["zh_CN"])
zh.install(True)
_ = zh.gettext

class NavBarLinks(object):
    def __init__(self, brand_name="HaoduoYu", bg_color="bg-primary", navbar_color="navbar-dark"):
        self.brand_name = brand_name
        self.bg_color = bg_color
        self.navbar_color = navbar_color
        self.links = OrderedDict()
        self.collapse_id = str(uuid1())
    def add_links(self, name, ref):
        self.links[name] = ref

    def components_tree(self):

        nav_bar_brand = html.A(self.brand_name, className="navbar-brand")

        nav_bar_sandwich_btn = html.Button(**{"data-toggle": "collapse",
                                            "data-target": "#"+self.collapse_id,
                                            "aria-controls": self.collapse_id,
                                            "aria-expanded": "false",
                                            "aria-label": "Toggle navigation",
                                            "type": "button"},
                                            id="idShowOrHideLink",
                                            className="navbar-toggler",
                                            children=[
                                                html.Span(className="navbar-toggler-icon")
                                            ])

        nav_bar_links = html.Ul(className="navbar-nav mr-auto",
                            children=[
                                html.Li(className="nav-item", children=dcc.Link(key, href=value, className="nav-link", style={"cursor":"pointer"}))
                                for key, value in self.links.items()
                            ])
        nav_bar_collapse = html.Div(className="navbar-collapse collapse", id=self.collapse_id,
                                    children=[nav_bar_links])



        nav_bar = html.Nav(className="navbar  navbar-expand-md  navbar-dark bg-primary",
                        children = [nav_bar_brand,
                                    nav_bar_sandwich_btn,
                                    nav_bar_collapse,
                                    ])
        return nav_bar

class NavBarDropMenu(object):
    def __init__(self, brand_name="HaoduoYu", bg_color="bg-primary", navbar_color="navbar-dark"):
        self.brand_name = brand_name
        self.bg_color = bg_color
        self.navbar_color = navbar_color
        self.links = OrderedDict()
        self.collapse_id = str(uuid1())
        self.drop_menus  = []
        self.shop_cart = None
        self.shop_order = None
        self.buttons = []
    def add_drop_menu(self, menu_name, menu_items, item_links):
        menu= html.Div(className="btn-group", children=[
            html.Button(menu_name, **{"data-toggle":"dropdown","aria-haspopup":"true","aria-expanded":"false"},className="btn btn-dark dropdown-toggle"),
            html.Div(className="dropdown-menu", children=[
                dcc.Link(item, className="dropdown-item" ,href=item_link, style={"cursor": "pointer"}) for item, item_link in zip(menu_items, item_links)
            ])
         ])
        self.drop_menus.append(menu)

    def add_shop_cart_button(self, shop_cart_id):
        self.shop_cart = dcc.Link(href="/shop/cart", className="btn btn-outline-info", children=[
            html.I(_("Cart"),id=shop_cart_id, className="fa fa-shopping-cart")
        ])

    def add_shop_order_button(self, shop_order_id):
        self.shop_order = dcc.Link(href="/shop/order", className="btn btn-outline-info", children=[
            html.I(_("Order"),id=shop_order_id, className="fas fa-shipping-fast")
        ])

    def add_button(self, button_id, button_text):
        self.buttons.append(html.Button(id=button_id,
                                      className="btn btn-outline-info",
                                      children=[ html.I(button_text)]))
        self.buttons.append(html.Span("  "))
    def components_tree(self):

        nav_bar_brand = html.A(self.brand_name, className="navbar-brand text-white")

        nav_bar_sandwich_btn = html.Button(**{"data-toggle": "collapse",
                                            "data-target": "#"+self.collapse_id,
                                            "aria-controls": self.collapse_id,
                                            "aria-expanded": "false",
                                            "aria-label": "Toggle navigation",
                                            "type": "button"},
                                            id="idShowOrHideLink",
                                            className="navbar-toggler",
                                            children=[
                                                html.Span(className="navbar-toggler-icon")
                                            ])

        nav_bar_links = html.Ul(className="navbar-nav mr-auto", children=self.drop_menus)
        collapse_children = [nav_bar_links]
        collapse_children.extend(self.buttons)
        collapse_children.extend([self.shop_cart, html.Span("  "), self.shop_order])
        nav_bar_collapse = html.Div(className="navbar-collapse collapse",
                                    id=self.collapse_id,
                                    children=collapse_children)



        nav_bar = html.Nav(className="navbar navbar-expand-md navbar-dark bg-dark",
                        children = [nav_bar_brand,
                                    nav_bar_sandwich_btn,
                                    nav_bar_collapse,
                                    ])
        return nav_bar
        #return html.Div(className="container", children=[nav_bar])


