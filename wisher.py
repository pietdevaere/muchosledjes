import csv

message_file = open('messages.csv', 'r')
message_csv = csv.reader(message_file)
for line in message_csv:
    print("{} from {}".format(line[1], line[0]))
