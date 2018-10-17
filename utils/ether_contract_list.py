import requests, re, pickle, time

import getsource as gs

sources = {}
ether_sources = {}

with open("../db/real_source_list", "r") as f:
    sources = pickle.load(f)
    f.close()
with open("../db/ether_source_list", "r") as f:
    ether_sources = pickle.load(f)
    f.close()

addr_list = ether_sources.keys()

'''
for i in range(31900, len(addr_list)):
    if i%100 == 0:
        with open('../db/ether_source_list', 'wb') as f:
            pickle.dump(ether_sources, f)
            f.close()
        print str(i) + '!!'
    
    balance = int(gs.getbalance(addr_list[i]))
    print str(balance)  + ' Wei'
    if balance > 10**16:
        ether_sources[addr_list[i]] = [sources[addr_list[i]], balance]
'''

ether_sources = {}
for i in range(len(addr_list)):
    print i
    try:
        if(i % 100 == 0):
            with open("../db/ether_source_list.tmp", "wb") as f:
                pickle.dump(ether_sources, f)
        ether_sources[addr_list[i]] = gs.clear(sources[addr_list[i]])
    except:
        print 'error!'

