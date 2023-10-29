#!/usr/bin/python

import sqlite3

class KoboBookmark:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_highlights(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT Type, Text, ContentID FROM Bookmark WHERE Type='highlight'")
        highlights = c.fetchall()
        conn.close()
        return highlights
    
kobo = '/media/chris/KOBOeReader/.kobo/KoboReader.sqlite'

kobo_bookmarks = KoboBookmark(kobo).get_highlights()

for bookmark in kobo_bookmarks:
    print(bookmark)

