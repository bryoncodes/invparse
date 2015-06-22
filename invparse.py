#!/usr/bin/python
import sys
import json
import re

def get_inv():
# expects json-formatted data from stdin
# returns inventory object sorted by type

  # load json from standard in, initialize blank return object
  invtext = json.load(sys.stdin)
  inv={}
  
  # separate items by type for future data selection ease
  for item in invtext:
    itemtype= item['type'].lower()
    if itemtype in inv:
      inv[itemtype].append(item)
    else:
      inv[itemtype]=[]
      inv[itemtype].append(item)

  return inv


def print_most_expensive_items(inv):
# expects data as formatted by get_inv()
# outputs top 5 most expensive items in each category

  for itemtype in inv:
    top5 = []
    for item in inv[itemtype]:
      if len(top5) < 1:
        top5.append(item)
      else:
        # insert object in appropriate place to maintain sorted top list
        # (this does not allow for price collisions)
        for i in range(len(top5)-1, -1,-1):
          if item['price'] > top5[i]['price']:
            if i == 0:
              top5.insert(i, item)
            elif item['price'] < top5[i-1]['price']:
              top5.insert(i, item)
            elif item['price'] > top5[i-1]['price']:
              pass
    print("\n\nThe top 5 items for " + itemtype +"s are:")
    for i in range(5):
      print(top5[i])


def print_long_cds(cds):
# expects cd-specific data from results of get_inv()
# outputs object data for any cd whose total running time is > 1hr

  maxtime = 3600
  long_cds=[]
  
  for cd in cds:
    total=0
    for track in cd['tracks']:
      total += track['seconds']
    if total > maxtime:
      long_cds.append(cd)

  print("\n\nThe CDs with running times greater than 1 hour are:")
  for cd in long_cds:
    print(cd)


def print_musical_authors(books, cds):
# expects book & cd specific data asprovided by get_inv()
# prints a list of authors who have also released a cd

  # build list of authors
  authors=[]
  for book in books:
    if book['author'] not in authors:
      authors.append(book['author'])

  # find authors that have released cds
  musical_authors = []
  for author in authors:
    for cd in cds:
      if cd['author'] == author:
        musical_authors.append(author)
        break

  print("\n\nAuthors who have also released CDs are:")
  for i in musical_authors:
    print(i)


def print_items_with_years(inv):
# expects inventory object as provided by get_inv()
# outputs any object with a year in its <chapter|title|track>
# for this program, "year" is defined as any 4 digit number
  
  # regex for simple 4 digit number
  pattern = re.compile('(?<!\d)\d{4}(?!\d)')
  year_items=[]

  # for each inventory item type...
  for itemtype in inv:
    # ... check all items of that type for regex matches on chapter|title|track
    for item in inv[itemtype]:
      if "title" in item and pattern.search(item['title']) is not None:
        year_items.append(item)
      elif "chapters" in item:
        match = False
        for chapter in item['chapters']:
          if pattern.search(chapter) is not None:
            match = True
            break
        if match:
          year_items.append(item)
      elif "tracks" in item:
        match = False
        for track in item['tracks']:
          if pattern.search(track['name']) is not None:
            match = True
            break
        if match:
          year_items.append(item)
  
  print("\n\nItems with a year in their <chapter|title|track> are:")
  for item in year_items:
    print(item)


if __name__ == "__main__":
  inv = get_inv()
  print_most_expensive_items(inv)
  print_long_cds(inv['cd'])
  print_musical_authors(inv['book'], inv['cd'])
  print_items_with_years(inv)
