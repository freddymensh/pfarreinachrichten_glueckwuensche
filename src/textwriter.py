import pandas as pd
import logging
import os
from src.person import Person

class Textwriter:
    def __init__(self, indata, outpath, mode, logger_name='my_logger'):
        self.indata = indata
        self.outpath = outpath
        self.mode = mode
        self.dataframe = self.read_xlsx()

        self.logger = logging.getLogger(logger_name)

    def write_txt(self):
        if self.mode['birth']:
            self._write_txt_birth(data=self.dataframe['Geburtstage']) #TODO: Blattname in config
        if self.mode['baptize']:
            self._write_txt_baptize()
        if self.mode['dead']:
            self._write_txt_dead()

    def read_xlsx(self):
        data = pd.read_excel(io=self.indata, sheet_name=None)
        #self.logger.info("Tabellenblaetter {} gefunden".format(data)) #TODO: logger fixen
        return data

    def _write_txt_birth(self, data):
        personen = []
        for i in range(len(data.index)):
            personen.append(Person(data.iloc[[i]], 'geburtstag'))
            if personen[-1].name == None:
                personen.pop()

        import random
        random.shuffle(personen)
        personen.sort()

        outdata = os.path.join(self.outpath, "geb.txt")
        with open(file=outdata, mode="a", encoding="UTF-8") as file_out:
            age = 0
            for i in personen:
                if i.alter > age:
                    age = i.alter
                    file_out.write("zum " + str(age) + ".\n")
                file_out.write(str(i) + "\n")


    def _write_txt_baptize(self):
        pass

    def _write_txt_dead(self):
        pass