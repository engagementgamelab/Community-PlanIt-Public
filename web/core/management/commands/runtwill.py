import time
from django.core.management.base import BaseCommand

from web.core.twill_utils import twill_browser

import logging
log = logging.getLogger(__name__)

class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):
        t1 = time.time()
        b = twill_browser()
        page = b.login_to_game()
        #print page
        assert "You have not registered for this instance." not in page, "player not registered"
        assert "Please enter a correct username and password." not in page, "incorrect username or password"

        #b.soup=BeautifulSoup.BeautifulSoup(page)

        t2 = time.time()
        log.debug("ran twill tests in %s sec." %(t2-t1))
