import os
HADOOP_HOME = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lib\winutils-master\hadoop-3.0.0")
os.environ["HADOOP_HOME"] = HADOOP_HOME
import pyspark
sc = pyspark.SparkContext.getOrCreate()
#sqlContext = pyspark.sql.SQLContext(sc)
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import HashingTF, Tokenizer, VectorAssembler
from pyspark.sql import Row
from pyspark.sql.functions import *
from pyspark.sql.types import ArrayType, IntegerType, StringType
import xlrd

def read_excel_xlrd(path):
    xl_workbook = xlrd.open_workbook(path)
    #sheet_names = xl_workbook.sheet_names()
    #print('Sheet Names', sheet_names)
    #xl_sheet = xl_workbook.sheet_by_name(sheet_names[0])
    xl_sheet = xl_workbook.sheet_by_index(0)
    #print ('Sheet name: %s' % xl_sheet.name)
    data = []
    for row in range(xl_sheet.nrows):
        line = []
        for col in range(xl_sheet.ncols):
            line.append(str(xl_sheet.cell(row, col).value))
        data.append(line)
    columnNames = data[0]
    dataValues = data[1:]
    dataPairs = []
    for row in range(len(dataValues)):
        line = {}
        for col in range(len(columnNames)):
            line[columnNames[col]] = dataValues[row][col]
        dataPairs.append(Row(**line))
    dataRDD = sc.parallelize(dataPairs)
    df = dataRDD.toDF()
    return df

def items_get(df, columnName, delimiter=None):
    rows = df.groupBy(columnName).count().collect()
    results = []
    for row in rows:
        if delimiter!=None:
            for item in row[columnName].split(delimiter):
                if item not in results:
                    results.append(item)
        else:
            if row[columnName] not in results:
                results.append(row[columnName])
    results.sort()
    return results

def exist_list(list_all, list_compared):
    results = []
    for item in list_all:
        if item in list_compared:
            results.append(1)
        else:
            results.append(0)
    return results

def df_column_add(df, input_colName, output_colName, function, returnType):
    function_udf = udf(lambda item: function(item), returnType)
    return df.withColumn(output_colName, function_udf(col(input_colName)))

def countEmptyAndNull(df):
    for columnName in df.columns:
        print(r"Column '%s' has %d '', %d 'noInfo', %d 'None', %d filled, and %d null rows."
              % (columnName, df.filter(df[columnName]=='').count(), df.filter(df[columnName]=='noInfo').count(),
                 df.filter(df[columnName]=='None').count(), df.filter(df[columnName]!='').count(),
                 df.filter(df[columnName].isNull()).count()))

sampleDataPath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sampleData\lib-statistics.xlsx")
df = read_excel_xlrd(sampleDataPath)
print(df.filter(df['Ödünç Sayısı'].isNull()).count())
print(df.filter(df['Ödünç Sayısı']=='').count())
df = df.withColumn('Sınıflama', split(df['Sınıflama'], " ")[0])
df = df.withColumn('Ödünç Sayısı', df['Ödünç Sayısı'].cast('float'))
print(df.filter(df['Ödünç Sayısı'].isNull()).count())
df = df.fillna({'Sınıflama' : 'noInfo', 'Eser Adı' : 'noInfo', 'Yazar' : 'noInfo', 'Dil' : 'noInfo', 'Konu Başlıkları' : 'noInfo' , 'Ödünç Sayısı' : 0.0})
print(df.filter(df['Ödünç Sayısı'].isNull()).count())