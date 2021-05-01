import pandas as pd
import numpy as np
import scipy.signal
import matplotlib.pyplot as plt

f = pd.read_csv('Week_8/LRflutterx4_h2.txt', sep = ' ', header=None)

data = f.iloc[:,1] - 509.9
data = data.to_numpy()
data = np.flip(data)

#plt.plot(data)
#plt.show()

def Detection(seq):
    std = np.std(seq)
    peaks = len(scipy.signal.find_peaks(seq, height=30, prominence=20)[0])
    maxval = np.argmax(seq)
    minval = np.argmin(seq)
    if std > 19:
        if peaks > 4:
            return 'fl'
        else:
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

ls = []
ls2 = []

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

            ls.append(len(scipy.signal.find_peaks(interval, height=30, prominence=20)[0]))
            ls2.append(np.std(interval))

            predicted = Detection(interval)
            if predicted == 'NA':
                count += 1
                count2 = 0
            if predicted in ('L', 'R', 'fl') and count > 10:
                count2 += 1
                if count2 > 2 and count > 10:
                    print(predicted)
                    # predicted is input to the game here
                    count = 0
            previous = predicted
            j += 1000
    last_seq = data_temp
    i += 10000

#plt.plot(ls)
#plt.plot(ls2)
#plt.show()
