require 'csv'
require 'json'

def load_csv(path)
  # all first row of csv are headers
  lines = CSV.read(path)

  [lines[0], lines[1..-1]]
end

def load_events_train
  events_train_header, events_train_rows = load_csv('./data/events_train.csv')

  # there are 4347811 rows in events_train_rows.
  # the header is:
  #   ["time", "user_id", "title_id", "is_simulcast", "title_name",
  #    "watch_time"]
  # the first row is:
  #   ["2016-12-08T07:00:00Z", "00056734", "00000063", "false", "???", "2403"]

  # each row has 6 columns.
  # first_row[0]: this event was triggered at 2016-12-08T07:00:00Z.
  # first_row[1]: it was triggered by user 00056734 (must be 8 digits).
  # first_row[2]: it was triggered for title 00000063 (must be 8 digits).
  # first_row[3]: true if the show was just published at Japan or Korea.
  # first_row[4]: the title name.
  # first_row[5]: how much time the user spent on this title after last event.
  p 'events_train_rows:'
  p "length:  #{events_train_rows.length}"
  p "header:  #{events_train_header}"
  p "rows[0]: #{events_train_rows[0]}"

  [events_train_header, events_train_rows]
end

def load_events_test
  events_test_header, events_test_rows = load_csv('./data/events_test.csv')

  # there are 2940609 rows in events_test_rows.
  # format of events_train_rows and events_test_rows are the same.
  # events_train are logs of 60% selected users.
  # events_test are logs of the other 40% selected users.
  p 'events_test_rows:'
  p "length:  #{events_test_rows.length}"
  p "header:  #{events_test_header}"
  p "rows[0]: #{events_test_rows[0]}"

  [events_test_header, events_test_rows]
end

def load_labels_train
  labels_train_header, labels_train_rows = load_csv('./data/labels_train.csv')

  p 'labels_train_rows:'
  p "length:  #{labels_train_rows.length}"
  p "header:  #{labels_train_header}"
  p "rows[0]: #{labels_train_rows[0]}"

  [labels_train_header, labels_train_rows]
end

def load_labels_test
  labels_test_header, labels_test_rows = load_csv('./data/sample.csv')

  p 'labels_test_rows:'
  p "length:  #{labels_test_rows.length}"
  p "header:  #{labels_test_header}"
  p "rows[0]: #{labels_test_rows[0]}"

  [labels_test_header, labels_test_rows]
end

def load_titles
  titles = JSON.load(File.read('./data/titles.json'))

  p titles['00000000']

  titles
end

def save_result(labels_test_header, labels_test_rows, path)
  CSV.open(path, 'wb') do |csv|
    csv << labels_test_header

    labels_test_rows.each { |row| csv << row }
  end
end

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

labels_test_header, labels_test_rows = load_labels_test

titles = load_titles

# how about all users watched '00000001'?
# build and submit the results!
labels_test_rows.map! { |row| [row[0], '00000001'] }

save_result(labels_test_header, labels_test_rows, './data/results_0.csv')

# if each user watched a "random" title?
# build and submit the results!
labels_test_rows.map! do |row|
  [row[0], rand(titles.length).to_s.rjust(8, '0')]
end

save_result(labels_test_header, labels_test_rows, './data/results_1.csv')

# NOTE: more different strategies
# ? find the relationships between events_train and labels_train, use the
#   relationships to guess labels_test based on events_test
# ? find the relationships between titles by examining titles
