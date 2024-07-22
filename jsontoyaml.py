import json
import sys
import yaml
''' 
Converts NR dashboard in json format to 
Tac yaml
IBM - Copyright 2024
Written by Andrew Lee
'''

def fix(x):
    '''
    somtimes NR json include space at the end of nrql query and ':'. 
    this function removes ':' ,space,and '\n' at the end of query
    '''
    y=list(x)
    z=y[0].replace(':','$')
    z=z.replace('\n',' ')
    if z[-1]==' ':
       z=z[:-1]
    #z={z}
    return z 
def extract(t):
    tabl,lyne,bill,mark = [[] for _ in range(4)]
    new,layout,b_layout,li_layout,ti,m_layout = [{} for _ in range(6)]
    for x in t['widgets']:  # search O(n)  linear run time.
        widget=x['visualization']['id']
        if widget != 'viz.markdown':
            z=fix({x['rawConfiguration']['nrqlQueries'][0]['query']})
        if widget=='viz.table':
            layout=x['layout']
            ti['title']=x['title']
            layout.update({'title':x['title']})
            x['rawConfiguration']['nrqlQueries'][0]['query']=z
            layout.update({'nrql':x['rawConfiguration']['nrqlQueries'][0]['query']})
            ti.update(layout)
            tabl.append(layout)
        if 'line' in widget:
            li_layout=x['layout']
            li_layout.update({'title':x['title']})
            x['rawConfiguration']['nrqlQueries'][0]['query']=z
            li_layout.update({'nrql':x['rawConfiguration']['nrqlQueries'][0]['query']})
            lyne.append(li_layout)
        if widget=='viz.billboard':
            b_layout=x['layout']
            b_layout.update({'title':x['title']})
            x['rawConfiguration']['nrqlQueries'][0]['query']=z
            b_layout.update({'nrql':x['rawConfiguration']['nrqlQueries'][0]['query']})
            bill.append(b_layout)
        if widget=='viz.markdown':
            m_layout=x['layout']
            m_layout.update({'title':x['title']})
            m_layout.update({'text':x['rawConfiguration']['text']})
            mark.append(m_layout)
    
    if len(tabl) > 0:
        ''' add widget name'''
        new['widget_table']=tabl
    if len(lyne) > 0:
        new['widget_line']=lyne
    if len(bill) > 0:
        #print(bill)
        new['widget_billboard']=bill
    if len(mark) > 0:
       new['widget_markdown']=mark
    return new

def main():
    x = sys.argv[1]
    with open(x, "r") as f:
        content = json.load(f)
    modif=[]
    p={} # page
    db={} #dashboard
    xtemp={}
    result=[]
    for item in content['pages']:
        new=extract(item)
        move={}
        move['name']=item['name']
        move.update(new)
        result.append(move)
    p['pages']=result
    xtemp = list(p.items())
    xtemp.insert(0, ('title', content["name"]))
    xtemp.insert(0,('name','foo'))
    p=dict(xtemp)
    db['dashboard']=p
    #print(p['pages'][0]['widget_table'])
    yaml_string=yaml.dump(db,sort_keys=False,default_flow_style=False)
    print(yaml_string)

if __name__=='__main__':
    main()
