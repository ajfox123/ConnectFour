import pandas as pd
import numpy as np
import scipy.signal
import matplotlib.pyplot as plt

f = pd.read_csv('Week_8/LRflutterx4_h2.txt', sep = ' ', header=None)

data = f.iloc[:,1] - 509.9
data = data.to_numpy()
data = np.flip(data)

def Detection(seq):
    std = np.std(seq)
    diff = np.max(seq) - np.min(seq)
    peaks = len(scipy.signal.find_peaks(seq, height=30, prominence=20)[0])
    maxval = np.argmax(seq)
    minval = np.argmin(seq)
    if peaks > 9:
        return 'fl'
    elif std > 14 and diff > 70:
        if maxval > minval:
            return 'L'
        else:
            return 'R'
    else:
        return 'NA'

l = len(data)
last_seq = np.empty(0)

i = 0
count = 0
count2 = 0
previous = 'NA'

best_diff = 0
best = 0

#simulating live streaming conditions
while i < l:
    if l-i < 10000:
        data_temp = data[i:(l-1)]
    else:
        data_temp = data[i:(i+10000)]

    combined = np.concatenate((last_seq, data_temp), axis = None)

    j = 0
    if len(combined) > 0:
        movement = len(combined) - 10000
        while movement - j > 0:
            interval = combined[j:(j+10000)]
            predicted = Detection(interval)
            range = np.max(interval) - np.min(interval)

            if predicted == 'NA':
                count += 1

            elif predicted == 'fl' and count > 7:
                count = 0
                best = 0
                best_diff = 0
                print(predicted)
                # predicted is input to game here

            if range > 50 and count > 7:
                if range >= best_diff:
                    best_diff = range
                    best = interval
                elif (best_diff - range) > 20:
                    actual = Detection(best)
                    print(actual)
                    # actual is input to game here
                    best = 0
                    best_diff = 0
                    count = 0
            previous = predicted
            j += 1000
    last_seq = data_temp
    i += 10000
