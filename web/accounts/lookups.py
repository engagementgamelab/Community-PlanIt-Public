from .models import UserProfileStake

class StakesLookup(object):

    def get_query(self, q, request):
        """ return a query set."""
        return UserProfileStake

    def format_item(self, item):
        """ the display of a currently selected object in the area below the search box. html is OK """
        if isinstance(item.object, Physician):
            return u"%s" % (item.object.get_full_name())

    def format_result(self, item):
        """ the search results display in the dropdown menu.  may contain html and multiple-lines. will remove any |  """
        return self.format_item(item)

