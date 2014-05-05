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

scriptDir = os.path.dirname(os.path.realpath(__file__))
_LOGGER = logging.getLogger(__name__)
_DATA_PATH = scriptDir + "/../data/sanitized.csv"
_OUTPUT_PATH = scriptDir + "/../savedModel"
model = ModelFactory.create(model_params.MODEL_PARAMS)

def train():
  model.enableInference({'predictedField': 'hostname'})

  with open (findDataset(_DATA_PATH)) as fin:
    reader = csv.reader(fin)
    headers = reader.next()
    # Skip header lines
    reader.next()
    reader.next()

    i = 0
    for i, record in enumerate(reader, start=1):
      modelInput = dict(zip(headers, record))
      model.run(modelInput)
      i += 1
      if (i%500 == 0):
        print("ran "+ str(i) + " steps")

    model.save(os.path.join(_OUTPUT_PATH, "checkpoint"))


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  train()
