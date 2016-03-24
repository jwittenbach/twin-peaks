import json
from numpy import array, zeros, where
from scipy.misc import imread
from glob import glob

from scipy.ndimage.filters import gaussian_filter, maximum_filter
from itertools import product

results = []

# loop over all datasets
datasets = glob('./neurofinder*')
for folder in datasets:

    # load the images
    files = sorted(glob(folder + '/images/*.tiff'))
    imgs = array([imread(f) for f in files])

    # compute the average image
    avg = imgs.mean(axis=0)

    # blur to smooth in space
    blurred = gaussian_filter(avg, 3)

    # replace each pixel by the maximum value in a neighborhood
    # of size roughly equal to a single neuron
    maxed = maximum_filter(blurred, size=10)

    # locate peaks by looking at where the max filter has no effect
    peaks = zip(*where(maxed == blurred))

    # for each peak, include all pixes within a fixed radius in the source
    regions = []
    xmax, ymax = avg.shape[0], avg.shape[1]

    def get_circle_points(x, y, r):
        points = []
        rangeX, rangeY = range(x-r, x+r+1), range(y-r, y+r+1)
        for (px, py) in product(rangeX, rangeY):
            if px < 0 or py < 0 or px > xmax or py > ymax:
                continue
            if (px-x)**2 + (py-y)**2 <= r**2:
                points.append((px, py))
        return points

    for (x, y) in peaks:
        regions.append({"coordinates": get_circle_points(x, y, 5)})

    # get dataset id
    idx = folder.find('.', 2)
    name = folder[idx+1:]

    # append results for this dataset
    results.append({"dataset": name, "regions": regions})

# write results
with open("estimates.json", "w") as f:
    json.dump(results, f) 
