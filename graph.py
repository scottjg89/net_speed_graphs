#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import re
import sys
from os import popen
from datetime import datetime
from datetime import timedelta


def graph(date):
    N = 0
    dlList = []
    ulList = []
    std = []
    tms = []
    hst = popen('hostname').read()
    if hst == 'raspberrypi\n':
        file = open('/mnt/Public/speed/{}-speed.log'.format(date), 'r').readlines()
    else:
        file = open('/Volumes/Public/speed/{}-speed.log'.format(date), 'r').readlines()
    for line in file:
        if not len(line) < 5:
            N = N + 1
            std.append(5)
            time = re.findall(r'\d{2}:\d{2}', line)[0]
            tms.append(time)
            dl = float(re.findall(r'(?<=D: )\d{1,3}\.\d{2}', line)[0])
            ul = float(re.findall(r'(?<=U: )\d{1,3}\.\d{2}', line)[0])
            dlList.append(dl)
            ulList.append(ul)

    ind = np.arange(N)  # the x locations for the groups
    width = 0.5       # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, dlList, width, color='r', yerr=std)
    rects2 = ax.bar(ind + width, ulList, width, color='y', yerr=std)

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Mbs/s')
    ax.set_title('Hourly internet speed test results {}'.format(date))
    ax.set_xticks(ind + width)
    ax.set_xticklabels(tms)

    ax.legend((rects1[0], rects2[0]), ('Download', 'Upload'))

    autolabel(rects1, ax)
    autolabel(rects2, ax)

    plt.show()


def autolabel(rects, ax):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                '%d' % int(height),
                ha='center', va='bottom')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        dr = sys.argv[1]
    else:
        dr = datetime.now().strftime('%d-%m-%y')
    try:
        drs = dr.split('-')
        if datetime(year=int(drs[2]), month=int(drs[1]), day=int(drs[0])):
            graph(dr)
    except ValueError:
        print('Incorrect date!')
    except IndexError:
        if dr == 'yday':
            date = datetime.today() - timedelta(days=1)
            graph(date.strftime('%d-%m-%y'))
        elif 'yday' in dr:
            try:
                date = datetime.today() - timedelta(days=int(dr[0:2]))
                graph(date.strftime('%d-%m-%y'))
            except ValueError:
                try:
                    date = datetime.today() - timedelta(days=int(dr[0]))
                    graph(date.strftime('%d-%m-%y'))
                except ValueError:
                    print('Err 1:Incorrect date! Check formatting (dd-mm-yy or yday or 2yday/3yday etc)')
                except IOError:
                    print('Err 3.3: IO Error {}-speed.log not found'.format(date.strftime('%d-%m-%y')))
            except IOError:
                print('Err 3.2: IO Error {}-speed.log not found'.format(date.strftime('%d-%m-%y')))
        else:
            print('Err 2: Incorrect date! Check formatting (dd-mm-yy or yday or 2yday/3yday etc)')
    except IOError:
        print('Err 3.1: IO Error {}-speed.log not found'.format(dr))
