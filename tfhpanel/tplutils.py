from tfhpanel.models import DBSession, Base, RootFactory, make_url

def get_root_panels():
    return RootFactory.children

def format_panel_value(value, panelview):
    if isinstance(value, bool):
        # &#x2714; HEAVY CHECK MARK / &#x2718; HEAVY BALLOT X
        # &#x25cf; BLACK CIRCLE / &#x25cb; WHITE CIRCLE
        boolvalue = '&#x2714;' if value else '&#x2718;'
        return '<span class="panel-value-bool">'+boolvalue+'</span>'
    
    if isinstance(value, list):
        items = []
        for vit in value:
            items.append(format_panel_value(vit, panelview))
        return ', '.join([o for o in items])
    
    if isinstance(value, Base):
        newpath = panelview.path[:]
        view = find_view(value)
        if view:
            v_ = None
            for i, v in enumerate(newpath):
                if view.parent is None or isinstance(v_, view.parent):
                    newpath[i] = view()
                    newpath[i].id = panelview.path[i].id
                v_ = v
            url = make_url(newpath, change_ids=value)
            return '<a href="%s">%s</a>'%(url, str(value))
        else:
            return str(value)

    return '<span class="panel-value">'+str(value)+'</span>'

def find_view(dbo, root=RootFactory.children):
    for v in root.values():
        if isinstance(dbo, v.model):
            return v
        elif v.children:
            r = find_view(dbo, v.children)
            if r:
                return r

