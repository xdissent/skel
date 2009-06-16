from django.core.management.commands import runserver
import os
import signal
import subprocess
import time
import sys

class Command(runserver.Command):    
    def handle(self, *args, **kwargs):
        server_proc = subprocess.Popen(['python -m smtpd -n -c DebuggingServer localhost:1025'], shell=True)
        try:
            super(Command, self).handle(*args, **kwargs)
        finally:
            # Shutdown server
            print 'Final shutdown'