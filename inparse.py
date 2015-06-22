#!/usr/bin/python
import sys
import json

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


if __name__ == "__main__":
  inv = get_inv()
  print_most_expensive_items(inv)
  print_long_cds(inv['cd'])
