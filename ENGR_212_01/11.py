import shelve

dbtable=shelve.open("dbtable.db", writeback=True)
dbtable["akndkncsk"]=123
dbtable.close()
dbtable=shelve.open("dbtable.db", writeback=True)
print dbtable.keys()
dbtable.close()

