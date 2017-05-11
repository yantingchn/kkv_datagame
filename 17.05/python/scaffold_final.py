
import csv
import json
import sys
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier

# Additional modules

# Local modules
def load_csv(filename):
    """CSV loader with escape of header line.
    
    :rtype: [header, lines] where lines is an interator
    """
    # with codecs.open(filename, 'r', encoding='utf-8') as fin:
    #     csvreader = csv.reader(fin)
    #     header = next(csvreader)
    # return header, csvreader
    content = np.genfromtxt(filename, dtype=None, delimiter=',', names=True)
    header = content.dtype.names
    print("loading... "+filename+" finshed")
    return header ,content

def load_pickle(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)

    header = data['header']
    rows = data['rows']

    return header, rows

def load_events_train():
    """Load events_train.csv.
    
    there are 4347811 rows in events_train_rows.
    the header is:
    ["time", "user_id", "title_id", "is_simulcast", "title_name", "watch_time"]
    the first row is:
     ["2016-12-08T07:00:00Z", "00056734", "00000063", "false", "???", "2403"]

    each row has 6 columns.
    first_row[0]: this event was triggered at 2016-12-08T07:00:00Z.
    first_row[1]: it was triggered by user 00056734 (must be 8 digits).
    first_row[2]: it was triggered for title 00000063 (must be 8 digits).
    first_row[3]: true if the show was just published at Japan or Korea.
    first_row[4]: the title name.
    first_row[5]: how much time the user spent on this title after last event.
  
    :rtype: [header, lines] where lines is an interator
    """
    if load_from_pickle:
        return load_pickle('./data/events_train')
    else:
        return load_csv('./assets/events_train.csv')


def load_events_test():
    """Load events_test.csv.
  
    There are 2940609 rows in events_test_rows.
    The format of events_train_rows and events_test_rows are the same.
    events_train contains logs of 60% selected users.
    events_test contains logs of the other 40% selected users.

    :rtype: [header, lines] where lines is an interator
    """
    if load_from_pickle:
        return load_pickle('./data/events_test')
    else:
        return load_csv('./assets/events_test.csv')

def load_labels_train():
    """Load labels_train.csv.

    :rtype: [header, lines] where lines is an interator
    """
    if load_from_pickle:
        return load_pickle('./data/labels_train')
    else:
        return load_csv('./assets/labels_train.csv')


def load_labels_test():
    """Load labels_train.csv.

    :rtype: [header, lines] where lines is an interator
    """
    if load_from_pickle:
        return load_pickle('./data/labels_test')
    else:
        return load_csv('./assets/sample.csv')


def load_titles():
    """Load titles.json, title's metadata.
    
    :rtype: a dictionary of titles with title_id as keys
    """
    # with codecs.open('./assets/titles.json', 'r', encoding='utf-8') as fin:
    #     titles = json.loads(fin.read())

    with open('./assets/titles/titles_all.json') as json_data:
        video_info = json.load(json_data)

    return video_info


def save_result(filename, rows):
    """Save the testing's result, labels, into a file.
    
    :param: as iterator with each item as (user_id, title_id)

    NOTE: both user_id and title_id in rows should be a string 
    with necessary padding zeros.
    """
    # with codecs.open(filename, 'w', encoding='utf-8') as fout:
    #     fout.write(','.join(headers)+'\n')
    #     fout.writelines(','.join(r)+'n' for r in rows)
    with open(filename, 'w') as csvfile:
        field = ['user_id', 'title_id']
        writer = csv.DictWriter(csvfile, fieldnames = field)

        writer.writeheader()
        for i in xrange(len(rows)):
            writer.writerow({
                    "user_id":str(i).zfill(8), 
                    "title_id":str(int(rows[i])).zfill(8)
                    })


load_from_pickle = True
video_num = 730
train_num = 62307
test_num = 41539
alpha = 1
beta = 1

