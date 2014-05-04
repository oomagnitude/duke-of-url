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
import texttable


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
      table = texttable.Texttable()
      oneStepPredictions = result.inferences['multiStepPredictions'][1]
      threeStepPredictions = result.inferences['multiStepPredictions'][3]
      printTopNPredictions(oneStepPredictions, "next", table, 3)
      printTopNPredictions(threeStepPredictions, "third", table, 3)
      print table.draw()

def runUrlPrediction():
  model.enableInference({'predictedField': 'hostname'})
  cmdPrompt = UrlShell()
  cmdPrompt.cmdloop()

def printTopNPredictions(predictions, step, table, n):
  row = [step]
  invPredictions = {v:k for k, v in predictions.items()}
  i = 1
  for key in sorted(invPredictions, reverse=True):
    if(i > n):
      break
    i += 1
    pct = "%.2f" % (key * 100)
    row.append(invPredictions[key] + " (" + pct + "%)")
  table.add_row(row)

if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  runUrlPrediction()
