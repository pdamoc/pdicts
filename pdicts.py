#!/usr/bin/env python

license = """
Copyright (C) 2011 by Peter Damoc

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
import json
import sqlite3
import os.path
from UserDict import DictMixin

class PersistentDict(DictMixin):
    def __init__(self, dbfile):
        self.__dbfile = dbfile
        if not os.path.exists(dbfile):
            con = sqlite3.connect(dbfile)
            cur = con.cursor()
            cur.execute("CREATE TABLE store (key text, value text)")
            con.commit()
        else:
            con = sqlite3.connect(dbfile)
            cur = con.cursor()
            
        self.con_mem = sqlite3.connect(':memory:')
        self.cur_mem = self.con_mem.cursor()        
        self.con_mem.executescript("".join(line for line in con.iterdump()))
        self.con_mem.commit()
        
    def keys(self): 
        self.cur_mem.execute("SELECT key FROM store")
        return [key[0] for key in self.cur_mem.fetchall()]
        
    def __getitem__(self, key): 
        self.cur_mem.execute("SELECT value FROM store WHERE key=?", (key,))
        value = self.cur_mem.fetchone()
        
        if value is None:
            raise KeyError(key)
        return json.loads(value[0])
        
    def __setitem__(self, key, value): 
        con = sqlite3.connect(self.__dbfile)
        cur = con.cursor()
        self.cur_mem.execute("SELECT value FROM store WHERE key=?", (key,))
        
        if self.cur_mem.fetchone() is None:
            self.cur_mem.execute("INSERT INTO store (key, value) VALUES (?, ?)", (key, json.dumps(value)))
            cur.execute("INSERT INTO store (key, value) VALUES (?, ?)", (key, json.dumps(value)))
        else:
            cur.execute('UPDATE store SET value=? where key=?', (json.dumps(value), key))
            self.cur_mem.execute('UPDATE store SET value=? where key=?', (json.dumps(value), key))        
            
        con.commit()
        self.con_mem.commit()            
            
    def __delitem__(self, key):
        self.cur_mem.execute("SELECT value FROM store WHERE key=?", (key,))
        value = self.cur_mem.fetchone()
        if value is None:
            raise KeyError(key)
        else:
            con = sqlite3.connect(self.__dbfile)
            cur = con.cursor()
            self.cur_mem.execute("DELETE FROM store WHERE key=?", (key, ))
            cur.execute("DELETE FROM store WHERE key=?", (key, ))
            con.commit()
            self.con_mem.commit()            
            
        return json.loads(value[0])
        