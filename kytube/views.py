from .analysis import daytimeplot, getDateFilter, getDatof, getTimeDat, getTimeFilter, mostWatchedDays, plot_kw_freq, plotkwfreqMultiple, topNentries, indices_from_date,ampm_to_24hr, ampm_to_24hr, ampm_to_24hr_pre
from django.http import request
from .forms import UploadFileForm
from django.shortcuts import render
from .models import MainRow
import numpy as np
from django.http import HttpResponse, HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
import json
total_data = {}
done = 0
from django.shortcuts import render, get_object_or_404
def extractRows(table):
    retTable = np.empty(len(table), dtype='<U300')
    def listready(row):
        if(row=='None'):
            return 'None'
        try:
            row = json.loads(row)
            row:list
            datetime = row[-1]
            # print(datetime)
            date = ','.join(datetime.split(',')[:2])
            # print(date)
            mi, di = indices_from_date(date)
            row.insert(0, di)
            row.insert(0, mi)
        except:
            # print(row)
            row = 'None'
            return row
    # except:
            # print(row)
        # print(json.dumps(row))
        return json.dumps(row)
    # listready(table)
    retTable = []
    global done
    done = 0
    len_table = len(table)
    for row in table:
        done += 1/len_table
        a = listready(row)

        if(a!='None'):
            retTable.append(json.loads(a))
        else:
            continue
    # print(retTable)
    return np.array(retTable, dtype='<U400')
class dataHandler(APIView):
    def get(self, request):
        global global_data
        print("ASked status", global_data.keys())
        return Response((round(done,2)))
    def post(self, request:HttpRequest):
        # print(request.headers)
        purpose=""
        userid=""
        rows=""
        cleanedData=""
        datamain = json.loads((request.body).decode())        
        if(len(datamain)==4):
            purpose = datamain[0]['value']
            userid = datamain[1]['value']     
            rows = datamain[2]['value']
            cleanedData = datamain[3]['value']
        else:
            try:
                datamain = json.loads((request.body).decode())['params']['updates']
                purpose = datamain[0]['value']
                userid = datamain[1]['value']     
                rows = datamain[2]['value']
                cleanedData = datamain[3]['value']
            except:
                print(len(datamain))
                print(datamain)
        if(purpose=='Senduserdata'):
            table = json.loads(rows)
            table = extractRows(table)
            # processData()
            cleanedData = getCSVfmt(table, userid)
            return Response(json.dumps(cleanedData.tolist()))
        elif(purpose=='Userdata'):
            data = np.array(json.loads(cleanedData))
            ans = analyse_data(data, userid)
            # print(ans.keys())
            return Response(json.dumps(ans))
        if(purpose=='Groupwise'):
            kwlist = json.loads(rows)
            for kw in kwlist:
                if(kw.__contains__([])):
                    kw:list
                    kw.remove([])
                    kw.append([''])
            # print(datamain[2])
            # resp = {}
            print(kwlist, type(kwlist))
            totdat = np.array(json.loads(cleanedData))
            resp = analyse_data(totdat, userid, kwlist)
            return Response(json.dumps(resp))
        elif(purpose=='Filteruserdata'):
            data = np.array(json.loads(cleanedData))
            rows = json.loads(rows)
            mi, di = indices_from_date(rows[0])
            mi1, di1 = indices_from_date(rows[1])
            timelims = ampm_to_24hr(np.array(rows[2:]))
            print(timelims)
            # print(data, di, di1)
            data = np.array(getDateFilter(data, di, di1))
            data = np.array(getTimeFilter(data, data,timelims[0],timelims[1]))
            # print(data)
            # ans = analyse_data(data, userid)
            # print(rows)
            print(rows[0],rows[1])#format to date-indice
            print(rows[2],rows[3])#format to time-indice
            return Response(json.dumps(data.tolist()))
            #  data = getTimeFilter(data, data, )
        return Response(json.dumps([1, 2, 3]))

import codecs
import threading
class myThread(threading.Thread):
    def __init__(self, threadID, name, mainf, data):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.mainf = mainf
      self.data = data
    #   self.request = request
    def run(self):
      self.mainf(*self.data)
global_data = {}

i = 0
delimit =  ' ,,, '
mtoi = {
        'Jan':0,
        'Feb':1,
        'Mar':2,
        'Apr':3,
        'May':4,
        'Jun':5,
        'Jul':6,
        'Aug':7,
        'Sep':8,
        'Oct':9,
        'Nov':10,
        'Dec':11,
    }
daysinmonths = {
    'Jan':31,
    'Feb':28,
    'Mar':31,
    'Apr':30,
    'May':31,
    'Jun':30,
    'Jul':31,
    'Aug':31,
    'Sep':30,
    'Oct':31,
    'Nov':30,
    'Dec':31,
}

g_processor:myThread
def analyse_data(data, userid, kwlist = [['Youtube', '']]):
    global global_data, total_data
    total_data[userid] = data
    table, vals = topNentries(data)
    global_data[userid] = {'TopNVideos': table}
    viewfreq, extdates = plotkwfreqMultiple(data, kwlist)
    global_data[userid]['viewFreq'] = viewfreq
    global_data[userid]['extDates'] = extdates
    # kwtable = getDatof(data, [2, 3], ['Jiya', ''])
    # global_data['kwtable'] = json.dumps(kwtable)
    daytime = daytimeplot(data, kwlist)
    global_data[userid]['daytimeFreq'] = daytime
    # kw_freq = plot_kw_freq(data, ['Glendale'])
    # global_data['kwFreq'] = json.dumps(kw_freq)
    # mulkwfreq=plotkwfreqMultiple(data, [['Glendale'], ['Crash Course']])
    # global_data['mult'] = json.dumps(mulkwfreq)
    # datbound = getDateFilter(data, 17.57, 18.18)
    # global_data['datbound'] = json.dumps(datbound)
    # timefilt = getTimeFilter(data, data, 1 ,23)
    # global_data['timefilt'] = json.dumps(timefilt)
    # times, days = mostWatchedDays(data, 5)
    # global_data['topNdays'] = json.dumps(days)
    return global_data[userid]
def updateUser(done,request):
    # print(done, "as received")
    return render(request, "kytube_land.html", {'done':done})
def getCSVfmt(data, userid,request=None,get_proc=False):
    return data
    # print(userid)
def land(request):
    form = UploadFileForm()
    return render(request, "kytube_land.html", {'form':form.as_p()})
def results(request):
    return render(request, "road_to_ang.html")
def check_status(request):
    print(done)
    return render(request, "processing.html", {'progress':str(round(done, 2)), 'test':'blah'})
    # else:
    #     return render(request, "processing.html")
    
def processData(data, userid):
    print('HI')
    processor = myThread(1, 'pre', getCSVfmt, [data, userid])
    processor.start()
    g_processor = processor
    print("work started")
    return
    #process collected data
def submit(request):
    # print(request.POST)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        # print(request.POST)
        if (form.is_valid()):
            data = request.FILES['data']
            processData(data)
        else:
            print("not valid")
    return render(request, "processing.html")