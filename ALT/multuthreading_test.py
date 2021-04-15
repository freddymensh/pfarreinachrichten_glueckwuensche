import json
import os
import numpy as np
import pandas as pd


def main():
    path = "C:\\Users\\Freddy\\tubCloud\\Shared\\AutProjekt3_DL_Verfahren_Gruppe2\\Modelle\\SOLOv2\\augmentiert"
    files = [os.path.join(path, i) for i in [j for j in os.listdir(path) if ".json" in j]]
    json_list = []
    for i in files:
        with open(files[i]) as json_file:
            for j in json.load(json_file)
                if not '' in j.keys:
                    json_list.append[j]

    df = pd.read_json(json.dumps(json_list))


if __name__ == "__main__":
    main