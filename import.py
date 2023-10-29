#!/usr/bin/python
import sqlite3
import json
import os, sys

# region Settings
with open('settings.json') as f:
    settings = json.load(f)

kobo_path = settings['kobo_path']
obsidian_path = settings['obsidian_path']
# endregion

class Bookmark:
    def __init__(self, bookmark_type, text, volume_id, content_id, 
                 date_modified, date_created, container_start):
        self.Type = bookmark_type
        self.Text = text.strip()
        self.VolumeID = volume_id
        self.ContentID = content_id
        self.DateCreated = date_created
        self.DateModified = date_modified if date_modified is not None else date_created
        self.Location = container_start

    def __str__(self):
        return f"Type: {self.Type}\nText: {self.Text}\nVolumeID: {self.VolumeID}\nContentID: {self.ContentID}\nDateModified: {self.DateModified}Location: {self.Location}"
    
    def GetAuthor(self):
        try:
            return self.VolumeID.split('/onboard/')[1].split('/')[0].rstrip('_')
        except:
            # return None
            return 'Unknown'

    def GetBook(self):
        try:
            book = self.VolumeID.split('/')[-1].split(' - ')[0].replace('_', "'")
            return os.path.splitext(book)[0] # unlikely to still have extension
        except:
            return None
        
    def GetLocationFriendly(self):
        if '_split_' in self.Location:
            page = self.Location.split('_split_')[1].replace('_', ':')
            page = page.replace('.html#', '')
            point = page.split('point')[1]
            page = page.split('point')[0]
            return f'Page ({page}) Point {point}'
        elif 'html' in self.Location:
            page = self.Location.split('#')[0].split('/')[-1]
            point = self.Location.split('#')[-1]
            return f'Page ({page}) Point {point}'
        else:
            return self.Location


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

    def export(self, author, output):

        if not os.path.exists(output):
            os.makedirs(output)

        file = f'{output}/{author}.md'
        print(file)

        if os.path.exists(file):
            os.remove(file)

        books = self.Author[author]
        
        with open(file, "w") as f:

            for book in books:
                print(book)
                f.write(f'# {book}\n')
                
                for bookmark in books[book]:
                    f.write(f'##### {bookmark.Text}\n')
                    f.write(f'**Location**: {bookmark.GetLocationFriendly()}\n')
                    f.write(f'**Date**: {bookmark.DateModified}\n')

class KoboReader:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_highlights(self):
        try:
            conn = sqlite3.connect(self.db_path)
        except:
            print(f"Error connecting to {self.db_path}")
            sys.exit()
        c = conn.cursor()
        c.execute("SELECT Type, Text, VolumeID, ContentID, DateModified, DateCreated, StartContainerPath FROM Bookmark WHERE Type='highlight'")
        highlights = c.fetchall()
        conn.close()
        coll = Collection()
        for highlight in highlights:
            bookmark = Bookmark(highlight[0], highlight[1], highlight[2], highlight[3], highlight[4], highlight[5], highlight[6])
            author = bookmark.GetAuthor()
            if author is None:
                author = 'Unknown'
            book = bookmark.GetBook()
            
            coll.add(bookmark)

            

        return coll



collection = KoboReader(kobo_path).get_highlights()

for author in reversed(collection.Author):
    print('~'*50)
    books = collection.Author[author]
    collection.export(author, obsidian_path)
    # for book in books:
        # print(book)
        # for bookmark in books[book]:
        #     # print(bookmark.Text)
        #     # print(bookmark.DateModified)
        #     # print(bookmark.GetLocationFriendly())
        #     # print()
        #     print()

