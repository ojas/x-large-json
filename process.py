#!/usr/bin/env python

import ijson
import csv
import sys
from flattener import Flattener


flattener = Flattener()

#columns = request.GET.get('columns')
#columns = columns.split(',') if columns is not None else None
flattener.one_index = True
flattener.delimiter = '_'
#flattener.columns = columns
#if columns is not None:

all_cols = {}
item_count = 0

in_file = sys.argv[1]
with open(in_file, 'r') as f:
#with open('data.json', 'r') as f:
    objects = ijson.items(f, 'item')
    for obj in objects:
        item_count += 1
        csv_row = flattener.to_dict(obj)
        cols = csv_row.keys()
        for col in cols:
            all_cols[col] = 1


    all_cols = sorted(all_cols.keys())
    f.seek(0)
    objects = ijson.items(f, 'item')
    writer = csv.DictWriter(sys.stdout, all_cols, extrasaction='ignore')
    writer.writeheader()
    for obj in objects:
        csv_row = flattener.to_dict(obj)
        writer.writerow(csv_row)


