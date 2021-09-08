from .forms import UploadFileForm
from django.shortcuts import render
import numpy as np
# Create your views here.
###add numpy to freeze list.


def getCSVfmt(file):
    raw = file.read()
    arr_raw = raw.split('\n')
    # for inst in arr_raw:
    #     print(inst.split('<div class="content-cell').__len__())
    raw_instances = arr_raw[-1].split('<div class="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1">')
    # for ri in raw_instances:
    delimit =  ' ,,, '
    raw_instances.pop(0)
    rows = raw_instances.__len__()
    cols = 7
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
    data = np.empty([rows, cols],dtype='<U100')
    j=0
    for i in range(len(raw_instances)):
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
            index_by_month = str(year + round((1/12)*mtoi[month], 2))
            print(index_by_month)
            index_by_date = str(round(float(index_by_month)+ round(day_date/(12*31), 5), 5))
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
    np.savetxt('data_cleaned.csv', data,fmt='%s', encoding='utf8', delimiter=delimit)
    titles_list = data[:,1]
    titles, freq = np.unique(titles_list, return_counts=True)
    s_freq,s_titles = zip(*sorted(zip(freq, titles)))
    # sorted_freq = np.sort(freq)
    print(s_freq)
    print(s_titles[-1])
    return data[:,:3]
def land(request):
    return render(request, "kytube_land.html")
def submit(request):
    # print(request.POST)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        # print(request.POST)
        if form.is_valid():
            data = request.FILES['data']
            # table = getCSVfmt(data)
            # print(table)
            print("hi")
    return render(request, "kytube_land.html")