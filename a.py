''
# take continuous data stream
inputBufferSize = 20002  # keep betweein 2000-20000
# set read timeout, 20000 is one second
ser.timeout = inputBufferSize / 20000.0
# this is the problem line on the mac
# ser.set_buffer_size(rx_size = inputBufferSize)

%matplotlib notebook

total_time = 100.0  # time in seconds [[1 s = 20000 buffer size]]
max_time = 10.0  # time plotted in window [s]
N_loops = 20000.0 / inputBufferSize * total_time

# length of time that data is acquired for
T_acquire = inputBufferSize / 20000.0
# total number of loops to cover desire time window
N_max_loops = max_time / T_acquire

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
plt.ion()
fig.show()
fig.canvas.draw()


def Detection(seq, std_thresh, diff_thresh, prom_threshold):
    std = np.std(seq)
    diff = np.max(seq) - np.min(seq)
    peaks = len(scipy.signal.find_peaks(seq, prominence=prom_threshold)[0])
    maxval = np.argmax(seq)
    minval = np.argmin(seq)
    if peaks > 2:
        return 'fl'
    elif std > std_thresh and diff > diff_thresh:
        if maxval > minval:
            return 'L'
        else:
            return 'R'
    else:
        return 'NA'


b = 0
x = 200
calibrating = True
game_input = 'NA'
start = True
cal_count = 0
nas = 0
last_seq = np.empty(0)
max_cstd = 0
max_cdiff = 0
max_ch = 0
current_detection = 0
count = 0
best_diff = 0
cbest_diff = 0
ccount = 0
cstds = np.empty(0)
cdiffs = np.empty(0)

for k in range(0, int(N_loops)):
    data = read_arduino(ser, inputBufferSize)
    data_temp = process_data(data)
    data_temp = np.flip(data_temp)

    a1 = []
    z = 0
    while z < len(data_temp):  # Taking rolling average for x points
        a1.append(np.mean(data_temp[z:z + x]))
        z += x

    data_temp = np.array(a1)
    combined = np.concatenate((last_seq, data_temp), axis=None)

    if calibrating and b > 0:
        if start:
            arrs = np.split(data_temp, 5)
            means = np.empty(0)
            diffs = np.empty(0)
            for k in arrs:
                means = np.append(means, np.mean(k))
                diffs = np.append(diffs, (np.max(k) - np.min(k)))
            base_h = np.median(means)
            base_std = np.std(data_temp)
            if base_std > 5:
                base_std = 5
            base_diff = np.median(diffs)
            start = False
        else:
            c = 0
            movement = len(combined) - 50
            while movement - c > 0:
                interval = combined[c:(c + 50)]
                cstd = np.std(interval)
                cdiff = np.max(interval) - np.min(interval)
                ch = np.max(interval)
                cpeaks = len(scipy.signal.find_peaks(
                    interval, prominence=10)[0])
                if cpeaks >= 3:
                    calibrating = False
                    cpeaks = 0
                    cstds = np.flip(np.sort(cstds))
                    cdiffs = np.flip(np.sort(cdiffs))
                    fstd = cstd
                    fdiff = cdiff
                    fch = ch

                    max_std = cstds[0]
                    if len(cstds) > 3:
                        low_std = cstds[2]
                    elif len(cstds) == 1:
                        low_std = max_std
                    else:
                        low_std = cstds[1]
                    std_threshold = low_std / 2

                    max_diff = cdiffs[0]
                    if len(cdiffs) > 3:
                        low_diff = cdiffs[2]
                    elif len(cdiffs) == 1:
                        low_diff = max_diff
                    else:
                        low_diff = cdiffs[1]
                    diff_threshold = low_diff / 2

                    prom_threshold = 10
                    break

                elif cstd > 2 * base_std and ccount > 4:
                    if cdiff >= cbest_diff:
                        cbest_diff = cdiff
                        cbest = interval
                    elif (cbest_diff - cdiff) > 10:
                        cstds = np.append(cstds, np.std(cbest))
                        cdiffs = np.append(cdiffs, cbest_diff)
                        cbest = 0
                        cbest_diff = 0
                        ccount = 0
                else:
                    ccount += 1

                c += 5
    elif b > 0:
        d = 0
        if len(combined) > 50:
            movement = len(combined) - 50
            while movement - d > 0:
                interval = combined[d:(d + 50)]
                predicted = Detection(
                    interval, std_threshold, diff_threshold, prom_threshold)
                ran = np.max(interval) - np.min(interval)
                sdi = np.std(interval)

                if predicted == 'NA':
                    count += 1

                elif predicted == 'fl' and count > 5:
                    count = 0
                    best = 0
                    best_diff = 0
                    # print(predicted)
                    # predicted is input to game here
                    game_input = predicted

                elif (sdi > std_threshold or ran > diff_threshold) and count > 5:
                    if ran >= best_diff:
                        best_diff = ran
                        best = interval
                    elif (best_diff - ran) > 10:
                        actual = Detection(
                            best, std_threshold, diff_threshold, prom_threshold)
                        game_input = actual
                        # actual is input to game here
                        best = 0
                        best_diff = 0
                        count = 0
                if game_input != 'NA':
                    print(game_input)
                # game_input is input to game here
                game_input = 'NA'
                previous = predicted
                d += 5
    last_seq = data_temp
    b += 10000

    # if k <= N_max_loops:
    #    if k==0:
    #        data_plot = data_temp
    #    else:
    #        data_plot = np.append(data_temp,data_plot)
    #    t = (min(k+1,N_max_loops))*inputBufferSize/20000.0*np.linspace(0,1,(data_plot).size)
    # else:
    #    data_plot = np.roll(data_plot,len(data_temp))
    #    data_plot[0:len(data_temp)] = data_temp
    #t = (min(k+1,N_max_loops))*inputBufferSize/20000.0*np.linspace(0,1,(data_plot).size)

#    plt.xlim([0,max_time])
    # ax1.clear()
    #ax1.set_xlim(0, max_time)
    #plt.xlabel('time [s]')
    # ax1.plot(t,data_plot)
    # fig.canvas.draw()
    # plt.show()
