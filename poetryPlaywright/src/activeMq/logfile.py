import datetime
import time, os, logging
from typing import Tuple

import pandas
from pandas import DatetimeIndex
from pyarrow import string

from activeMq.properties import Props

import advertools as adv

import pandas as pd

logger = logging.getLogger(__name__)


class Logfile:

    def set_ticket_interval(self) -> tuple[DatetimeIndex]:
        ticket_interval_end = datetime.datetime.now()
        ticket_interval_start = ticket_interval_end - datetime.timedelta(hours=1)

        ticket_interval_end_final = ticket_interval_end.strftime('%Y-%m-%d %H')
        ticket_interval_start_final = ticket_interval_start.strftime('%Y-%m-%d %H')

        # ticket_interval_final_idx = pandas.DatetimeIndex([ticket_interval_start, ticket_interval_end_final])
        # ticket_interval_end_final_idx = pandas.DatetimeIndex([ticket_interval_end_final])

        # .strftime('%Y-%m-%d %H:%m')
        # ticket_interval = '2024-03-08'
        return ticket_interval_end_final, ticket_interval_start_final

    def analyze_logfile(self, interval_start, interval_end) -> dict:
        logger.info("Start logfile analysis")

        props = Props()

        adv.logs_to_df(log_file=f"{props.LOG_PATH}/{props.LOG_FILE}",

                       output_file=f"{props.LOG_PATH}/{props.LOG_FILE}.parquet",

                       errors_file=f"{props.LOG_PATH}/{props.LOG_FILE}.errors",

                       log_format=r'([\d]{4}-[\d]{2}-[\d]{2} \d\d:\d\d:\d\d,[\d]{3})'
                       # r'(.*)'
                       # r'([A-Z]{4,5,6})'
                       # r'(.*)'
                                  r'(.*)',
                       # log_format='common',

                       fields=['datetime', 'message'])
        # fields=None)

        df = pd.read_parquet(f"{props.LOG_PATH}/{props.LOG_FILE}.parquet")
        # print(df.info)

        # df_last_lines = df.tail(10)
        # print(f"df_last_lines: {df_last_lines}")

        # df_today = df[df['datetime'].str.contains(ticket_interval)]

        df_today = df[df['datetime'].str.contains(f"{interval_start}|{interval_end}")]

        # i = pd.date_range('2024-03-15 00:00:00,000', periods=df_today.index.size, freq='10m')
        # df_today.set_index(i)

        # df_today2 = df_today[df_today['datetime'].between_time('07:30:00,000', '08:00:00,000')]

        print(f"df_get: {df_today}")
        print(f"df_get_count: {df_today.count()}")
        print(f"df_get_info: {df_today.info()}")

        # experimental:
        # df_filter = df_today[df_today['message'].apply(lambda x: extract(r"^.*(\Start message retry)$", expand=True)]
        # df_filter2 = pd.DataFrame({'df_filter': df_filter})
        # df_filter = df[df.message.str.match(r"^.*(?P<message>\Start message retry)$")]
        # df_filter = df_today[df_today['message'].str.contains("Start message retry", regex=True)]
        # df_extract = df_today[df_today['message'].str.extract(r"^.*((\n).*){9}(?P<message>\Start message retry)$")]
        # print(f"df_filter: {df_filter.filter(['message'])}")

        return df_today.tail(100).to_string()


lf = Logfile()
interval_start, interval_end = lf.set_ticket_interval()
dici = lf.analyze_logfile(interval_start, interval_end)
print(dici)
