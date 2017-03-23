#-*- coding: utf-8 -*-

from xlrd import *
from anydbm import *

curriculumdb=open("curriculum.db","c")

wb = open_workbook('cs.xlsx')
sheet_name=None
semester_row_no__dic={}
semester_col_no__dic={}
semester_no=0

code_by_semester={}
title_by_semester={}
credit_by_semester={}

for s in wb.sheets():
    if "curriculum" in s.name:
        sheet_name=s.name
        for row in range(s.nrows):
            for col in range(s.ncols):
                if type(s.cell(row,col).value)==float:
                    pass
                elif type(s.cell(row,col).value)==int:
                    pass
                elif "Semester I" in s.cell(row,col).value:
                    semester_no+=1
                    semester_row_no__dic[semester_no]=row
                    semester_col_no__dic[semester_no]=col
                    print s.cell(row,col).value
                elif "Semester V" in s.cell(row,col).value:
                    semester_no+=1
                    semester_row_no__dic[semester_no]=row
                    semester_col_no__dic[semester_no]=col
                    print s.cell(row,col).value
        semester_row_no__dic[semester_no+1]=semester_row_no__dic[semester_no-1]+9
        semester_row_no__dic[semester_no+2]=semester_row_no__dic[semester_no]+9
        for i in range(semester_no):
            semester="Semester "+str(i+1)
            code_row=None
            code_col=None
            title_col=None
            credit_col=None

            start_row=semester_row_no__dic[i+1]
            start_col=semester_col_no__dic[i+1]
            end_row=semester_row_no__dic[i+3]
            end_col=semester_col_no__dic[i+1]+7

            for row in range(start_row,end_row):
                for col in range(start_col,end_col):
                    if type(s.cell(row,col).value)==float:
                        pass
                    elif type(s.cell(row,col).value)==int:
                        pass
                    elif "Code" in s.cell(row,col).value:
                        code_row=row
                        code_col=col
            for col in range(start_col,end_col):
                if type(s.cell(code_row,col).value)==float:
                    pass
                elif type(s.cell(code_row,col).value)==int:
                    pass
                elif "Title" in s.cell(code_row,col).value:
                    title_col=col
                elif "Cr" in s.cell(code_row,col).value:
                    credit_col=col
            codes=[]
            titles=[]
            creditss=[]
            for row in range(code_row+1,end_row):
                if s.cell(row,code_col).value!="":

                    codes.append(str(s.cell(row,code_col).value))
                    titles.append(str(s.cell(row,title_col).value))
                    creditss.append(str(s.cell(row,credit_col).value))
            code_by_semester[semester]=codes
            title_by_semester[semester]=titles
            credit_by_semester[semester]=creditss

print code_by_semester
print title_by_semester
print credit_by_semester
print code_by_semester["Semester 1"][0]
print len(code_by_semester["Semester 1"])



#print curriculumdb

curriculumdb.close()
