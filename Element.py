from functools import total_ordering

@total_ordering
class Element:

    def __init__(self,key,data):
        self.key = key
        self.data = data

    def __eq__(self,other):
        return self.key == other.key

    def __lt__(self,other):
        return self.key < other.key

    def __str__(self):
        return 'a'

    def __unicode__(self):
        return u'a'

    def __repr__(self):
        return str(self.key) + "  " + str(self.data)

    def __hash__(self):
        return hash(self.key) ^ hash(self.data)