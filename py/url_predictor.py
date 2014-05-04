import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'model_0'))
import model_params
import csv
import cmd
import logging
from nupic.data.datasethelpers import findDataset
from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic.frameworks.opf.predictionmetricsmanager import MetricsManager
from urls import loadTlds
from urls import parseUrl
import datetime



scriptDir = os.path.dirname(os.path.realpath(__file__))
_LOGGER = logging.getLogger(__name__)
_DATA_PATH = os.path.join(scriptDir, "..", "data", "sanitized.csv")
_MODEL_PATH = os.path.join(scriptDir, "..", "savedModel", "checkpoint")
model = ModelFactory.loadFromCheckpoint(_MODEL_PATH)

tlds = loadTlds()


class UrlShell(cmd.Cmd):
    intro = 'Enter URL to predict next hostname.\n'
    prompt = 'url> '
    file = None

    def default(self, line):
      processOneUrl(line)

def processOneUrl(url): 
      timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%s")
      urlFields = parseUrl(url, tlds)

      # Create dict: timestamp,tld,hostname,port,subdomain,path1,path2,path3,path4,path5,path6
      modelInput = dict(timestamp=timestamp, url=url, 
        tld=urlFields[0], 
        hostname=urlFields[1], 
        port=urlFields[2], 
        subdomain=urlFields[3], 
        path1=urlFields[4], 
        path2=urlFields[5], 
        path3=urlFields[6], 
        path4=urlFields[7],
        path5=urlFields[8],
        path6=urlFields[9])
      result = model.run(modelInput)
      nextUrl = result.inferences['multiStepBestPredictions'][1]
      thirdUrl = result.inferences['multiStepBestPredictions'][3]
      print("next: " + nextUrl)
      print("third: " + thirdUrl)

def runUrlPrediction():
  model.enableInference({'predictedField': 'hostname'})
  cmdPrompt = UrlShell()
  cmdPrompt.cmdloop()

if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  runUrlPrediction()
