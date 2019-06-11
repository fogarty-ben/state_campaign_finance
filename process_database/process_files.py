import json, zipfile, csv
import sys, requests, os, io
import tempfile
import shutil
from contextlib import closing
from fake_useragent import UserAgent
import datetime as dt
import uuid
from dateutil.parser import parse


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
    print(new_row)
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
    for num, meta in enumerate(meta_row[14:35]):
        if not (meta + 1):
            item = ""
        elif meta:
            item = data_row[meta]
        new_row.append(item)
    new_row[21] = create_name(data_row, meta_row[24], meta_row[26], meta_row[25], meta_row[23])
    if len(new_row[14]) > 5:
        new_row[14] = new_row[14][:5]
    print(new_row)
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
        update += data_row[num]
    return update

def check_for_duplicates(filename):
    duplicate_check = set()
    count = 0
    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            if row[2] in duplicate_check:
                print("DUPLICATE", row[2],row[1:4])
            if not row[2] in duplicate_check:
                duplicate_check.add(row[2])
            if not count % 100000:
                print(count)
            count += 1

def check_for_numbers_errors(filename):
    count = 0
    last = 0
    skipped = 0
    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            count += 1
            if not row[9]:
                skipped += 1
                continue
            try:
                int(row[9])
            except:
                last += 1
                print(row[9], "|NUMBER 9|", count, last, skipped)
            if not count % 100000:
                print(count)




def summary_file(filename):
    zip_dict = {}
    date_dict = {}
    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        count = 0
        for row in reader:
            count += 1
            if row[3]:
                d_split = row[3].split(" ")
                new_split = d_split[0].split("-")
                date = dt.datetime(int(new_split[0]), int(new_split[1]), int(new_split[2]))
            else:
                date = False
            zip_code = row[23]
            if row[24]:
                amount = float(row[24])
            elif not row[24]:
                amount = 0
            if zip_code and zip_code not in zip_dict:
                zip_dict[zip_code] = [1, amount]
            elif zip_code and zip_code in zip_dict:
                zip_dict[zip_code][0] += 1
                zip_dict[zip_code][1] += amount

            if date and date not in date_dict:
                date_dict[date] = [1, amount]
            elif date and date in date_dict:
                date_dict[date][0] += 1
                date_dict[date][1] += amount
            if not count % 100000:
                print(count)


    with open("date_summary.csv", "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(["date", "count", "amount"])
        sort = sorted(date_dict.keys())
        for item in sort:
            writer.writerow([item, date_dict[item][0], date_dict[item][1]])

    with open("zip_summary.csv", "w") as csvfile_zip:
        writer = csv.writer(csvfile_zip, delimiter=",")
        writer.writerow(["date", "count", "amount"])
        sort = sorted(zip_dict.keys())
        for item in sort:
            writer.writerow([item, zip_dict[item][0], zip_dict[item][1]])



def load_new():
    with open("results3.csv", "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        with open("update_results.csv", "w") as csvfile_zip:
            writer = csv.writer(csvfile_zip, delimiter=",")
            next(reader)
            for row in reader:
                writer.writerow(row)


