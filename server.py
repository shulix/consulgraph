from jaal import Jaal
import pandas as pd
import numpy as np
import json

from urllib.request import urlopen

#all=[]
services=[]
response = urlopen("http://10.16.16.102:8500/v1/catalog/services")
json_data = response.read().decode('utf-8', 'replace')
d = json.loads(json_data)

for service in d.keys():
    response = urlopen("http://10.16.16.102:8500/v1/catalog/service/"+service)
    json_data = response.read().decode('utf-8', 'replace')
    d = json.loads(json_data)
#   all.append(d)
    for node in range(len(d)):      
        nodewithip=str(d[node]["Node"])+"_"+str(d[node]["Address"])
        nodemap = {"service":service, "nodes":nodewithip}
        services.append(nodemap)

df = pd.json_normalize(services)

values = ['ctrl', 'taptica', 'ondemand','workflow']
conditions = list(map(df['nodes'].str.contains, values))
df['product'] = np.select(conditions, values, 'other')
nodecount=df.pivot_table(index=['service'], aggfunc ='size')
df1 = nodecount.reset_index()
df.to_pickle('service.pkl')
df1.to_pickle('nodes.pkl')

df=df.rename(columns={"service": "from", "nodes": "to"})
df1=df1.rename(columns={"service": "id"})
print(df)
print(df1)
#df2 = pd.DataFrame().assign(Courses=df['from'])
#Jaal(df).plot(vis_opts={'height': '1000px', # change height
#                        'interaction':{'hover': True}, # turn on-off the hover 
#                        'physics':{'stabilization':{'iterations': 100}}}) # define the convergence iteration of network

if __name__ == '__main__':
    Jaal(df).plot(directed=True,vis_opts={'height': '1000px', 
                            'interaction':{'hover': True}, # turn on-off the hover 
                            'physics':{'stabilization':{'iterations': 100}}}) # define the convergence iteration of network