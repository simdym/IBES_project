import pandas as pd
import numpy as np

def record(filename, length, bitalino, channels, nSamples = 1000):
    data = bitalino.read(0)

    for i in range(length // nSamples):
        print(i * nSamples)
        data = np.append(data, bitalino.read(nSamples), axis=0)

    toCSV(data, filename)

def toCSV(data, filename):
    pd.DataFrame(data).to_csv(filename, index=False)
