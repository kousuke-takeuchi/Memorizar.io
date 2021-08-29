"""
WSGI config for memorizar project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

import newrelic.agent

from django.core.wsgi import get_wsgi_application


newrelic.agent.initialize(os.path.join(os.path.dirname(__file__), 'newrelic.ini'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'memorizar.settings')

application = get_wsgi_application()
application = newrelic.agent.wsgi_application()(application)