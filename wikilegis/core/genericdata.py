from wikilegis.auth2.models import User


class BillAuthorData(object):
    def __init__(self, obj):
        self.obj = obj

    @property
    def user(self):
        return User.objects.get(pk=self.obj.data['user'])

    @property
    def title(self):
        return self.obj.data.get('title')
