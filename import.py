#!/usr/bin/python
import sqlite3
import json
import os

# region Settings
with open('settings.json') as f:
    settings = json.load(f)

kobo_path = settings['kobo_path']
obsidian_path = settings['obsidian_path']
# endregion

class Bookmark:
    def __init__(self, bookmark_type, text, volume_id, content_id, date_modified, date_created):
        self.Type = bookmark_type
        self.Text = text
        self.VolumeID = volume_id
        self.ContentID = content_id
        self.DateCreated = date_created
        self.DateModified = date_modified if date_modified is not None else date_created

    def __str__(self):
        return f"Type: {self.Type}\nText: {self.Text}\nVolumeID: {self.VolumeID}\nContentID: {self.ContentID}\nDateModified: {self.DateModified}"
    
    def GetAuthor(self):
        try:
            return self.VolumeID.split('/onboard/')[1].split('/')[0].rstrip('_')
        except:
            return None

    def GetBook(self):
        try:
            book = self.VolumeID.split('/')[-1].split(' - ')[0].replace('_', ':')
            return os.path.splitext(book)[0] # unlikely to still have extension
        except:
            return None

class Collection:
    def __init__(self):
        self.Author = {}
    
    def add(self, bookmark):
        book = bookmark.GetBook()
        author = bookmark.GetAuthor()
        if author not in self.Author.keys():
            self.Author[author] = {}
        if book not in self.Author[author].keys():
            self.Author[author][book] = []
        # append highlight
        self.Author[author][book].append(bookmark)

class KoboReader:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_highlights(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT Type, Text, VolumeID, ContentID, DateModified, DateCreated FROM Bookmark WHERE Type='highlight'")
        highlights = c.fetchall()
        conn.close()
        coll = Collection()
        for highlight in highlights:
            bookmark = Bookmark(highlight[0], highlight[1], highlight[2], highlight[3], highlight[4], highlight[5])
            author = bookmark.GetAuthor()
            if author is None:
                continue # fix?
            book = bookmark.GetBook()
            
            coll.add(bookmark)

            

        return coll



collection = KoboReader(kobo_path).get_highlights()

for author in collection.Author:
    print('~'*50)
    print(author)
    books = collection.Author[author]
    for book in books:
        print('BOOK!!!!!!!!!!!!!!')
        print(book)
        for bookmark in books[book]:
            print(bookmark.Text)
            print(bookmark.DateModified)
            print(bookmark.DateCreated)
            print()

# for author in kobo_bookmarks.keys():
#     print('~'*50)
#     print(author)
#     books = kobo_bookmarks[author]
#     for book in books:
#         print(book.GetBook())
#         for bookmark in books:
#             print(bookmark.Text)



# for bookmark in (kobo_bookmarks):
#     # print(bookmark)
#     print(bookmark.GetAuthor())
#     # print(os.path.splitext(bookmark.GetBook())[0])
#     print(bookmark.GetBook())
#     print('~'*50)

# sample = kobo_bookmarks[-1]

# print(str(sample))
# print()
# print(sample.GetAuthor())