import yet
import pickle

sources = pickle.load(open("./db/source_list"))
addr_list = sources.keys()

'''
for i in range(len(addr_list)):
    print addr_list[i], 
    try:
        a = yet.tree(None, sources[addr_list[i]])

        print ' Owner :',

        for i in a.owner.keys():
            print i+ '() ' + a.owner[i][1]['name'] + ',',
    except Exception as e:
        pass
        #print 'error!'
    print ''
'''

compiled = yet.solc.compile_source(open("./test.sol").read(100000))
ast = compiled[compiled.keys()[0]]['ast']

b = yet.tree(ast)

print 'modifier list'
for i in b.modifier_list:
    print i['attributes']['name']

print 'function list'
for i in b.function_list:
    print i['attributes']['name']
print ''

for i in b.public_function_list:
    print i['attributes']['name']

print b.owner


'''
import pickle
import solc
import re

import utils.getsource as gs
import utils.verified_parse as vp

sources = pickle.load(open('./db/real_source_list', 'r'))
addr_list = sources.keys()

new_sources = {}

compiled_list = []
err_count = 0
for i in range(len(addr_list)):
    print str(i)

    #print gs.comment_remover(sources[addr_list[i]])
    #print gs.clear(sources[addr_list[i]])

    try:
        new_sources[addr_list[i]] = re.sub('pragma.+[\n]', '', gs.clear(sources[addr_list[i]]))
    except:
        print 'fuck!!'
        err_count += 1

    #compiled_list.append(solc.compile_source(tmp))

pickle.dump(new_sources, open("./db/real_source_list.tmp", "wb"))

print 'total error count : ' + str(err_count)
for i in addr_list:
    tmp_source = gs.comment_remover(sources[i])

    print gs.getcontractname(tmp_source)
'''
