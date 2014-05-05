from __future__ import with_statement
import csv
import re
import os
from urlparse import urlparse
import socket
import time
from urls import loadTlds
from urls import parseUrl

# TODO: Figure out how to take Command-Line Arguments
# TODO: Read directly from Chrome SQLite DB

# Pipe-delimited
scriptDir = os.path.dirname(os.path.realpath(__file__))
rawFile = scriptDir + "/../data/raw.csv"
sanitizedFile = scriptDir + "/../data/sanitized.csv"
tldsFilename = scriptDir + "/../data/effective_tld_names.dat.txt"
maxPathElements = 6

def main():
  tlds = loadTlds()

  inFile = open(rawFile)
  outFile = open(sanitizedFile, "w")
  writer = csv.writer(outFile)
  appendHeader(writer)
  for line in inFile:
    fields = processLine(line, tlds)
    writer.writerow(fields)
  inFile.close()
  outFile.close()

def appendHeader(writer):
  writer.writerow(["timestamp","tld","hostname","port","subdomain","path1","path2","path3","path4","path5","path6"])
  writer.writerow(["datetime","string","string","string","string","string","string","string","string","string","string"])
  writer.writerow(["","","","","","","","","","",""])

# Takes a line of raw input and produces an array of fields
def processLine(line, tlds):
  rawFields = line.split("|")
  url = rawFields[0]
  urlFields = parseUrl(url, tlds)

  timestamp = rawFields[5]


  tld=urlFields[0]
  hostname=urlFields[1]
  port=urlFields[2] 
  subdomain=urlFields[3]
  path1=urlFields[4]
  path2=urlFields[5]
  path3=urlFields[6]
  path4=urlFields[7]
  path5=urlFields[8]
  path6=urlFields[9]
  ret = [timestamp, tld, hostname, port, subdomain, path1, path2, path3, path4, path5, path6]
  # ret.append(url)
  return ret

if __name__ == "__main__":
  main()
