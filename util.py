def sort_records(records, order_by, order_direction='desc'):
    return sorted(records, key=lambda d: d[order_by], reverse=True if order_direction=='desc' else False)
