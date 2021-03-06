import sys
from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    help = "Provides feedback about the current Haystack setup."
    
    def handle_noargs(self, **options):
        """Provides feedback about the current Haystack setup."""
        # Cause the default site to load.
        from django.conf import settings
        __import__(settings.ROOT_URLCONF)
        from haystack import site
        
        print
        print "WARNING: This will irreparably remove EVERYTHING from your search index."
        print "Your choices after this are to restore from backups or rebuild via the `reindex` command."
        
        yes_or_no = raw_input("Are you sure you wish to continue? [y/N] ")
        print
        
        if not yes_or_no.lower().startswith('y'):
            print "No action taken."
            sys.exit()
        
        print "Removing all documents from your index because you said so."
        
        from haystack import backend
        sb = backend.SearchBackend()
        sb.clear()
        
        print "All documents removed."
