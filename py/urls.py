from urlparse import urlparse
import os
import re


maxPathElements = 6
scriptDir = os.path.dirname(os.path.realpath(__file__))

tldsFilename = scriptDir + "/../data/effective_tld_names.dat.txt"

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


def loadTlds():
      # load tlds, ignore comments and empty lines:
  with open(tldsFilename) as tldFile:
      tlds = [line.strip() for line in tldFile if line[0] not in "/\n"]
  return tlds

def parseUrl(url, tlds):
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
  return ret



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

# Turns URL path into an array of path elements. Takes care of leading and trailing slashes.
def parseUrlPath(urlPath):
  commaSafeUrlPath = re.sub(",", "", urlPath)
  return commaSafeUrlPath.strip("/").split("/")
