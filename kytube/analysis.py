import math
import numpy as np
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

arr_or = np.vectorize(lambda x, y: x or y)
arr_and = np.vectorize(lambda x, y: x and y)
months = list(mtoi.keys())
itmo = {str(round(i/12, 2)):months[i] for i in range(12)}
rev_itmo = {str(itmo[x]):x for x in itmo}
ind_to_tick = lambda x: itmo[str(round(float(x) - math.floor(float(x)), 2))]+ str(math.floor(float(x)))
get_date = np.vectorize(lambda x: ','.join(x.split(',')[:2]))
get_time_12hr = np.vectorize(lambda x: ''.join((x.split(',')[-1]).split(' ')[:-1]))
ampm_to_24hr = np.vectorize(lambda x: int(x.split(':')[0]) + (12)*(int(x[-2:]=='PM')))
ampm_to_24hr_pre = np.vectorize(lambda x: int(x.split(':')[0]) + (12)*(int(x[-2:]=='PM')) + round(int(x.split(':')[1])/60, 2))
def indices_from_date(date):
    month = date[:3]
    day_date = int(date.split(',')[0][-2:])
    year = int(date.split(',')[1][-2:])
    index_by_month = str(year + round((1/12)*mtoi[month], 2))
    index_by_date = str(round(float(index_by_month)+ round(day_date/(12*daysinmonths[month]), 5), 5))
    return index_by_month, index_by_date
def colfreq(data, col_index, getUnsorted=False):
    # if(col_index==0):
    try:
        col = data[:,col_index]
    except:
        col = data
    # col = data[:,col_index]
    col, freq = np.unique(col, return_counts=True)
    s_freq,s_col = zip(*sorted(zip(freq, col)))
    if(getUnsorted):
        return col, freq
    return s_col, s_freq

def topNentries(data, title_index=2,N=10, showTable=True):
    s_titles, s_freq = colfreq(data, title_index)
    # print(len(s_titles), N)
    table_arr = []
    for i in range(1,min(N+1, len(s_titles))):
        table_arr.append([f"{i}",str(s_titles[-i]),f"{s_freq[-i]} times"])

    return (table_arr, np.array([s_titles, s_freq]).transpose()[::-1,:])
def getTimeDat(rows, mi=0, di=1, superMonths=[], superDays=[]):
    rows = np.array(rows)
    superMonths = np.unique(superMonths)
    superDays = np.unique(superDays)
    monthzeros = np.zeros(shape = len(superMonths))
    dayzeros = np.zeros(shape = len(superDays))
    i_m, i_m_c = np.unique(rows[:,mi], return_counts=True)
    # print(i_m)
    # print(superMonths)
    monthzeros[np.where(np.isin(superMonths, i_m))] = i_m_c
    # print(monthzeros)
    i_d, i_d_c = np.unique(rows[:,di], return_counts=True)
    dayzeros[np.where(np.isin(superDays,i_d))] = i_d_c
    return [[superMonths.tolist(), monthzeros.tolist()], [superDays.tolist(), dayzeros.tolist()]]
    
def getDatof(table, columns,list_of_kw, return_bools = False):
        table = np.array(table)
        for i in range(len(list_of_kw)):
            list_of_kw[i] = list_of_kw[i].lower()
        checksubstr = lambda arr, ss_arr: np.vectorize(lambda string: bool(sum([string.lower().count(ss) for ss in ss_arr])))(arr)
        bools = (np.ones(shape=(table.shape[0]))!=1)
        # print(bools)
        for i in columns:
            col = table[:,i]
            # kw = list_of_kw[0]
            where = checksubstr(col, list_of_kw)
            bools = arr_or(bools, where)
            # print(bools)
        if(return_bools):
            return table[bools].tolist(), bools.tolist()
        return table[bools].tolist()
def daytimeplot(data, kw_list):
    dates_times_literal = data[:,6]
    table = {}
    for kw in kw_list:
        prob=np.zeros(shape=(24,))
        hours_dat = ampm_to_24hr(get_time_12hr(dates_times_literal[getDatof(data, [2, 3], kw, return_bools=True)[1]]))
        u_hrs_dat, hrs_freq = np.unique(hours_dat, return_counts=True)
        u_hrs_dat = u_hrs_dat % 24
        prob[u_hrs_dat] += hrs_freq/len(hours_dat)
        table[f"Daytime probability of watching {kw[0]}"] = prob.tolist()
    #     plt.plot(np.arange(0, 24, 1), prob, label=f"Daytime probability of watching {kw[0]}")
    #     plt.title("")
    #     plt.legend()
    #     plt.xlim(0, 23)
    #     plt.ylim(0, max(plt.ylim()[1],np.max(prob)*1.1))
    #     plt.ylabel("Probability that a Youtube video in my History was watched in that Hour.")
    #     plt.xlabel("Time of the Day (24Hr)")
    #     plt.xticks(list(range(24)))
    # plt.show()
    return table
def plot_kw_freq(data,kw:list, title='', columns=[2, 3], avg_month=True, retExt=False):
        data = np.array(data)
        supermonths=data[:,0]
        superdays=data[:,1]
        superdates = data[:,-1]
        extm = (superdates[-1], superdates[0])
        # print(supermonths)
        # print(superdays)
        dat = getDatof(data, columns, kw)
        main = getTimeDat(dat, superMonths=supermonths, superDays=superdays)
        if(retExt):
            return main, extm
        else:
            return main
def plotkwfreqMultiple(data,kw:list, avg_month_=True,columns=[2, 3]):
    table = {}
    extdates = ""
    for kw_list in kw:
        main = plot_kw_freq(data, kw_list, kw_list[0], columns=columns,avg_month=avg_month_, retExt=True)
        table[kw_list[0]] = main[0]
        extdates = main[1]
        # ax = plot_kw_freq(data,kw_list, ax, kw_list[0], avg_month=avg_month_)
    # plt.show()
    return table, extdates
def getDateFilter(table, ll, ul, index=1):
    dim = table[:,index]
    ll = float(ll)
    ul = float(ul)
    dim = np.vectorize(lambda x:float(x))(dim)
    # print(dim)
    bools = arr_and(dim>=ll, dim<=ul)
    return table[bools].tolist()
def getTimeFilter(data,table, ll, ul):
    dates_times_literal = data[:,6]
    hours_dat = ampm_to_24hr(get_time_12hr(dates_times_literal))
    bools = arr_and(hours_dat>=ll,(hours_dat<=ul))
    hours_within_bounds = hours_dat[np.where(bools)]
    # print(hours_within_bounds)
    return table[bools].tolist()

def mostWatchedDays(data, N=10):
    dates_times_literal = data[:,6]
    # print(dates_times_literal)
    dates_literal = get_date(dates_times_literal)
    arr = topNentries(dates_literal, 0, N=N,showTable=False)[1]
    durs = np.zeros(shape=(len(arr), int(arr[0,1])))
    for i in range(len(arr[:N,0])):
        date = arr[i,0]
        # print(date)
        # print(data[:,1], date)
        indices = np.where(data[:,1]==str(float(indices_from_date(date)[1])))[0]
        if(indices==[]):
            print('error',date, indices_from_date(date)[1])
        # print(indices)
        rows = data[indices,-1:]
        rows = get_time_12hr(rows[::-1,0])
        # print(rows)
        rows = ampm_to_24hr_pre(rows)
        durs[i,:len(rows)] = rows
    e = min(N, len(durs))
    durs = durs[:e]
    arr = arr[:e]
    return durs.tolist(), arr.tolist()

