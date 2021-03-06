#! python3
# shingeki.py - Download every single shingeki no kyojin comic.
#
# Personal notes/references. ---------------------------------------------------
# Dissecting HTML pages with BeautifulSoup:
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# Getting all images on a page:
# https://stackoverflow.com/questions/18408307/how-to-extract-and-download-all-images-from-a-website-using-beautifulsoup
# Saving image data to a file:
# https://stackoverflow.com/questions/54338681/how-to-download-images-from-websites-using-beautiful-soup

# Imports/using. ---------------------------------------------------------------
import os
import requests
from bs4 import BeautifulSoup
from requests.exceptions import MissingSchema

# Variables. -------------------------------------------------------------------
ch_num = 0
ch_count = 0
confirmation = False
root = os.path.abspath(os.curdir)


# Functions. -------------------------------------------------------------------
def format_check(chapter_or_page):
    """Formats number to three digits."""

    # https://ww7.readsnk.com/chapter/shingeki-no-kyojin-chapter-0/
    # compared to...
    # https://ww7.readsnk.com/chapter/shingeki-no-kyojin-chapter-001/
    # So if it's chapter zero, don't format.
    if chapter_or_page == 0:
        return chapter_or_page

    # Format all the others.
    if len(str(chapter_or_page)) == 1:
        chapter_or_page = f"00{chapter_or_page}"

    elif len(str(chapter_or_page)) == 2:
        chapter_or_page = f"0{chapter_or_page}"

    return chapter_or_page


# Chapter loop. ----------------------------------------------------------------
while True:
    # Reset page number and count for each chapter.
    page_number = 1
    count = 0

    # Get chapter URL.
    ch_format = format_check(ch_num)
    ch_url = f'https://ww7.readsnk.com/chapter/shingeki-no-kyojin-chapter-{ch_format}/'
    req = requests.get(ch_url)

    # "OK" status confirm to start. --------------------------------------------
    if req.status_code == 200:

        soup = BeautifulSoup(req.content, 'html.parser')
        # Each chapter will be separated with their own folders.
        ch_path = f"{root}/shingeki/chapter{ch_format}"
        try:
            os.makedirs(ch_path)
        except FileExistsError:
            pass

        # Total chapter count confirmation. ------------------------------------
        # Getting a rough chapter count from the dropdown menu on the first page.
        list_of_chapters = []
        for o in soup.find_all('option'):
            if "chapter" in o['value']:
                list_of_chapters.append(o)

        # Remove duplicates (multiple identical dropdown menus on the website).
        list_of_chapters = (list(dict.fromkeys(list_of_chapters)))

        # Check to see if we've already asked this or not.
        if not confirmation:
            length = len(list_of_chapters)
            # During tests, most chapters average ~25-30mb in folder size.
            input(f"There are ~{length} chapters available. \n"
                  f"Total download size may be around {(30 * length) / 1000}GB"
                  f" or larger."
                  f"\nHit enter to proceed.")
            confirmation = True

        # Manga page loop. -----------------------------------------------------
        # All manga pages are images.
        img_tags = soup.find_all('img')
        for img in img_tags:
            page_number += 1
            try:
                # The img class for the manga pages seems to always be this type.
                if img['class'] == ['my-3', 'mx-auto', 'js-page']:
                    # Grab the image url from "src" tag.
                    url = img['src'].rstrip('\r')

                    # Save manga page. -----------------------------------------
                    pg_format = format_check(page_number)

                    with open(f"{ch_path}/Shingeki_{ch_format}_{pg_format}.png", 'wb') as file:
                        print(f"Downloading {url}...")
                        try:
                            image_response = requests.get(url)
                            file.write(image_response.content)
                            count += 1
                        except MissingSchema:
                            print(f"(404) Unable to find that image.\nSkipping!\n")
                            pass

            # Very rarely, a chapter may contain an image that has no key 'class'.
            # These are manually placed ads what from I can tell.
            # I didn't think returning a default value with .get() would help
            # in this case, so we'll just catch this error.
            except KeyError:
                # Log to console so we know it happened, just in case.
                print(f"Skipping: {img['src']}")
                pass

        print(f"Finished chapter {ch_num}. Saved {count} pages!")
        ch_num += 1
        ch_count += 1

    # Else "Not found" (404) status. -------------------------------------------
    elif req.status_code == 404:
        print(f"Results! ------------------------------------------------------\n"
              f"We have downloaded a total of {ch_count} chapters!\n\n")
        print(f"Unable to locate chapter {ch_num} of Shingeki at:")
        print(ch_url)
        print(f"Does that chapter exist yet?\n"
              f"If it does exist, check for differences in the URLs for this chapter.")
        print(f"Shutting down program. さようなら \n(*￣▽￣)b  *:･ﾟ✧")

        # Open folder in explorer to see results (only works in Windows)
        os.startfile(root)
        break