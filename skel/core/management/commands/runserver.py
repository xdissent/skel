from django.core.management.commands import runserver
import os
import signal
import subprocess
import time
import sys

class BrokenCommand(runserver.Command):    
    def handle(self, *args, **kwargs):
        server_proc = subprocess.Popen(['python -m smtpd -n -c DebuggingServer localhost:1025'], shell=True)
        open_proc = subprocess.Popen(['open http://localhost:8000/'], shell=True)
        try:
            super(Command, self).handle(*args, **kwargs)
        finally:
            # Shutdown server
            print 'Final shutdown'