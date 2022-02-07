# Merges the second column of `inputfile` into the `colname` column of the `templatefile`

import argparse
import csv

parser = argparse.ArgumentParser(description="AH")
parser.add_argument('inputfile', type=str)
parser.add_argument("templatefile", type=str)
parser.add_argument('colname', type=str, metavar='N', nargs='+')
parser.add_argument("--notfound", type=str, default="notfound.csv")
parser = parser.parse_args()


class VirtualCSV:
    def __init__(self, file):
        self.first_line = None  # used to store first-line-specific information
        self.lines = []  # used to store line-specific information
        self.dico = {}  # used to store csv-global information, if need be

        with open(file) as csvfile:
            reader = csv.reader(csvfile, delimiter=",", quotechar='"')
            for i, row in enumerate(reader):
                if i == 0:
                    self.first_line_func(row)
                else:
                    self.line_func(row)

    def output(self, filename):
        string = ""
        if self.first_line is not None:
            string += self._output(self.first_line)

        for line in self.lines:
            string += self._output(line)

        with open(filename, "w") as f:
            f.write(string)

    def _output(self, content):
        content = [str(x) for x in content]
        content = ['"' + c + '"' if " " in c else c for c in content]
        return ",".join(content) + "\n"

    def first_line_func(self, row):
        raise NotImplementedError()

    def line_func(self, row):
        raise NotImplementedError()


class InputCSV(VirtualCSV):
    def __init__(self, file):
        super().__init__(file)

    def first_line_func(self, row):
        return self.line_func(row)  # first line not special

    def line_func(self, row):
        self.dico[row[0]] = row[1:]  # in dico, we want dico{matricule} = [grades]


class OutputCSV(VirtualCSV):
    def __init__(self, file, note_dico, colnames):
        self.colnames = colnames  # names of columns to match
        self.note_dico = note_dico  # note dict taken from input csv
        self.not_founds = []  # mats that couldnt be matched
        super().__init__(file)

    def first_line_func(self, row):
        def get_col_nb(colname):
            return row.index(colname)

        self.first_line = row
        self.mat_col_nb = get_col_nb("Matricule")  # remember column id of matricule
        self.colindices = []
        for name in self.colnames:
            self.colindices.append(get_col_nb(name))  # remember column id of columns to match in an ordered fashion

    def line_func(self, row):
        mat = row[self.mat_col_nb]  # get matricule string
        for colname_index, _ in enumerate(self.colnames):
            try:
                note = self.note_dico[mat][colname_index]  # get grade for column to match

                row[self.colindices[colname_index]] = float(note) * 100  # assign value to specific column in row
            except KeyError:
                self.not_founds.append(mat)  # remember matricules that couldn't be matched
        self.lines.append(row)
if __name__ == "__main__":
    input = InputCSV(parser.inputfile)

    output = OutputCSV(parser.templatefile, input.dico, parser.colname)
    output.output("results.csv")

    with open(parser.notfound, 'w') as f:
        for l in output.not_founds:
            f.write(l + "\n")
