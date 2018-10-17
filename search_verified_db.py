import pickle
import sys
import re

import utils.getsource as gs

sources = {}
addr_list = []

with open("./db/real_source_list", "r") as f:
    sources = pickle.load(f)
    addr_list = sources.keys()

'''
with open("./db/source_list", "r") as f:
    sources = pickle.load(f)
    addr_list = sources.keys()
'''

'''
with open("./db/ether_source_list", "r") as f:
    tmp = pickle.load(f)
    addr_list = tmp.keys()
    for i in addr_list:
        sources[i] = tmp[i][0]
'''



if(len(sys.argv) == 2):
    for i in addr_list:
        sources[i] = re.sub('([ ]|[\n]|[\t]|[\r])', '', sources[i]).lower()
        #sources[i] = re.sub('([\n]|[\t])', '', sources[i]).lower()
        #sources[i] = gs.comment_remover(sources[i])
check = True
while check:
    word = raw_input('give me word : ')
    badword = raw_input('enter the bad word : ')
    tmp_source = {}
    count = 0
    for i in addr_list:
        if(sources[i].find(word) != -1 and sources[i].find(badword) <= 0):
            print 'find ! => ' + i + ' count : ' + str(count+1)
            count += 1
            tmp_source[i] = sources[i]

    if(raw_input('keep in the search? ').lower() == 'y'):
        sources = tmp_source
        addr_list = sources.keys()

    else:
        check = False

