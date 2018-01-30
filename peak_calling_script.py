
from __future__ import print_function
import sys
import numpy
import math
import random
import csv
import matplotlib.pyplot as plt
import pystache
import json
from sklearn import mixture

x = []
y = []

toolInput = sys.argv[1]
toolOutput = sys.argv[2]
toolWebsite = sys.argv[3]

with open(sys.argv[1], 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t')
    for i, row in enumerate(spamreader):
        if i != 0:
            x.append(int(row[0]))
            y.append(int(row[1]))

# you have to set this manually to weed out all the noise. Every bit of noise should be below it.
threshold = 20
rightLimit = 200

# unravelling histogram into samples.
samples = []
for no, value in enumerate([int(round(i)) for i in y]):
    if value > threshold and no < rightLimit:
        for _ in range(value):
            samples.append(no)

# total number of reads
totalAmp = len(samples)

# reshaping numpy arrays to indicate that we pass a lot of samples, not a lot of features.
xArray = numpy.array(x).reshape(1, -1)
samplesArray = numpy.array(samples).reshape(-1, 1)

# learning a gaussian mixture model.
gmm2 = mixture.BayesianGaussianMixture(n_components=2).fit(samplesArray)

# getting the mean of each gaussian
means = [x[int(round(i[0]))] for i in gmm2.means_]

# rounding errors
roundErr = [i[0] - int(round(i[0])) for i in gmm2.means_]

# getting the coverage of each gaussian
weights = gmm2.weights_

sampleID = toolOutput + ".html"

with open(toolOutput, "w") as f:
    print("sampleID", file=f, end="\t")
    print("Al1", file=f, end="\t")
    print("Al2", file=f, end="\t")
    print("frac1", file=f, end="\t")
    print("frac2", file=f, end="\t")
    print(file=f)
    print(sampleID, file=f, end="\t")
    print(means[0], file=f, end="\t")
    print(means[1], file=f, end="\t")
    print(weights[0], file=f, end="\t")
    print(weights[1], file=f, end="\t")

template_dir = {
    "sampleID": sampleID,
    "al1": means[0],
    "al2": means[1],
    "freq1": weights[0],
    "freq2": weights[1],
    "x": json.dumps(x),
    "y": json.dumps(y)
    }
with open(toolWebsite) as wt:
    with open(sampleID, "w") as wr:
        wr.write(pystache.render(wt.read(), template_dir))
