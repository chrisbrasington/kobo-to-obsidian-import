#!/usr/bin/python
import sqlite3

kobo = '/media/chris/KOBOeReader/.kobo/KoboReader.sqlite'
obsidian = '/home/chris/obsidian/highlights'

class Bookmark:
    def __init__(self, bookmark_type, text, content_id):
        self.Type = bookmark_type
        self.Text = text
        self.ContentID = content_id

class KoboBookmark:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_highlights(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT Type, Text, ContentID FROM Bookmark WHERE Type='highlight'")
        highlights = c.fetchall()
        conn.close()
        bookmarks = []
        for highlight in highlights:
            bookmark = Bookmark(highlight[0], highlight[1], highlight[2])
            bookmarks.append(bookmark)
        return bookmarks

kobo_bookmarks = KoboBookmark(kobo).get_highlights()

for bookmark in kobo_bookmarks:
    print(bookmark.ContentID)

