# twin-peaks
Sample workflow + naive algorithm for Neurofinder

## usage
To generate a `JSON` file with the estimated ROIs, simply download the testing data from the [Neurofinder website]
(http://neurofinder.codeneuro.org/), and place the `segment.py` script in a folder containing all of the testing
datasets. Then simply run `python segment.py` from the command line in this directory. The resulting file is in
the correct form for uploading to the Neurofinder leaderboard for scoring.

## algorithm
The algorithm uses 2D peak finding and assumes a fixed circulur region arround each peak

