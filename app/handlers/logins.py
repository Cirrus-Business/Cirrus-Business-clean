# -*- coding: utf-8 -*-
import os
import logging
import webapp2

from hashlib import md5
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template


# Import packages from the project


from models import *
from baserequesthandler import BaseRequestHandler
from tools.common import decode
from tools.decorators import login_required, admin_required

providers = {
    'Google'   : 'https://www.google.com/accounts/o8/id',
    'Yahoo'    : 'yahoo.com',
    'MySpace'  : 'myspace.com',
    'AOL'      : 'aol.com',
    'MyOpenID' : 'myopenid.com'
    # add more here
}
# OpenID login
class LogIn(BaseRequestHandler):
    """
    Redirects a user to the OpenID login site. After successful login the user
    redirected to the target_url (via /login?continue=/<target_url>).
    """
    def get(self):
        user = users.get_current_user()
        if user:  # signed in already
            self.response.out.write('Hello <em>%s</em>! [<a href="%s">sign out</a>]' % (
                user.nickname(), users.create_logout_url(self.request.uri)))
        else:     # let user choose authenticator
            self.response.out.write('Hello world! Sign in at: ')
            for name, uri in providers.items():
                self.response.out.write('[<a href="%s">%s</a>]' % (
                    users.create_login_url(federated_identity=uri), name))        
            
# LogOut redirects the user to the GAE logout url, and then redirects to /
class LogOut(webapp.RequestHandler):
    def get(self):
        url = users.create_logout_url("/")
        self.redirect(url) 

 
 
# Account page and after-login handler
class Account(BaseRequestHandler):
    """
    The user's account and preferences. After the first login, the user is sent
    to /account?continue=<target_url> in order to finish setting up the account
    (email, username, newsletter).
    """
    def get(self):
        target_url = decode(self.request.get('continue'))
        # Circumvent a bug in gae which prepends the url again
        if target_url and "?continue=" in target_url:
            target_url = target_url[target_url.index("?continue=") + 10:]
 
        if not self.userprefs.is_setup:
            # First log in of user. Finish setup before forwarding.
            self.render("account_setup.html", {"target_url": target_url, 'setup_uri':self.uri_for('setup')})
            return
 
        elif target_url:
            # If not a new user but ?continue=<url> supplied, redirect
            self.redirect(target_url)
            return
 
        # Render the account website
        self.render("account.html", {'setup_uri':self.uri_for('setup')})
 
 
class AccountSetup(BaseRequestHandler):
    """Initial setup of the account, after user logs in the first time"""
    def post(self):
        username = decode(self.request.get("username"))
        email = decode(self.request.get("email"))
        subscribe = decode(self.request.get("subscribe"))
        target_url = decode(self.request.get('continue'))
        target_url = target_url or self.uri_for('account')
 
        # Set a flag whether newsletter subscription setting has changed
        subscription_changed = bool(self.userprefs.subscribed_to_newsletter) \
                is not bool(subscribe)
 
        # Update UserPrefs object
        self.userprefs.is_setup = True
        self.userprefs.nickname = username
        self.userprefs.email = email
        self.userprefs.email_md5 = md5(email.strip().lower()).hexdigest()
        self.userprefs.subscribed_to_newsletter = bool(subscribe)
        self.userprefs.put()
 
    
        # After updating UserPrefs, redirect
        self.redirect(target_url)
 