import pandas as pd
import logging
import os
from src.person import Person


class Textwriter:
    def __init__(self, indata, outpath, mode, config, progressbar_callback, logger_name='my_logger'):
        self.logger = logging.getLogger(logger_name)
        self.indata = indata
        self.outpath = outpath
        self.mode = mode
        self.config = config  # read-only
        self.dataframe = self.read_xlsx()

        self.progressbar_callback = progressbar_callback
        self.progress = 0
        self.task_count = self._count_tasks()

    def write_txt(self):
        if self.mode['birth']:
            self._write_txt_birth(data=self.dataframe[self.config['default']['sheet_birth']])
        if self.mode['baptize']:
            self._write_txt_baptize(data=self.dataframe[self.config['default']['sheet_baptize']])
        if self.mode['dead']:
            self._write_txt_dead(data=self.dataframe[self.config['default']['sheet_dead']])

    def read_xlsx(self):
        data = pd.read_excel(io=self.indata, sheet_name=None)
        self.logger.info("Tabellenblaetter {} gefunden".format([i for i in data.keys()]))

        return data

    def _update_progress(self, n):
        self.progress += n
        self.progressbar_callback(int(100*self.progress/self.task_count))

    def _count_tasks(self):
        task_count = 0
        if self.mode['birth']:
            task_count += len(self.dataframe[self.config['default']['sheet_birth']].index)
        if self.mode['baptize']:
            task_count = len(self.dataframe[self.config['default']['sheet_baptize']].index)
        if self.mode['dead']:
            task_count += len(self.dataframe[self.config['default']['sheet_dead']].index)
        return task_count

    def _write_txt_birth(self, data):
        personen = []
        for i in range(len(data.index)):
            personen.append(Person(data.iloc[[i]], 'geburtstag'))
            if type(personen[-1].name) == float:
                personen.pop()
            self._update_progress(0.5)

        personen.sort()

        outdata = os.path.join(self.outpath, self.config['default']['out_birth'])
        with open(file=outdata, mode="a", encoding="UTF-8") as file_out:
            age = 0
            for i in personen:
                if i.alter > age:
                    age = i.alter
                    file_out.write("zum " + str(age) + ".\n")
                file_out.write(str(i) + "\n")
                self._update_progress(0.5)

    def _write_txt_baptize(self, data):
        personen = []
        for i in range(len(data.index)):
            personen.append(Person(data.iloc[[i]], 'taufen'))
            if type(personen[-1].name) == float:
                personen.pop()
            self._update_progress(0.5)

        outdata = os.path.join(self.outpath, self.config['default']['out_baptize'])
        with open(file=outdata, mode="a", encoding="UTF-8") as file_out:
            for i in personen:
                file_out.write(str(i) + "\n")
                self._update_progress(0.5)

    def _write_txt_dead(self, data):
        personen = []
        for i in range(len(data.index)):
            personen.append(Person(data.iloc[[i]], 'verstorben'))
            if personen[-1].name == None:
                personen.pop()
            self._update_progress(0.5)

        outdata = os.path.join(self.outpath, self.config['default']['out_dead'])
        with open(file=outdata, mode="a", encoding="UTF-8") as file_out:
            for i in personen:
                file_out.write(str(i) + "\n")
                self._update_progress(0.5)
