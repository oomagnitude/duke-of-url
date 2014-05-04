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
    # csvWriter = csv.writer(open(_OUTPUT_PATH,"wb"))
    # csvWriter.writerow(["timestamp", "consumption", "anomaly_score"])
    headers = reader.next()
    reader.next()
    reader.next()
    for i, record in enumerate(reader, start=1):
      modelInput = dict(zip(headers, record))
      result = model.run(modelInput)

    model.save(os.path.join(_OUTPUT_PATH, "test_checkpoint"))


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  train()
