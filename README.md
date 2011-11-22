# Introduction 

**pdict** is an implementation of a persistent dictionary using sqlite3 and json libraries.
The library is silly and it sucks and as such it shouldn't be used by anyone. :)

## Install

Just download [pdicts.py](https://raw.github.com/pdamoc/pdicts/master/pdicts.py) and put it somewhere where you software can find it (e.g. same directory)

## Usage Example
```python
from pdicts import PersistentDict
d = PersistentDict("storage.sqlite")

#testing some adds
d['mission'] = "Let the beauty of what you love be what you do"
d['years_active'] = [2010, 2011, 2012]

print d.keys() #testing the saved keys
print d['mission'] #testing a simple get
print d['hate'] #testing a missing key
```

## Sucking Less

If you see simple ways this library could suck less, please feel free to contribute your ideas. 
