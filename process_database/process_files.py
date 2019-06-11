import json, zipfile, csv
import sys, requests, os, io
import tempfile
import shutil
from contextlib import closing
from fake_useragent import UserAgent
import datetime as dt
import uuid

def main(filename, results="results.csv"):
    headers = requests.utils.default_headers()
    headers.update({'User-Agent': str(UserAgent())})

    with open(results, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        main_header = ["primary_key","committee_state","trans_id","date",
            "committee_cd","committee_type","commitee_name","trans_type",
            "trans_subtype","contrib_commitee_cd","contrib_org",
            "contrib_full_name","contrib_prefix","contrib_suffix",
            "contrib_first","contrib_middle","contrib_last",
            "contrib_occupation","contrib_employer","contrib_addr_line_1",
            "contrib_addr_line_2","contrib_city","contrib_state","contrib_zip",
            "amount"]
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            table = []
            next(reader)
            for row in reader:
                row = new_row_meta(row)
                if row[3].lower() == "zip":
                    print("test")
                    response = requests.get(row[1], headers=headers)
                    zipfile_load(writer, row, response)
                elif row[3].lower() == "csv":
                    csvfile_load_online(writer, row)


def new_row_meta(meta_row):
    row = []
    for num, meta in enumerate(meta_row[10:35]):
        if not (num - 3):
            row.append(meta)
        elif meta:
            row.append(int(meta))
        else:
            row.append(-1)
    new_row = meta_row[0:10] + row
    return new_row

def zipfile_load(table, row, response):
    print("preparing")
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        print("starting")
        zip_ref.extractall("new_data/")
        path = "new_data/" + row[7]
        print("success")
        items_in_path = os.listdir(path)
        print(items_in_path)
        if not row[5]:
            csvfile_local(table, row[6], row)
        if row[5]:
            count = 1
            new_row = row[5] + str(count) + ".csv"
            new_row_alt = row[5] + "0" + str(count) + ".csv"
            print(new_row, new_row_alt)
            while (new_row in items_in_path or new_row_alt in items_in_path):
                print(new_row, new_row_alt)
                if new_row in items_in_path:
                    csvfile_local(table, path + new_row, row)
                elif new_row_alt in items_in_path:
                    csvfile_local(table, path + new_row_alt, row)     
                count += 1
                new_row = row[5] + str(count) + ".csv"
                new_row_alt = row[5] + "0" + str(count) + ".csv"
        shutil.rmtree(path)

def csvfile_local(writer, filename, meta_row):
    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        row_num = 0
        header = next(reader)
        print(header)
        for data_row in reader:
            process_row(writer, meta_row, data_row)
            if not row_num % 10000:
                print(filename, row_num)
            row_num += 1



def csvfile_load_online(writer, meta_row):
    with closing(requests.get(meta_row[1], stream=True)) as r:
        reader = csv.reader(r.iter_lines(decode_unicode=True), delimiter=',', quotechar='"')
        row_num = 0
        header = next(reader)
        print(header)
        for data_row in reader:
            process_row(writer, meta_row, data_row)
            if not row_num % 50000:
                print("online", row_num)
            row_num += 1
            

def process_row(writer, meta_row, data_row):
    new_row = [uuid.uuid4(), meta_row[0]]
    new_row.append(data_row[meta_row[11]])
    if data_row[meta_row[12]]:
        new_row.append(dt.datetime.strptime(data_row[meta_row[12]], meta_row[13]))
    else:
        new_row.append("")
        print(data_row)
    for num, meta in enumerate(meta_row[14:35]):
        if meta:
            item = data_row[meta]
        elif not (meta + 1):
            item = ""
        new_row.append(item)
    new_row[21] = create_name(data_row, meta_row[24], meta_row[26], meta_row[25], meta_row[23])
    writer.writerow(new_row)




def create_name(data_row, first, last, middle=False, suffix=False):
    name = ""
    name += add_name(name, data_row, first)
    name += add_name(name, data_row, middle)
    name += add_name(name, data_row, last)
    name += add_name(name, data_row, suffix)

    return name

def add_name(name, data_row, num):
    update = ""
    if (num + 1) and data_row[num]:
        if name:
            update += " "
        update = data_row[num]

    return update

