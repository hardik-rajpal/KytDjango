from .analysis import daytimeplot, getDateFilter, getDatof, getTimeDat, getTimeFilter, mostWatchedDays, plot_kw_freq, plotkwfreqMultiple, topNentries, indices_from_date
from django.http import request
from .forms import UploadFileForm
from django.shortcuts import render
from .models import MainRow
import numpy as np
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
import json


from django.shortcuts import render, get_object_or_404
class dataHandler(APIView):
    def get(self, request):
        global global_data
        def ser(row):
            ans = ""
            for i in range(7):
                ans = ans+str(row[i]) + "###"
            return ans
        # arr = list(np.apply_along_axis(ser, 1, global_data[:10, :]))
        return Response(json.dumps(global_data))
# Create your views here.
###add numpy to freeze list.
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
done = 0
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
def analyse_data(data):
    global global_data
    table, vals = topNentries(data)
    global_data['User1'] = {'TopNVideos': table}
    viewfreq = getTimeDat(data)
    global_data['User1']['viewFreq'] = viewfreq
    # kwtable = getDatof(data, [2, 3], ['Jiya', ''])
    # global_data['kwtable'] = json.dumps(kwtable)
    # daytime = daytimeplot(data, [['Crash Course'],['Glendale']])
    # global_data['daytime'] = json.dumps(daytime)
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
def updateUser(done,request):
    # print(done, "as received")
    return render(request, "kytube_land.html", {'done':done})
def getCSVfmt(file, request=None,get_proc=False):
    global global_data, done,delimit, mtoi, daysinmonths,indices_from_date
    # file = open('')
    # if(not file.isclose()):
    binary = file.read()
    text = codecs.encode(codecs.decode(binary), encoding='utf-8')
    raw = text.decode()
    arr_raw = raw.split('\n')
    # for inst in arr_raw:
    #     print(inst.split('<div class="content-cell').__len__())
    raw_instances = arr_raw[-1].split('<div class="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1">')
    # for ri in raw_instances:
    
    raw_instances.pop(0)
    rows = raw_instances.__len__()
    cols = 7
    
    data = np.empty([rows, cols],dtype='<U100')
    j=0
    l = len(raw_instances)
    # l = 
    i = l - 60
    for i in range(i,l):
        #add proccess bar informer
        done = i/l
        ri = raw_instances[i]
        detes = ri.split('Watched\xa0<a')
        # print(detes)
        try:
            segs = detes[1].split('>')
        except:
            # print(detes, "Error here.")
            continue
        # print(detes)
        title = segs[1][:-3]
        title = title.replace('&#39;', "'")
        title = title.replace('&amp;', '&')
        # data = title.decode("utf-8")
        # 
        channel = segs[4][:-3]
        link_vid = segs[0][7:-1]
        link_chan = segs[3][9:-1]

        date = segs[6][:-5]
        month = date[:3]
        try:
            day_date = int(date.split(',')[0][-2:])
            year = int(date.split(',')[1][-2:])
            index_by_month,index_by_date = indices_from_date(date)
            data[j] = np.array([index_by_month, index_by_date,title, channel, link_vid, link_chan, date])
            j+=1
        except:

            # print('Private Vid possibly at: ', detes)
            continue
        # print(index_by_month, title, channel, link_vid, link_chan)


    blank_first = np.where(data[:,1] == '')[0][0]
    # print(data[:,1])
    data = data[:blank_first,:]
    # clean = open('data_cleaned.csv', 'w')
    # np.savetxt('data_cleaned.csv', data,fmt='%s', encoding='utf8', delimiter=delimit)
    #django table entries:
    # def tabelize(row):
    #     # row[6] = 
    #     MainRow.objects.create(dayIndex=row[0], monthIndex=row[1], title=row[2], channel=row[3], titleLink=row[4], channelLink=row[5], moment = row[6])
    # return data
    # np.apply_along_axis(tabelize, 1, data)
    # global_data['total'] = data
    analyse_data(data)
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
    
def processData(data):
    print('HI')
    done = 0
    processor = myThread(1, 'pre', getCSVfmt, [data])
    processor.start()
    g_processor = processor
    # print(processor.setDaemon(False))
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