def main():

    events_train_header, events_train_rows = load_events_train()

    events_test_header, events_test_rows = load_events_test()

    labels_train_header, labels_train_rows = load_labels_train()

    labels_test_header, labels_test_rows = load_labels_test()

    video_info = load_titles()

    if not load_from_pickle:
        events_train = {
            "header":events_train_header,
            "rows":events_train_rows
        }
        with open('./data/events_train', 'wb') as f:
            pickle.dump(events_train, f, pickle.HIGHEST_PROTOCOL)

        events_test = {
            "header":events_test_header,
            "rows":events_test_rows
        }
        with open('./data/events_test', 'wb') as f:
            pickle.dump(events_test, f, pickle.HIGHEST_PROTOCOL)
        
        labels_train = {
            "header":labels_train_header,
            "rows":labels_train_rows
        }
        with open('./data/labels_train', 'wb') as f:
            pickle.dump(labels_train, f, pickle.HIGHEST_PROTOCOL)

        labels_test = {
            "header":labels_test_header,
            "rows":labels_test_rows
        }
        with open('./data/labels_test', 'wb') as f:
            pickle.dump(labels_test, f, pickle.HIGHEST_PROTOCOL)

    print "loading train file"


    X_train = np.zeros(shape=(train_num,video_num))
    prev_id = -1


    time = 0
    max_time = 0
    last = -1
    el_list = [110, 391, 669]
    interest = [669, 664, 391, 110, 482, 389, 251, 87, 628, 587, 483, 372, 265]
    no_his = []
    less_epi = []
    users = {}
    watch_time_less = []

    episode_count = 0
    episode_num = {}

    for v in video_info:
        for n in video_info[v]["total_episode_counts"]:
            episode_count += int(video_info[v]["total_episode_counts"][n])
        if int(v) in interest:
            print v, episode_count
        episode_num[int(v)] = episode_count
        episode_count = 0

    print len(episode_num)


    temp_list = {}
    for i in xrange(events_train_rows.shape[0]):
        if events_train_rows[i][1] != prev_id:
            users[prev_id] = last
            if max_time < 121500 and last not in el_list:
                no_his.append(prev_id-41539)
            elif episode_num[int(last)] < 11:
                less_epi.append(prev_id-41539)
            # elif temp_list[last] < 500:
            #     watch_time_less.append(prev_id-41539)
            prev_id = events_train_rows[i][1]
            max_time = 0
            temp_list = {}
        time = int(events_train_rows[i][0][5:7] + events_train_rows[i][0][8:10]+ events_train_rows[i][0][11:13])
        if time > max_time:
            max_time = time
            last = events_train_rows[i][2]
        elif time == max_time:
            if temp_list[last] < events_train_rows[i][5]:
                last = events_train_rows[i][2]
        if events_train_rows[i][3]:
            X_train[events_train_rows[i][1]-41539, events_train_rows[i][2] - 1] += 1*alpha
        else:
            X_train[events_train_rows[i][1]-41539, events_train_rows[i][2] - 1] += 1
        if (events_train_rows[i][2]) not in temp_list:
            temp_list[events_train_rows[i][2]] = events_train_rows[i][5]
        else:
            temp_list[events_train_rows[i][2]] = events_train_rows[i][5]

    users[prev_id] = last
    no_his = np.sort(no_his)
    less_epi = np.sort(less_epi)
    # watch_time_less = np.sort(watch_time_less)

    correct = np.zeros(730)
    total_count = np.zeros(730)
    count = 0

    Y_train = np.zeros(train_num)

    for i in xrange(labels_train_rows.shape[0]):
        total_count[labels_train_rows[i][1]] += 1

        # if labels_train_rows[i][0] in watch_time_less:
        #     if users[labels_train_rows[i][0]] == labels_train_rows[i][1]:
        #         count += 1
        #         correct[labels_train_rows[i][1]] += 1
        Y_train[i] = labels_train_rows[i][1]



    print "no_his_len", len(no_his)
    print "less_len", len(less_epi)
    # print "watch_time_less", len(watch_time_less)
    print "count:", count
    # for i in xrange(730):
    #     if correct[i] > 10:
    #         print i, correct[i]
    # print "total count", train_num - len(less_epi)

    # print '####################'
    # print '360', total_count[360]
    # print '409', total_count[409]
    # print '670', total_count[670]
        
    # print '####################'
    # print '265', correct[265]
    # print '372', correct[372]
    # print '483', correct[483]
    # print '587', correct[587]
    # print '628', correct[628]
    X = X_train[no_his]
    Y = Y_train[no_his]

    X_e = X_train[less_epi]
    Y_e = Y_train[less_epi]

    # X_w = X_train[watch_time_less]
    # Y_w = Y_train[watch_time_less]

    print X.shape, Y.shape
    print X_e.shape, Y_e.shape
    # print X_w.shape, Y_w.shape
    print "start training"
    X = np.asarray(X)
    Y = np.asarray(Y)

    X_e = np.asarray(X_e)
    Y_e = np.asarray(Y_e)

    # X_w = np.asarray(X_w)
    # Y_w = np.asarray(Y_w)

    clf = RandomForestClassifier(
                            n_estimators=200
                            ,max_depth=40
                            ,min_samples_split=2
                            ,random_state=None
                            )
    clf_e = RandomForestClassifier(
                            n_estimators=200
                            ,max_depth=25
                            ,min_samples_split=2
                            ,random_state=None
                            )

    # clf_w = RandomForestClassifier(
    #                         n_estimators=100
    #                         ,max_depth=30
    #                         ,min_samples_split=2
    #                         ,random_state=None
    #                         )

    clf = clf.fit(X.astype('float32'), Y.astype('float32').ravel())
    clf_e = clf_e.fit(X_e.astype('float32'), Y_e.astype('float32').ravel())
    # clf_w = clf_w.fit(X_w.astype('float32'), Y_w.astype('float32').ravel())

    print 'EVA'
    print "clf_accuracy:", clf.score(X, Y.ravel())
    print "clf_e_acc:", clf_e.score(X_e, Y_e.ravel())
    # print "clf_w_acc", clf_w.score(X_w, Y_w.ravel())

    print "loading test csv"

    test = np.zeros(shape=(test_num,video_num))
    prev_id = -1

    time = 0
    max_time = 0
    last = -1
    users = {}
    no_his_test = []
    less_epi_test = []
    watch_time_less = []

    temp_list = {}
    for i in xrange(events_test_rows.shape[0]):
        if events_test_rows[i][1] != prev_id:
            users[prev_id] = last
            if max_time < 120000 and last not in el_list:
                no_his_test.append(prev_id)
            elif episode_num[int(last)] < 11:
                less_epi_test.append(prev_id)
            # elif temp_list[last] < 500 and max_time > 121500:
            #     watch_time_less.append(prev_id)
            prev_id = events_test_rows[i][1]
            max_time = 0
            temp_list = {}
        time = int(events_test_rows[i][0][5:7] + events_test_rows[i][0][8:10] + events_test_rows[i][0][11:13])
        if time > max_time:
            last = events_test_rows[i][2]
            max_time = time
        elif time == max_time:
            if temp_list[last] < events_test_rows[i][5]:
                last = events_test_rows[i][2]
        if events_test_rows[i][3]:
            test[events_test_rows[i][1], events_test_rows[i][2] - 1] += 1*alpha
        else:
            test[events_test_rows[i][1], events_test_rows[i][2] - 1] += 1
        if (events_test_rows[i][2]) not in temp_list:
            temp_list[events_test_rows[i][2]] = events_test_rows[i][5]
        else:
            temp_list[events_test_rows[i][2]] = events_test_rows[i][5]

    users[prev_id] = last
    no_his_test = np.sort(no_his_test)
    less_epi_test = np.sort(less_epi_test)
    # watch_time_less = np.sort(watch_time_less)

    print "no_his_len", len(no_his_test)
    print "less_epi_test", len(less_epi_test)
    # print "watch_time", len(watch_time_less)
    
    results = clf.predict(test)
    results_e = clf_e.predict(test[less_epi_test])
    # results_w = clf_w.predict(test[watch_time_less])

    test_dis = np.zeros(video_num)
    print test.shape
    print len(results)

    counter = 0 
    ppp = 0
    for j in xrange(len(results)):
        if j not in no_his_test:
            results[j] = users[j]
        if j in less_epi_test:
            results[j] = results_e[counter]
            counter += 1
        # if j in watch_time_less:
        #     results[j] = results_w[ppp]
        #     ppp += 1
        test_dis[int(results[j])] += 1

    
    for i in xrange(len(test_dis)):
        if test_dis[i] > 800:
            print i, test_dis[i]

    save_result('./results/results_test_with_no_his_less_time_hope_1215_time.csv', results)


    # save_result(labels_test_header, labels_test_rows, './data/results_1.csv')

    # NOTE: more different strategies
    # ? find the relationships between events_train and labels_train, use the
    #   relationships to guess labels_test based on events_test
    # ? find the relationships between titles by examining titles

    return


if __name__ == "__main__":
    main()
