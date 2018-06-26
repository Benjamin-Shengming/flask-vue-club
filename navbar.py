#!/usr/bin/python3
from collections import OrderedDict
from uuid import uuid1
import dash
import dash_html_components as html
import dash_core_components as dcc
'''
<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <a class="navbar-brand" href="#">Navbar w/ text</a>
  <button class="navbar-toggler" type="button"
            data-toggle="collapse"
            data-target="#navbarText"
            aria-controls="navbarText"
            aria-expanded="false"
            aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarText">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item active">
        <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#">Features</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#">Pricing</a>
      </li>
    </ul>
    <span class="navbar-text">
      Navbar text with an inline element
    </span>
  </div>
</nav>
'''
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

    def add_drop_menu(self, menu_name, menu_items):
        menu= html.Div(className="btn-group", children=[
            html.Button(menu_name, **{"data-toggle":"dropdown","aria-haspopup":"true","aria-expanded":"false"},className="btn btn-dark dropdown-toggle"),
            html.Div(className="dropdown-menu", children=[
                dcc.Link(item, className="dropdown-item" ,href="/"+menu_name + "/" + item, style={"cursor": "pointer"}) for item in menu_items
            ])
         ])
        self.drop_menus.append(menu)

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
        nav_bar_collapse = html.Div(className="navbar-collapse collapse", id=self.collapse_id,
                                    children=[nav_bar_links])



        nav_bar = html.Nav(className="navbar navbar-expand-md navbar-dark bg-dark",
                        children = [nav_bar_brand,
                                    nav_bar_sandwich_btn,
                                    nav_bar_collapse,
                                    ])
        return nav_bar
        #return html.Div(className="container", children=[nav_bar])


