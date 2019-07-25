from google.transit import gtfs_realtime_pb2
from datetime import datetime
import time
import urllib
import pandas as pd
import numpy as np


trains = list()
data_source = 'http://datamine.mta.info/mta_esi.php?key=8cce8a18e7fc76932d5f8349472d04c9&feed_id=1'

feed = gtfs_realtime_pb2.FeedMessage()
header = gtfs_realtime_pb2.FeedHeader()
en = gtfs_realtime_pb2.FeedEntity()
response = urllib.urlopen(data_source)
feed.ParseFromString(response.read())

# lists for creating columns in DataFrame
train_service = list()
train_destination = list()
train_stop = list()
train_stop_time = list()


ts = time.time()
print datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


class Train:
    """
        This class provides the framework for a train object, created through the live transit data.
        For each unique train in the live transit feed, an object will be created detailing its service,
        stops, and stop times.

        While a class object does assign directions to trains (Uptown/Downtown) using the "assign_train" function,
        it mainly acts as a container for the train stops and times.
    """

    def __init__(self, name):
        self.name = name
        self.stops_on_route = list()
        self.stop_times = list()
        self.stops_times = list()

    def assign_train(self):
        stops_on_route = self.stops_on_route

        if stops_on_route:
            if "N" in stops_on_route[0]:
                train_val = "Uptown"
            else:
                train_val = "Downtown"

            return train_val


def _create_trains():
    """
        The crucial function for the NYCT Project - this function parses the data from the transit feed,
        calls "create_train_lists" to create lists of this data; calls "create_dataframe" to align this data
        in a Pandas dataframe; and finally calls sort_dataframe to sort and add calculated fields to the DF.
    :return: a Pandas dataframe containing the trip_updates for the 4, 5, and 6 trains
    """
    for entity in feed.entity:
        # create dict and two lists for each train
        stops_and_times = dict()
        stations = list()
        arrival_times = list()
        # create object
        new_train = Train(entity.trip_update.trip.route_id)

        # filter entities for only trip_updates and only 4, 5, and 6 trains
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


def _create_train_lists(train_objects):

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


def _create_dataframe(np1, np2, np3, np4):

    new_df = pd.DataFrame(columns=['Service', 'Destination', 'Stop', 'Stop_Time'])
    service_np = np1
    destination_np = np2
    stop_np = np3
    stop_time_np = np4

    new_df['Service'] = service_np
    new_df['Destination'] = destination_np
    new_df['Stop'] = stop_np
    new_df['Stop_Time'] = stop_time_np
    new_df['Stop_Time'] = pd.to_numeric(new_df['Stop_Time'])
    new_df['ETA'] = new_df['Stop_Time'] - time.time()
    new_df['ETA'] = new_df['ETA'] / 60
    new_df['Train_ID'] = new_df['Service'].astype(str) + new_df['Stop'].astype(str) + new_df['ETA'].astype(str)
    new_df = new_df.drop_duplicates(subset='Train_ID')

    # With DF created, now filter for the desired trains to display in the GUI.
    date_adjust = time.time() + 300
    print "Filtering...\n"
    print datetime.fromtimestamp(date_adjust).strftime('%Y-%m-%d %H:%M:%S')

    downtown_stops = new_df['Stop'] == '626S'
    uptown_stops = new_df['Stop'] == '626N'
    train_is_gone = new_df['ETA'] > 4
    filtered_stops_df = new_df.loc[downtown_stops | uptown_stops, :]
    filtered_df = filtered_stops_df.loc[train_is_gone, :]
    filtered_df = filtered_df.sort_values(by='ETA', ascending=True)
    return filtered_df


def train_main():

    _create_trains()
    _create_train_lists(trains)

    # Create numpy arrays of the lists created in the _create_train_lists function.
    train_service_np = np.array(train_service)
    train_destination_np = np.array(train_destination)
    train_stop_np = np.array(train_stop)
    train_stop_time_np = np.array(train_stop_time)
    created_df = _create_dataframe(train_service_np, train_destination_np, train_stop_np, train_stop_time_np)
    del train_service_np
    del train_destination_np
    del train_stop_np
    del train_stop_time_np
    return created_df


if __name__ == "__main__":
    train_main()
