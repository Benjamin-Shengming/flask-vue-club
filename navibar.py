
#!/usr/bin/python3
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
nav_bar_brand = html.A("HaoduoYu", className="navbar-brand")

nav_bar_sandwich_btn = html.Button(**{"data-toggle": "collapse",
                                      "data-target": "#navbarText",
                                      "aria-controls": "navbarText",
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
                           html.Li(className="nav-item active",
                                   children=dcc.Link("Home", href="/home", className="nav-link")),
                           html.Li(className="nav-item",
                                   children=dcc.Link("Orders", href="/orders",className="nav-link")),
                           html.Li(className="nav-item",
                                   children=dcc.Link("My Profile",href="/profile", className="nav-link")),
                       ])

nav_bar_collapse = html.Div(className="navbar-collapse collapse", id="navbarText",
                            children=[nav_bar_links])



nav_bar = html.Nav(className="navbar  navbar-expand-md  navbar-dark bg-primary",
                   children = [nav_bar_brand,
                               nav_bar_sandwich_btn,
                               nav_bar_collapse,
                               #nav_bar_text
                               ])

