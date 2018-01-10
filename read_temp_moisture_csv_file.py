import pandas

def read_temp_file(filePath):
    colnames = ['a','b']
    data = pandas.read_csv(filePath,names=colnames)
    x = data.a.tolist()
    y = data.b.tolist()
    return x, y


x, y = read_temp_file('moisture_with_time.csv')
print(x)
print(y)
