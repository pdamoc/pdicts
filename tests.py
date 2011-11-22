from pdicts import PersistentDict
import os
import os.path
dbfile = "test.sqlite"
if os.path.exists(dbfile):
    os.remove(dbfile)
d = PersistentDict(dbfile)

#testing some adds
d['mission'] = "Let the beauty of what you love be what you do"
d['years_active'] = [2010, 2011, 2012]

print d.keys() #testing the saved keys
print d['mission'] #testing a simple get
print d['hate'] #testing a missing key
