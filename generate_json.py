import pandas as pd
from collections import defaultdict
import csv
import glob
from pyquery import PyQuery as pq
import os
import json
import sys

counties = {}
for line in csv.reader(open('national_county.txt')):
    code = int("%s%s"%(line[1], line[2]))
    counties[code] = line

def load_demographics():
    data = pd.read_csv('CC-EST2014-ALLDATA.csv')
    data = data[data['YEAR'] == data['YEAR'].max()]
    data['fips'] = data['STATE']*1000 + data['COUNTY']
    agedata = data
    data = data[data['AGEGRP'] == 0]
    data = data.set_index('fips')
    for fips, d in agedata.groupby('fips'):
        youngv = d[(d['AGEGRP'] >= 5) & (d['AGEGRP'] <= 7)]
        data.loc[fips,'millenials'] = youngv['TOT_POP'].sum()
    return data

def load_cbs_results():    
    stateresults = {}
    countyresults = defaultdict(dict)
    for f in glob.glob('cbsrip/County_*.xml'):
        d = pq(open(f).read())
        stateresult = defaultdict(lambda: 0)
        for c in d.find('county'):
            c = pq(c)
            for cnd in c.find('cand'):
                cnd = pq(cnd)
                name = cnd.attr('name').split()[-1].lower()
                votes = float(cnd.attr('votes'))
                stateresult[name] += votes
                countyresults[int(c.attr('fips'))][name] = votes
        stateresults[d.attr('state')] = stateresult

    countyshares = defaultdict(dict)
    for cid, cinfo in counties.iteritems():
        if cid in countyresults:
            cr = countyresults[cid]
        elif cinfo[0] in stateresults:
            cr = stateresults[cinfo[0]]
        else:
            continue
        total = sum(cr.values())
        if total == 0:
            continue
        for cand, votes in cr.iteritems():
            countyshares[cand][cid] = votes/float(total)*100
    
    return countyshares

def tryval(f):
    try:
        f()
    except KeyError:
        return None

def main():
    demos = load_demographics()
    dstdir = sys.argv[1]
    voteshares = load_cbs_results()
    index = {}
    for cand, voteshare in voteshares.iteritems():
        fname = "%s.json"%cand
        output = defaultdict(list)
        index[cand] = {'name': cand.title()}
        for cid, share in voteshare.iteritems():
            try:
                demo = demos.loc[cid]
            except KeyError:
                print "Skipping"
                continue
            output['vote_share'].append(share)
            cinfo = counties[cid]
            output['place_name'].append("%s, %s"%(cinfo[3], cinfo[0]))
            output['place_fips'].append(cid)
            output['female_share'].append(demo['TOT_FEMALE']/float(demo['TOT_POP'])*100)
            output['white_share'].append((demo['WA_FEMALE'] + demo['WA_MALE'])/float(demo['TOT_POP'])*100)
            output['black_share'].append((demo['BA_FEMALE'] + demo['BA_MALE'])/float(demo['TOT_POP'])*100)
            output['hispanic_share'].append((demo['H_FEMALE'] + demo['H_MALE'])/float(demo['TOT_POP'])*100)
            output['millenial_share'].append((demo['millenials'])/float(demo['TOT_POP'])*100)
        json.dump(output, open(os.path.join(dstdir, fname), 'w'))
    json.dump(index, open(os.path.join(dstdir, 'index.json'), 'w'))

if __name__ == '__main__': main()
