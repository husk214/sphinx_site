# -*- coding: utf-8 -*-
import os
from docutils.parsers.rst import roles

def _define_role(name):
#    print "sphinxcontrib_roles#_define_role name:", name
    #=> strike, red
    base_role = roles.generic_custom_role
    role = roles.CustomRole(name, base_role, {'class': [name]}, [])
    roles.register_local_role(name, role)

def on_builder_inited(app):
#    print "sphinxcontrib_roles#onbuilder_inited item", app.builder.config.roles.items()
    #=> [('strike', 'text-decoration: line-through;'), ('red', 'color: red;')]
    for name in app.builder.config.roles:
        _define_role(name)

def on_html_collect_pages(app):
    if isinstance(app.builder.config.roles, dict) and app.builder.config.roles:
        cssdir = os.path.join(app.builder.outdir, '_static')
        cssfile = os.path.join(cssdir, 'roles.css')
        if not os.path.exists(cssdir):
            os.makedirs(cssdir)

        fd = open(cssfile, 'wt')
#        print "sphinxcontrib_roles#on_html_collect_pages write cssfile", cssfile
        #=> C:\work\sphinx\_build\html\_static\roles.css
        for name, style in app.builder.config.roles.items():
            fd.write("span.%s { %s }\n" % (name, style))
        fd.close()
    return ()

def html_page_context(app, pagename, templatename, context, doctree):
    if isinstance(app.builder.config.roles, dict) and app.builder.config.roles:
        if 'css_files' in context:
#            print "sphinxcontrib_roles#html_page_context pagename", pagename
            context['css_files'].append('_static/roles.css')

def setup(app):
    print "sphinxcontrib_roles#setup"
    app.add_config_value('roles', [], 'html')
    app.connect("builder-inited", on_builder_inited)
    app.connect("html-collect-pages", on_html_collect_p
