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


# Main page request handler
class Main(BaseRequestHandler):
    def get(self):
        # Render the template
        self.render("index.html")

class NotFound(BaseRequestHandler):
    def get(self):
        self.error404()
        
    def post(self):
        self.error404()