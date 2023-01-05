# coding: utf8
import os
import PyPDF2
import camelot
import pandas
import sys


def extraction(path):
    file_name = path.replace('uploads/', '')
    try:
        PyPDF2.PdfFileReader(open(path, "rb"))
    except PyPDF2._utils.PdfStreamError:
        print("invalid PDF file")
    else:
        if not path.endswith('.pdf'):
            os.rename(path, path+'.pdf')
            path += '.pdf'
        if not os.path.isdir(f'uploads/tables/{file_name}'):
            os.mkdir(f'uploads/tables/{file_name}')

        tables = camelot.read_pdf(path, stream=True, pages='all')

        for k in range(len(tables)):
            left_x, left_y, right_x, right_y = 596, 896, 0, 0
            for i in range(len(tables[k].cells)):
                for j in range(len(tables[k].cells[i])):
                    left_x = min(left_x, tables[k].cells[i][j].x1)
                    left_y = min(left_y, tables[k].cells[i][j].y1)
                    right_x = max(right_x, tables[k].cells[i][j].x2)
                    right_y = max(right_y, tables[k].cells[i][j].y2)
            tables[k].df = pandas.concat([tables[k].df,
                                          pandas.DataFrame(['table information',
                                                            'page', tables[k].page,
                                                            'table area', left_x, left_y, right_x, right_y,
                                                            'rows', len(tables[k].rows),
                                                            'columns', len(tables[k].cols)]
                                                           )],
                                         ignore_index=True)
        tables.export(f'uploads/tables/{file_name}/{file_name}.csv',
                      f='csv',
                      compress=False)
        if path.endswith('.pdf'):
            os.rename(path, path.replace('.pdf',''))


if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2])
