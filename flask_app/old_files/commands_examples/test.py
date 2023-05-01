from datetime import datetime
from dateutil.relativedelta import relativedelta


ptn_start_date = datetime(2023, 1, 1)

for i in range(12):
    ptn_year = ptn_start_date.strftime("%y")
    ptn_month = ptn_start_date.strftime("%m")
    ptn_start = ptn_start_date.strftime("%Y-%m-%d")
    ptn_end_date = ptn_start_date + relativedelta(months=1)
    ptn_end = ptn_end_date.strftime("%Y-%m-%d")

    partition_str = f"CREATE TABLE IF NOT EXISTS history_{ptn_year}_{ptn_month} PARTITION OF histories FOR VALUES FROM ('{ptn_start}') TO ('{ptn_end}')"

    print(partition_str)

    ptn_start_date = ptn_end_date
