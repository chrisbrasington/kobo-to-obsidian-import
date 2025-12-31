#!/usr/bin/env python

import sqlite3
import json
import os
import sys

# region Settings
settings_file = 'settings.json'

# Check if an argument is provided from the command line
if len(sys.argv) > 1:
    # If an argument is provided, use it as the settings file path
    settings_file = sys.argv[1]

with open(settings_file) as f:
    settings = json.load(f)

kobo_path = settings['kobo_path']
obsidian_path = settings['obsidian_path']
# endregion

class Highlight:
    """
    A class representing a highlight in a Kobo e-reader.

    Attributes:
    - Type (str): The type of bookmark (e.g. "Bookmark", "Highlight", "Note").
    - Text (str): The text of the highlight.
    - VolumeID (str): The ID of the book that the highlight belongs to.
    - ContentID (str): The ID of the content that the highlight belongs to.
    - DateCreated (str): The date when the highlight was created.
    - DateModified (str): The date when the highlight was last modified.
    - Location (str): The location of the highlight in the book.
    - Annotation (str): The user annotation of the highlight.
    - Color (int): The color of the highlight.
    """

    def __init__(self, bookmark_type, text, volume_id, content_id,
                 date_modified, date_created, container_start, annotation, color):
        """
        Initializes a new instance of the Highlight class.

        Args:
        - bookmark_type (str): The type of bookmark (e.g. "Bookmark", "Highlight", "Note").
        - text (str): The text of the highlight.
        - volume_id (str): The ID of the book that the highlight belongs to.
        - content_id (str): The ID of the content that the highlight belongs to.
        - date_modified (str): The date when the highlight was last modified.
        - date_created (str): The date when the highlight was created.
        - container_start (str): The location of the highlight in the book.
        """
        self.Type = bookmark_type
        self.Text = text.strip() if text is not None else text
        self.VolumeID = volume_id
        self.ContentID = content_id
        self.DateCreated = date_created
        self.DateModified = date_modified if date_modified is not None else date_created
        self.Location = container_start
        self.Annotation = annotation
        self.Color = color

    def __str__(self):
        """
        Returns a string representation of the Highlight object.
        """
        return f"Type: {self.Type}\nText: {self.Text}\nVolumeID: {self.VolumeID}\nContentID: {self.ContentID}\nDateModified: {self.DateModified}Location: {self.Location}\nAnnotation: {self.Annotation}\nColor: {self.Color}"

    def GetAuthor(self):
        """
        Returns the author of the book that the highlight belongs to.

        Returns:
        - str: The author of the book.
        """
        try:
            return self.VolumeID.split('/onboard/')[1].split('/')[0].rstrip('_')
        except:
            # return None
            return 'Unknown'

    def GetBook(self):
        """
        Returns the title of the book that the highlight belongs to.

        Returns:
        - str: The title of the book.
        """
        try:
            book = self.VolumeID.split('/')[-1].split(' - ')[0].replace('_', "'")
            return os.path.splitext(book)[0] # unlikely to still have extension
        except:
            return None

    def GetLocationFriendly(self):
        """
        Returns a human-readable version of the location of the highlight.

        Returns:
        - str: A human-readable version of the location of the highlight.
        """
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
    """
    A class representing a collection of highlights.

    Attributes:
    - Author (dict): A dictionary of authors and their books and highlights.
    """

    def __init__(self):
        """
        Initializes an empty dictionary of authors and their books and highlights.
        """
        self.Author = {}

    def add(self, bookmark):
        """
        Adds a highlight to the collection.

        Args:
        - bookmark (Highlight): The highlight to add to the collection.
        """
        book = bookmark.GetBook()
        author = bookmark.GetAuthor()
        if author not in self.Author.keys():
            self.Author[author] = {}
        if book not in self.Author[author].keys():
            self.Author[author][book] = []
        self.Author[author][book].append(bookmark)

    def export(self, author, output):
        """
        Exports the highlights of a given author to a Markdown file.

        Args:
        - author (str): The name of the author whose highlights to export.
        - output (str): The path to the directory where the Markdown file should be saved.
        """
        if not os.path.exists(output):
            os.makedirs(output)

        file = f'{output}/{author}.md'
        print(file)

        if os.path.exists(file):
            os.remove(file)

        books = self.Author[author]

        with open(file, "w") as f:

            for book in books:
                print(f'{book} - {len(books[book])} highlights')
                f.write(f'# {book}\n')
                f.write('\n---\n\n')
                for bookmark in books[book]:
                    if bookmark.Color == 0:
                        quote = settings['callout_yellow']
                    elif bookmark.Color == 1:
                        quote = settings['callout_red']
                    elif bookmark.Color == 2:
                        quote = settings['callout_blue']
                    elif bookmark.Color == 3:
                        quote = settings['callout_green']
                    else:
                        quote = settings['callout_yellow']
                    f.write(f'{quote}\n{bookmark.Text}\n\n')

                    if bookmark.Type == 'note' and bookmark.Annotation is not None:
                        f.write(f'\n{settings["annotation"]}\n{bookmark.Annotation}\n\n')

                    f.write(f'**Location**: {bookmark.GetLocationFriendly()}\n')
                    f.write(f'**Date**: {bookmark.DateModified}\n')
                    f.write('\n---\n')



# Define a class called KoboReader
class KoboReader:
    # Constructor method that initializes the class with a path to the Kobo database
    def __init__(self, db_path):
        self.db_path = db_path

    # Method that retrieves all highlights from the Kobo database
    def get_highlights(self):
        # Try to connect to the Kobo database
        try:
            conn = sqlite3.connect(self.db_path)
        except:
            print(f"Error connecting to {self.db_path}")
            sys.exit()
        # Create a cursor object to execute SQL commands
        c = conn.cursor()
        # Execute a SQL command to select all highlights from the Bookmark table
        c.execute("SELECT Type, Text, VolumeID, ContentID, DateModified, DateCreated, StartContainerPath, Annotation, Color  FROM Bookmark WHERE Type in ('highlight','note')")
        # Fetch all the highlights from the cursor object
        highlights = c.fetchall()
        # Close the connection to the database
        conn.close()
        # Create a Collection object to store the highlights
        coll = Collection()
        # Loop through all the highlights and add them to the Collection object
        for highlight in highlights:
            bookmark = Highlight(highlight[0], highlight[1], highlight[2], highlight[3], highlight[4], highlight[5], highlight[6], highlight[7], highlight[8])
            author = bookmark.GetAuthor()
            if author is None:
                author = 'Unknown'
            book = bookmark.GetBook()
            coll.add(bookmark)
        # Return the Collection object with all the highlights
        return coll


# Create a Collection object called "collection" by calling the get_highlights method of a KoboReader object with the path to the Kobo database as an argument
collection = KoboReader(kobo_path).get_highlights()

# Loop through all the authors in the Collection object in reverse order
for author in reversed(collection.Author):
    print('~'*50)
    # Get the books for the current author from the Collection object
    books = collection.Author[author]
    # Export the highlights for the current author to the Obsidian vault using the export method of the Collection object
    collection.export(author, obsidian_path)
