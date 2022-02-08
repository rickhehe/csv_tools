import os
import re
import calendar
from datetime import datetime, date, timedelta
import time
import pytz

import pandas as pd
import numpy as np

def get_nz_today():

    x = datetime.now(pytz.utc)

    nzdt = pytz.timezone('nz')
    nz_now = x.astimezone(nzdt)

    nz_today_as_string = nz_now.date().isoformat() 

    return nz_today_as_string

def now_suffix():

    suffix = datetime.now().strftime("%Y%m%d_%H%M%S")

    return suffix
    
def datetime_csv_suffix(filename):

    filename = re.sub(
        r'\.csv$',
        '',
        filename,
        flags=re.I,
    )

    suffix = now_suffix()

    return f'{filename}_{suffix}.csv'

def get_df_holidays_warehouse(df_holidays, warehouse):

    df_holidays_warehouse = df_holidays[
        df_holidays[warehouse]==1
        ].date
        
    return df_holidays_warehouse.dt.date  # tricky

def get_yesterday_as_str(a_date=get_nz_today(),holidays=[]):

    yesterday = np.busday_offset(
        a_date,
        offsets=-1,
        roll='forward',
        holidays = holidays,
    )

    return str(yesterday)

def get_workday_count(start, finish, holidays=[]):
    
    '''
    start and finish should data series.
    '''

    help_column = finish.fillna(
        get_nz_today()
    )

    difference = np.busday_count(
        help_column,
        start,
        holidays=holidays,
    )
    
    return difference

def get_status_description(difference):

    if difference < -2:
        return '3 or 3+ days late'
    elif difference < -1:
        return '2 days late'
    elif difference < 0:
        return '1 day late'
    elif difference == 0:
        return 'done on time'
    else:
        return 'done in advance'

def modified_within(path, x):

    t0 = os.path.getmtime(path)    
    t1 = calendar.timegm(time.gmtime())

    return t1 - t0 < x
