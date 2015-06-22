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

if __name__ == "__main__":
  inv = get_inv()
  print(inv)
