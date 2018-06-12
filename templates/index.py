from browser import document, alert

# bind event 'click' on button to function echo

def echo(ev):
    alert(document["idServiceList"].id)


document["idServiceList"].bind("click", echo)
