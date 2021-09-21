#!/usr/bin/python

import matplotlib as mpl
import time
from bs4 import BeautifulSoup
import os

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')

mpl.rcParams['font.family'] = ['Heiti TC']

import matplotlib.pyplot as plt

def get_table_chart(df, identifier):

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(25,35))

    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    #df = pd.DataFrame(np.random.randn(10, 4), columns=list('ABCD'))
    print(df)
    tab = ax.table(cellText=df.values, colLabels=df.columns, loc='center')
    tab.auto_set_column_width(col=list(range(len(df.columns))))
    chartid = identifier + str(int(round(time.time() * 1000)))
 
    if not os.name == 'nt':
        chartpath = "/var/www/eggyolk.tech/html/report/" + chartid + '.png'
    else:
        pass    

    print(chartpath)
    urlpath = 'http://www.eggyolk.tech/report/%s.png' % chartid

    plt.tight_layout()
    plt.savefig(chartpath)
    return urlpath

def main():
    pass

if __name__ == "__main__":
    main()        
        

