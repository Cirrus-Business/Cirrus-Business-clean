# -*- coding: utf-8 -*-

import webapp2, handlers

# Map url's to handlers
urls = [
    webapp2.Route(r'/', handler=handlers.Main, name="home"),
    webapp2.Route(r'/login', handler=handlers.LogIn, name="login"),
    webapp2.Route(r'/_ah/login_required', handler=handlers.LogIn),
    webapp2.Route(r'/logout', handler=handlers.LogOut, name="logout"),
    webapp2.Route(r'/account', handler=handlers.Account, name="account"),
    webapp2.Route(r'/account/setup', handler=handlers.AccountSetup, name="setup"),
    (r'.*', handlers.NotFound)
]
