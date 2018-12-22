input_file = 'fide_historical.csv'
import re

def getElement(line):
    result = re.split(r',', line, maxsplit=1)
    element = result[0].strip()
    return element, result[1]

def getRankingDate(line):
    result= re.split(r',', line, maxsplit=1)
    ranking_date = re.findall(r'\d{2}-\d{2}-\d{2}', result[0])[0]
    return ranking_date,result[1]
def getRank(line):
    result = re.split(r',' , line , maxsplit = 1)
    rank = re.findall(r'\d+', result[0])[0]
    return rank,result[1]
def getName(line):
    result = re.split(r'"', line, maxsplit=2)
    name = re.findall(r'\w+', result[1])[0]
    surname= re.findall(r'\w+',result[1])[1]
    h = name+' '+surname
    return h, result[2][1:]
def getTitle(line):
    title, line = getElement(line)
    return title,line



try:
    with open('fide_historical.csv',encoding='utf-8',mode='r') as file:
        file.readline()
        dataset = dict()
        line_number = 1
        i=1
        for line in file:
            line = line.strip().rstrip()
            line_number += 1
            if not line:
                continue
            ranking_date,line = getRankingDate(line)
            rank,line=getRank(line)
            name,line=getName(line)
            title,line=getTitle(line)
            if ranking_date in dataset:
                if title in dataset[ranking_date]:
                    dataset[ranking_date][title][name]=rank
                else:
                    dataset[ranking_date][title]={name:rank}
            else:
                dataset[ranking_date] = {}
            if i==1:
                dataset[ranking_date][title] = {name: rank}
                i+=1
except IOError as e:
   print ("I/O error({0}): {1}".format(e.errno, e.strerror))

except ValueError as ve:
    print("Value error {0} in line {1}".format(ve, line_number))
import plotly
import plotly.graph_objs as go
x=[]
y=[]
for data in list(dataset.keys()):
    titles= dataset[data]
    for title in list(titles.keys()):
        x.append(data)
        y.append(title)
trace = go.Scatter(x=x,y=y)
plotly.offline.plot([trace], filename='plotly.html')
datas ={}
for data in list(dataset.keys()):
    titles = dataset[data]
    for title in list(titles.keys()):
        names = titles[title]
        l = list(names.values())
        k = []
        for i in l:
            k.append(int(i))
        k.sort()
        datas[data] = k[0]
res=list(datas.values())
bar = [go.Bar(x=x,y=res)]
plotly.offline.plot(bar, filename='plotly_2.html')