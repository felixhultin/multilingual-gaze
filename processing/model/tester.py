import os
from abc import ABC, abstractmethod

from processing.settings import LOGGER


class Tester(ABC):
    def __init__(self, quantities, device, task):
        self.quantities = quantities  # list of metrics to be evaluated (other than the loss)
        self.device = device
        self.task = task

        self.preds = []
        self.logs = []
        self.metrics = {}  # key-value dictionary metric --> value
        self.units = {}  # key-value dictionary metric --> measurement unit

    def evaluate(self):
        LOGGER.info(f"Begin evaluation task {self.task}")
        self.predict()

        LOGGER.info("Calulating metrics")
        self.calc_metrics()

        for key in self.metrics:
            LOGGER.info(f"val_{key}: {self.metrics[key]:.4f} {self.units[key]}")

    @abstractmethod
    def predict(self):
        pass

    @abstractmethod
    def calc_metrics(self):
        pass

    @abstractmethod
    def save_preds(self, fpath):
        pass

    def save_logs(self, fpath):
        dir = os.path.dirname(fpath)
        if not os.path.exists(dir):
            os.makedirs(dir)

        for key in self.metrics:
            self.logs.append(f"{key}: {self.metrics[key]:.4f} {self.units[key]}\n")

        with open(fpath, "w") as f:
            f.writelines(self.logs)
