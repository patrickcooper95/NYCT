from google.transit import gtfs_realtime_pb2
from datetime import datetime
import time
import urllib
import easygui

# f = open('MTADataStream.txt', 'w')
trains = []

feed = gtfs_realtime_pb2.FeedMessage()
header = gtfs_realtime_pb2.FeedHeader()
en = gtfs_realtime_pb2.FeedEntity()
response = urllib.urlopen('http://datamine.mta.info/mta_esi.php?key=8cce8a18e7fc76932d5f8349472d04c9&feed_id=1')
feed.ParseFromString(response.read())

ts = time.time()
print datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


class Train:

    def __init__(self, name):
        self.name = name
        self.stops_on_route = []
        self.stop_times = []
        self.stops_times = {}
        # self.stop = station
        # self.train_time = stop_time

    def assign_train(self):
            stops_on_route = self.stops_on_route
            name = self.name

            if stops_on_route:
            #if name == str(6):
                print name
                if "N" in stops_on_route[0]:
                    if name == "4":
                        train_val = "Woodlawn"
                    elif name == "5":
                        train_val = "Eastchester-Dyre Ave"
                    else:
                        train_val = "Pelham Bay Park"
                else:
                    if name == "4":
                        train_val = "New Lots Ave"
                    elif name == "5":
                        train_val = "Flatbush Ave"
                    else:
                        train_val = "Brooklyn Bridge"

                return train_val


for entity in feed.entity:
    # create object
    stops_and_times = {}
    stations = []
    arrival_times = []
    new_train = Train(entity.trip_update.trip.route_id)

    if entity.HasField('trip_update') and entity.trip_update.trip.route_id == 4 or 5 or 6:
        for i in range(len(entity.trip_update.stop_time_update)):
            stops_and_times.update({str(entity.trip_update.stop_time_update[i].stop_id):
                                   str(entity.trip_update.stop_time_update[i].arrival.time)})
            stations.append(str(entity.trip_update.stop_time_update[i].stop_id))
            arrival_times.append(str(entity.trip_update.stop_time_update[i].arrival.time))
        new_train.stops_on_route = stations
        new_train.stop_times = arrival_times
        new_train.stops_times = stops_and_times
    trains.append(new_train)
    del new_train
    del stations
    del arrival_times
    del stops_and_times

count = 0
for t in trains:
    if t.name == str(6) or t.name == str(5) or t.name == str(4):
        for key in t.stops_times.keys():
            if key == "626N" or key == "626S":
                print t.assign_train() + " " + datetime.fromtimestamp(float(t.stops_times[key])).\
                                                                      strftime('%Y-%m-%d %H:%M:%S')


easygui.msgbox(trains[0].stops_on_route[0], title="Train Update")
# f.close()
