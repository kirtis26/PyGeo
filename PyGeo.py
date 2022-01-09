# Импорт библиотек
import tkinter
import os
import random
import time, datetime
from math import *

def name_track(file_name):
    
    gpx_file = open(file_name, 'r', encoding="utf-8")
    list_lines = gpx_file.readlines()
    
    k = 0
    list_index = []
    for index_line in range(len(list_lines)):
        if list_lines[index_line].find('<trk>') != -1:
            k += 1
            if list_lines[index_line+1].find('<name>') != -1:
                list_index.append(index_line+1)
    
    print(f'Count tracks: {k}')
    
    name_tracks = []
    
    if len(list_index) != 0:
        for i in list_index:
            ind_name_begin = list_lines[i].find('<name>') + 6 # находим индекс начала названия трека
            ind_name_end = list_lines[i].rfind('</name>') # находим индекс конца названия трека
            name_tracks.append(list_lines[i][ind_name_begin:ind_name_end])
        return name_tracks
    
    else:
        print('Name tracks is not fined in trk: error structure file .gpx')
        return name_tracks

def distance(point_1, point_2):
    """
    Формула Хаверсина для расчета дистанции между двумя точками соседними
    """
    r = 6371302
    phi1 = point_1['lat'] * pi/180
    phi2 = point_2['lat'] * pi/180
    lam1 = point_1['lon'] * pi/180
    lam2 = point_2['lon'] * pi/180
    return 2 * r * asin(sqrt(sin((phi2 - phi1)/2)**2 + cos(phi1)*cos(phi2)*sin((lam2-lam1)/2)**2))

# ----------------------------------------------------------------------------------------------

file_name = 'ATB-Heerenveen.gpx'
gpx_file = open(file_name, 'r', encoding="utf-8") # открываем файл по определенному имени file_name

# file_name = random.choice(os.listdir('gpx')) # название случайного файла из папки gpx
# gpx_file = open(file_name, 'r', encoding="utf-8") # открываем случайных файл

# gpx_file = tkinter.filedialog() # открытие с помощью файлового диалога

list_lines = gpx_file.readlines() # построчно файл gpx_file записуем в список

print(name_track(file_name)) # Выводим названия треков из открытого файла

tracks = []

for index_line in range(len(list_lines)):
    
    if list_lines[index_line].find('<trk>') != -1:
        
        track = []
        flag_trk = True
        i = index_line
        while flag_trk == True:
            
            flag_seg = False
            while flag_seg == False:
                if list_lines[i].find('<trkseg>') != -1:
                    flag_seg = True
                else:
                    i += 1
        
            segment = []
            while flag_seg == True:
                if list_lines[i].find('<trkpt') != -1:
                    lat_begin = list_lines[i].find('lat="') + 5
                    lat_end = list_lines[i].find('"', lat_begin)
                    lat = float(list_lines[i][lat_begin:lat_end])
                    lon_begin = list_lines[i].find('lon="') + 5
                    lon_end = list_lines[i].find('"', lon_begin)
                    lon = float(list_lines[i][lon_begin:lon_end])
                    point = {'lat': lat,
                             'lon': lon,
                             'time': 0}
                    segment.append(point)
                    i += 1
                elif list_lines[i].find('<time>') != -1:
                    ind_time_begin = list_lines[i].find('<time>') + 6 
                    ind_time_end = list_lines[i].rfind('</time>')
                    str_date = list_lines[i][ind_time_begin:ind_time_end]
                    str_date = str_date.replace('T', ' ')
                    str_date = str_date.replace('Z', '')
                    segment[-1]['time'] = str_date
                    i += 1
                elif list_lines[i].find('</trkseg>') != -1:
                    flag_seg = False
                else:
                    i += 1
        
            track.append(segment)
            
            i += 1
            if list_lines[i].find('</trk>') != -1:
                flag_trk = False

        tracks.append(track)

# ----------------------------------------------------------------------------------------------#
# Вывод расстояний (длин) треков
# ----------------------------------------------------------------------------------------------#

for i in range(len(tracks)):
    dist_track = 0
    for j in range(len(tracks[i])):
        for k in range(len(tracks[i][j])-1):
            dist_track += distance(tracks[i][j][k], tracks[i][j][k+1])
    print(f'Distance track №{i+1}: {dist_track} м')   

# ----------------------------------------------------------------------------------------------#
# Вывод путевых отметок (если они есть)
# ----------------------------------------------------------------------------------------------#

wpts = []

for index_line in range(len(list_lines)):
    
    if list_lines[index_line].find('<wpt') != -1:
        
        ind_str_name = index_line
        flag_wpt = True
        
        while flag_wpt == True: 
            
            if list_lines[ind_str_name].find('<name>') != -1:
                ind_name_begin = list_lines[ind_str_name].find('<name>') + 6
                ind_name_end = list_lines[ind_str_name].find('</name>')
                name = list_lines[ind_str_name][ind_name_begin:ind_name_end]
                wpts.append(name)
            if list_lines[ind_str_name].find('</wpt>') != -1:
                flag_wpt = False
            ind_str_name += 1
if len(wpts) == 0:
    print('Wpt is not definded')
else:
    print(f'{len(wpts)} Путевые отметки:')
    print(wpts)

# ----------------------------------------------------------------------------------------------#
# Вывод затраченного времени трэков
# ----------------------------------------------------------------------------------------------#

times = []

for i in range(len(tracks)):
    
    flag_time = True
    for j in range(len(tracks[i])):
        for k in range(len(tracks[i][j])):
            if tracks[i][j][k]['time'] == 0:
                flag_time = False
    if flag_time == True:
        init_point_track = tracks[i][0][0]
        end_point_track = tracks[i][-1][-1]
        struct1 = time.strptime(init_point_track['time'], '%Y-%m-%d %H:%M:%S')
        struct2 = time.strptime(end_point_track['time'], '%Y-%m-%d %H:%M:%S')
        dt1 = datetime.datetime(struct1.tm_year, struct1.tm_mon, struct1.tm_mday, struct1.tm_hour, struct1.tm_min, struct1.tm_sec)
        dt2 = datetime.datetime(struct2.tm_year, struct2.tm_mon, struct2.tm_mday, struct2.tm_hour, struct2.tm_min, struct2.tm_sec)
        dif_dt = dt2 - dt1
        dif_sec = dif_dt.seconds
        dif_min = dif_sec / 60
        dif_hour = dif_min / 60
        dif_day = dif_hour / 24
        print(f'Track №{i+1}')
        print(f'Затрачено: секунд {dif_sec};\n минут {dif_min};\n часов {dif_hour};\n дней {dif_day}')
    else:
        print(f'Track №{i+1} имеет точки без времени')
