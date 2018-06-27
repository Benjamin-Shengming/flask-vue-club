#!/usr/bin/python3
from collections import OrderedDict
from uuid import uuid1
import dash
import dash_html_components as html
import dash_core_components as dcc

sider_bar = html.Div(className="col-md-3 float-left col-1 pl-0 pr-0 collapse width show", id="sidebar", children=[
                html.Div(className="list-group border-0 card text-center text-md-left")
                html.A(**{"data-toggle":"collapse", "aria-expanded":"false"}, href="#menu1", className="list-group-item d-inline-block collapsed", children=[
                    html.I(className="fa fa-dashboard")
                    html.Span("Item 1", className="d-none d-md-inline")
                ])
                html.Div(**{"data-parent":"#sidebar"}, className="collapse", id="menu1", children=[
                    html.A("Subitem 1", **{"data-toggle":"collapse", "aria-expanded":"false"}, href="#menu1sub1" className="list-group-item")
                    html.Div(className="collapse", id="menu1sub1", **{"data-parent":"#menu1"}, children=[
                        html.A("subitem a", **{"data-parent":"#menu1sub1"}, href="#", className="list-group-item")
                        html.A("subitem b", **{"data-parent":"#menu1sub1"}, href="#", className="list-group-item")
                        html.A("subitem c", **{"data-toggle":"collapse","aria-expanded":"false"}, href="#menu1sub1sub1", className="list-group-item")
                        html.Div(className="collapse", id="menu1sub1sub1", children=[
                            html.A("Subitem c.1", **{"data-parent": '#menu1sub1sub1'}, href="#", className="list-group-item")
                            html.A("subitme c.2", **{"data-parent":"#menu1sub1sub1"}, href="#", className="list-group-item")
                        ])
                    ])
                    html.A("SubItem 3", href="#", className="list-group-item")
                ])
                html.A(href="#", className="list-group-item d-inline-block collapsed", children=[
                    html.I(className="fa fa-film")
                    html.Span("item 2", className="d-none d-md-inline")
                ])
                html.A(**{"data-toggle":"collapse","aria-expanded":"false"}, href="#menu3", className="list-group-item d-inline-block collapsed", children=[
                    html.I(className="fa fa-book")
                    html.Span("Item 3", className="d-none d-md-inline")
                ])
                html.Div(**{"data-parent":'#sidebar'}, className="collapse", id="menu3", children=[
                    html.A("3.1", **{"data-parent"='#menu3'}, href="#", className="list-group-item")
                    html.A("3.2", **{"data-toggle":"collapse","aria-expanded":"false"}, href="#menu3sub2",className="list-group-item")
                    html.Div(className="collapse", id="menu3sub2", children=[
                       html.A("3.2.a", **{"data-parent":"#menu3sub2"}, href="#", className="list-group-item")
                       html.A("3.2.b", **{"data-parent":"#menu3sub2"}, href="#", className="list-group-item")
                       html.A("3.2.c", **{"data-parent":"#menu3sub2"}, href="#", className="list-group-item")
                    ])
                    html.A("3.3",**{"data-parent":"#menu3"}, href="#", className="list-group-item")
                ])

])


main_area = html.Main(className="col-md-9 float-left col px-5 pl-md-2 pt-2 main", children=[
                html.A(**{"data-target":"#sidebar", "data-toggle":"collapse"}, href="#", children=[
                    html.I(className="fa fa-navicon fa-2x py-2 p-1")
                ])
                html.Div(className="page-header", children=[
                    html.H2("Bootstrap 4 Sidebar Menu")
                ])
                html.P("A responsive, multi-level vertical accordion.", className="lead")
                html.Hr()
                html.Div(className="row", children=[
                    html.Div(className="col-lg-6", children=[
                        html.Button("horizontal  collapsible", **{"data-toggle":"collapse","data-target":'#demo',"aria-expanded":"true"}, role="button", className="btn btn-danger")
                        html.Div(**{"aria-expanded":"true"}, id="demo", className="width collapse show")
                            html.Div(className="list-group", style="width:400px", children=[
                                html.P("Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.")
                                html.P("Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.")
                            ])
                    ])
                    html.Div(className="col-lg-6", children=[
                        html.Button("vertical collapsible", role="button", className="btn btn-danger" **{"data-toggle":"collapse", "data-target":"#demo2", "aria-expanded":"true"})
                        html.Div(id="demo2",className="height collapse show" **{"aria-expanded":"true"})
                            html.Div(children=[
                                html.P("Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.")
                                html.P("Cras justo odio, dapibus ac facilisis in, egestas eget quam. Donec id elit non mi porta gravida at eget metus. Nullam id dolor id nibh ultricies vehicula ut id elit.")
                            ])
                    ])
                ])
])

html.Div(className="container-fluid", children=[
    html.Div(className="row d-flex d-md-block flex-nowrap wrapper", children=[
        sider_bar,
        main_area
    ])
])
'''
class SideBar(object):
    def __init__(self, brand_name="HaoduoYu", bg_color="bg-primary", navbar_color="navbar-dark"):
        self.brand_name = brand_name
        self.bg_color = bg_color
        self.navbar_color = navbar_color
        self.links = OrderedDict()
        self.collapse_id = str(uuid1())

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


