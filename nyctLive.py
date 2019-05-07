from google.transit import gtfs_realtime_pb2
from datetime import datetime
import time
import urllib
import pandas as pd
import numpy as np


# f = open('MTADataStream.txt', 'w')
trains = []
trains_df = pd.DataFrame(columns=['Service', 'Destination', 'Stop', 'Stop_Time'])


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

            if stops_on_route:
                if "N" in stops_on_route[0]:
                    train_val = "Uptown"
                else:
                    train_val = "Downtown"

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


# lists for creating columns in DataFrame
train_service = []
train_destination = []
train_stop = []
train_stop_time = []
train_dest_now = ""


def create_train_lists(train_objects):
    for t in train_objects:
        df_count = 0
        for tr in t.stops_on_route:
            train_dest_now = t.assign_train()
            train_service.append(t.name)
            train_destination.append(train_dest_now)
            train_stop.append(tr)

            date_time = t.stop_times[df_count]
            train_stop_time.append(date_time)
            df_count += 1


# Create numpy arrays of the lists created in the function above.
create_train_lists(trains)
train_service_np = np.array(train_service)
train_destination_np = np.array(train_destination)
train_stop_np = np.array(train_stop)
train_stop_time_np = np.array(train_stop_time)


trains_df = pd.DataFrame(columns=['Service', 'Destination', 'Stop', 'Stop_Time'])
trains_df['Service'] = train_service_np
trains_df['Destination'] = train_destination_np
trains_df['Stop'] = train_stop_np
trains_df['Stop_Time'] = train_stop_time_np
trains_df['Stop_Time'] = pd.to_numeric(trains_df['Stop_Time'])
# trains_df['ETA'] = np.nan
# trains_df['ETA'] = pd.to_numeric(trains_df['ETA'])
trains_df['ETA'] = trains_df['Stop_Time'] - time.time()
trains_df['ETA'] = trains_df['ETA'] / 60


date_adjust = time.time() + 300
print datetime.fromtimestamp(date_adjust).strftime('%Y-%m-%d %H:%M:%S')
for index, row in trains_df.iterrows():
    if row['Stop'] != "626S":
        trains_df = trains_df.drop(index=index)

for index, row in trains_df.iterrows():
    if row['ETA'] < 5:
        trains_df = trains_df.drop(index=index)

trains_df = trains_df.sort_values(by=['ETA'], ascending=True)

print trains_df
