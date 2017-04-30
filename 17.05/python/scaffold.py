#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set hls is ai et sw=4 sts=4 ts=8 nu ft=python:
#


# Built-in modules
import codecs
import csv
import json
import sys

# Additional modules

# Local modules



def load_csv(filename):
    """CSV loader with escape of header line.
    
    :rtype: [header, lines] where lines is an interator
    """
    with codecs.open(filename, 'r', encoding='utf-8') as fin:
        csvreader = csv.reader(fin)
        header = next(csvreader)
    return header, csvreader


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
    return load_csv('./data/events_train.csv')


def load_events_test():
    """Load events_test.csv.
  
    There are 2940609 rows in events_test_rows.
    The format of events_train_rows and events_test_rows are the same.
    events_train contains logs of 60% selected users.
    events_test contains logs of the other 40% selected users.

    :rtype: [header, lines] where lines is an interator
    """
    return load_csv('./data/events_test.csv')


def load_labels_train():
    """Load labels_train.csv.

    :rtype: [header, lines] where lines is an interator
    """
    return load_csv('./data/labels_train.csv')


def load_labels_test():
    """Load labels_train.csv.

    :rtype: [header, lines] where lines is an interator
    """
    return load_csv('./data/sample.csv')


def load_titles():
    """Load titles.json, title's metadata.
    
    :rtype: a dictionary of titles with title_id as keys
    """
    with codecs.open('/data/titles.json', 'r', encoding='utf-8') as fin:
        titles = json.loads(fin.read())
    return titles


def save_result(filename, rows, headers=('user_id', 'title_id')):
    """Save the testing's result, labels, into a file.
    
    :param: as iterator with each item as (user_id, title_id)

    NOTE: both user_id and title_id in rows should be a string 
    with necessary padding zeros.
    """
    with codecs.open(filename, 'w', encoding='utf-8') as fout:
        fout.write(','.join(headers)+'\n')
        fout.writelines(','.join(r)+'n' for r in rows)


def main(sys=sys.argv[:]):
    # NOTE: happy data game!

    # TODO(instructions):
    # download data from kaggle, unzip the archive into kkv_datagame/17.05/data
    # there should be 5 files: events_test.csv, events_train.csv, titles.csv,
    # labels_train.csv, sample.csv.

    # NOTE:
    # DO NOT PUBLISH THE DATA.

    # TODO(instructions):
    # submit sample.csv to kaggle competition to get your first score on public
    # leader board.
    # sample.csv is the format of your result.

    # NOTE: load all data. some csv are large files, skip them if you don't need
    # them.

    # events_train_header, events_train_rows = load_events_train

    # events_test_header, events_test_rows = load_events_test

    # labels_train_header, labels_train_rows = load_labels_train

    # labels_test_header, labels_test_rows = load_labels_test

    # titles = load_titles

    # how about all users watched '00000001'?
    # build and submit the results!
    # labels_test_rows.map! { |row| [row[0], '00000001'] }

    # save_result(labels_test_header, labels_test_rows, './data/results_0.csv')

    # if each user watched a "random" title?
    # build and submit the results!
    #labels_test_rows.map! do |row|
    #  [row[0], rand(titles.length).to_s.rjust(8, '0')]
    #end

    # save_result(labels_test_header, labels_test_rows, './data/results_1.csv')

    # NOTE: more different strategies
    # ? find the relationships between events_train and labels_train, use the
    #   relationships to guess labels_test based on events_test
    # ? find the relationships between titles by examining titles

    return


if __name__ == "__main__":
    main()
