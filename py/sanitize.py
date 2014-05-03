from __future__ import with_statement
import csv
import re
import os
from urlparse import urlparse
import socket

## Figure out how to take Command-Line Arguments

# Pipe-delimited
scriptDir = os.path.dirname(os.path.realpath(__file__))
rawFile = scriptDir + "/../data/raw.csv"
sanitizedFile = scriptDir + "/../data/sanitized.csv"
tldsFilename = scriptDir + "/../data/effective_tld_names.dat.txt"
maxPathElements = 6

def main():
    # load tlds, ignore comments and empty lines:
  with open(tldsFilename) as tldFile:
      tlds = [line.strip() for line in tldFile if line[0] not in "/\n"]

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
  writer.writerow(["tld","hostname","port","subdomain","path1","path2","path3","path4","path5","path6"])
  writer.writerow(["string","string","string","string","string","string","string","string","string","string"])
  writer.writerow(["","","","","","","","","",""])

# Takes a line of raw input and produces an array of fields
def processLine(line, tlds):
  rawFields = line.split("|")
  url = rawFields[1]
  parseResult = urlparse(url)
  domainParts = parseHostname(parseResult.netloc, tlds)

  # Take first maxPathElements path elements
  pathElements = parseUrlPath(parseResult.path)[:maxPathElements]
  # Pad the array if less than maxPathElements
  if len(pathElements) < maxPathElements: 
    while len(pathElements) < maxPathElements:
      pathElements.append("")
  subdomains = ""
  if domainParts.subdomains != None:
    subdomains = ".".join(domainParts.subdomains)
  ret = [domainParts.tld, domainParts.domain, domainParts.port, subdomains]
  ret.extend(pathElements)
  # ret.append(url)
  return ret

# Turns URL path into an array of path elements. Takes care of leading and trailing slashes.
def parseUrlPath(urlPath):
  commaSafeUrlPath = re.sub(",", "", urlPath)
  return commaSafeUrlPath.strip("/").split("/")

# Turns full network address into subdomain section plus hostname:port section.
# Returns dictionary with keys subdomain and hostname
# def parseHostname(networkAddress):
#   domainSearch = re.search('(.*)\.?([^.]+\.[^.]+)', networkAddress)
#   subdomain = ""
#   hostname = ""
#   domain = dict({
#     'subdomain': "",
#     'hostname': ""
#   })
#   if domainSearch: 
#     domain['subdomain'] = domainSearch.group(1)
#     domain['hostname'] = domainSearch.group(2)
#   return domain


# Taken from: http://stackoverflow.com/a/6926141
class DomainParts(object):
  def __init__(self, domain_parts, port, tld):
    self.domain = None
    self.subdomains = None
    self.tld = tld
    self.port = port
    if domain_parts:
      self.domain = domain_parts[-1]
      if len(domain_parts) > 1:
        self.subdomains = domain_parts[:-1]


def parseHostname(networkAddress, tlds):
  # Split out the port number
  portSplit = networkAddress.split(':')
  noPort = portSplit[0]
  port = "80" if len(portSplit) == 1 else portSplit[1]
  # Although convenient, this test for a valid IP takes waaay too long. Come up with something more efficient.
  # try:
  #   socket.inet_aton(noPort)
  #   # is a valid IP.
  #   return DomainParts([noPort], port, "")
  # except socket.error:
  #   # Not an IP, so continue.
  #   pass


  urlElements = noPort.split('.')

  # urlElements = ["abcde","co","uk"]
  for i in range(-len(urlElements),0):
    lastIElements = urlElements[i:]
    #    i=-3: ["abcde","co","uk"]
    #    i=-2: ["co","uk"]
    #    i=-1: ["uk"] etc

    candidate = ".".join(lastIElements) # abcde.co.uk, co.uk, uk
    wildcardCandidate = ".".join(["*"]+lastIElements[1:]) # *.co.uk, *.uk, *
    exceptionCandidate = "!"+candidate

    # match tlds: 
    if (exceptionCandidate in tlds):
      tld = ".".join(urlElements[i:])
      return tld 
    if (candidate in tlds or wildcardCandidate in tlds):
      tld = '.'.join(urlElements[i:])
      return DomainParts(urlElements[:i], port, tld)
      # returns ["abcde"]

  #print networkAddress
  #raise ValueError("Domain not in global list of TLDs")
  return DomainParts([noPort], port, "")
  # try:
  #   socket.inet_aton(noPort)
  #   # is a valid IP.
  #   return DomainParts([noPort], port, "")
  # except socket.error:
  #   # Not an IP, so continue.
  #   return DomainParts(urlElements, port, "")


if __name__ == "__main__":
  main()
