from datetime import datetime


def sort_records(records, order_by, order_direction='desc'):
    for record in records:
        for k,v in record.items():
            if k == 'submission_time':
                record[k] = unix_date_to_readable_date(record[k])
    return sorted(records, key=lambda d: d[order_by], reverse=True if order_direction=='desc' else False)


def unix_date_to_readable_date(unix_date):
    unix_date = int(unix_date)
    return datetime.utcfromtimestamp(unix_date).strftime('%Y-%m-%d %H:%M:%S')
