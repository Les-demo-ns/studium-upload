# Merges a "notes.csv" CSV in MAT,NOTE format with a studium import csv "studium.csv"

import argparse
import subprocess

parser = argparse.ArgumentParser(description="AH")
parser.add_argument('inputfile', type=str)
parser.add_argument("templatefile", type=str)
parser.add_argument('colname', type=str, metavar='N', nargs='+')
parser.add_argument("--notfound", type=str, default="notfound.csv")
parser = parser.parse_args()

def do_csv(name, line_func, first_line_func):
    import csv
    with open(name) as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar='"')
        for i, row in enumerate(reader):
            if i == 0:
                first_line_func(row)
            else:
                line_func(row)

def get_col_nb(colname_list: list, colname):
    return colname_list.index(colname)

def output(filename, content: list):
    content = ['"'+c+'"' if " " in c else c for c in content]
    with open(filename, "a") as f:
        f.write(",".join(content) + "\n")

def run(command):
    subprocess.run(command, shell=True, capture_output=True, check=True, universal_newlines=True)

note_dict = {}
def addto(line): note_dict[line[0]] = line[1:]
do_csv(parser.inputfile, addto, addto)

firstline = []
def getfirstline(x):
    firstline.append(x)
    output(tempfile, x)
import time
tempfile = time.strftime("%s%D%Y%h").replace("/", "")
not_founds = []
def modnote(line):
    fline = firstline[0]
    mat = line[get_col_nb(fline, "Matricule")]
    for iname, name in enumerate(parser.colname):
        try:
            note = note_dict[mat][iname]
            line[get_col_nb(fline, name)] = note
        except KeyError:
            not_founds.append(mat)
    output(tempfile, line)
do_csv(parser.templatefile, modnote, getfirstline)

run(f"rm -rf {parser.templatefile}")
run(f"cp {tempfile} {parser.templatefile}")
run(f"rm -rf {tempfile}")

for l in not_founds:
    output(parser.notfound, [parser.inputfile, l])