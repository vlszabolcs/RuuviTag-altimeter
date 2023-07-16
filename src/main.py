import csv_header
import csv
import datetime
import gpxpy
import nrf_parser

h=csv_header

station_csv="data/StationTag_20230529-1955.csv"
altimet_csv="data/AltimeterTag_20230529-1954.csv"
gpx_file = "nrf_logging/2023-07-06_19_40_26.794_2023-07-06T19_40+02.gpx"
file_path="nrf_logging/Log 2023-07-06 19_40_38.txt"

start_altitude=322 

def find_trackpoint_time(gpx_file):
    timestamp=[]
    gpx = gpxpy.parse(open(gpx_file, 'r'))
    first_time = gpx.tracks[0].segments[0].points[0].time
    timestamp.append(round(datetime.datetime.timestamp(first_time),0))
    
    last_time = gpx.tracks[-1].segments[-1].points[-1].time
    timestamp.append(round(datetime.datetime.timestamp(last_time),0))
    
    return timestamp


def convert_file(file_in):
    with open(file_in, 'r') as csvfile:
        data = list(csv.reader(csvfile, delimiter=","))
    return data


def convert_datetime(data_in, gpx_time):
    out=[]

    for a in data_in:
        timestamp=datetime.datetime.strptime(str(a[h.date]), '%Y-%m-%d %H:%M:%S').timestamp()
        
        if (timestamp-gpx_time[0])>0 and timestamp-gpx_time[1]<0:
            a[h.date]=timestamp
            out.append(a)

    return out

def convert_datetime_dic(data_in,gpx_time):
    out=[]
    for data in data_in:
        timestamp=round(datetime.datetime.strptime(str(data["date"]), '%Y-%m-%d %H:%M:%S').timestamp(),0)
        
        if (timestamp-gpx_time[0])>0 and timestamp-gpx_time[1]<0:
            data["date"]=timestamp
           
            out.append(data)

    return out


def altitude(slvp,altip,temp):

    cor_alti=((pow(float(slvp)/float(altip),1/5.257)-1)*(temp+273.15))/0.0065
    
    return cor_alti


def calc_slp(station_pressure, station_altitude):
    
    slp=float(station_pressure)*pow((1-((0.0065*station_altitude)/(15+0.0065*station_altitude+273.15))),-5.257)
    
    return slp

#eddig jó
def comparison(data_station,data_altimet):
    
    station_first_time=data_station[0][h.date]
    slp=calc_slp(data_station[0][h.pressure],start_altitude)
    alt=altitude(slp,data_altimet[0][h.pressure],15)
    print(alt)
    altimet_first_time=data_altimet[0][h.date]    
    dif_first_time = station_first_time-altimet_first_time

    if dif_first_time > 0 :
        print("altimet előbb")
    else:
        print("station előbb")
    
    #print(datetime.datetime.fromtimestamp(station_time))
    #print(datetime.datetime.fromtimestamp(altimet_time))
   

def minute_accuracy(data_in):
    dt = datetime.datetime.fromtimestamp(data_in)
    rounded_timestamp = data_in - (dt.second + dt.microsecond / 1e6)
    return rounded_timestamp

def station_avg(data_in):
    timestamp_1= minute_accuracy(data_in[0][h.date])
    i = 0
    avg = 0.0
    list = []
    
    for a in data_in:
        
        timestamp_2 = minute_accuracy(a[h.date])
        
        if timestamp_1 == timestamp_2:
            i += 1
            avg += float(a[h.pressure])   
     
        elif timestamp_1 != timestamp_2 and i == 0:
              
            a[h.date]=timestamp_1
            a[h.pressure]= a[h.pressure]
            list.append(a)
            i=0
            avg=0.0
            timestamp_1 = timestamp_2 
        else:
            a[h.date]=timestamp_1
            a[h.pressure]=(round(avg/(i),2))
            list.append(a)
            i=0
            avg=0.0
            timestamp_1=timestamp_2

    return list

gpx_times=find_trackpoint_time(gpx_file)
"""
station_section = convert_datetime(convert_file(station_csv),gpx_times)
altimet_section = convert_datetime(convert_file(altimet_csv),gpx_times)
print(len(altimet_section))
comparison(station_section,altimet_section)
"""

x=convert_datetime_dic(nrf_parser.parse_data(file_path), gpx_times)
print(len(x))



 