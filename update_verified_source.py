#!/usr/bin/python
import pickle
import bs4
import sys
import requests
import re

import utils.getsource as gs
import utils.verified_parse as vp

def main():

    verified_addr_list = {}
    with open('./db/verified_addr_list', 'r') as f:
        verified_addr_list = pickle.load(f)
        f.close()
    sources = {}
    with open('./db/source_list', 'r') as f:
        sources = pickle.load(f)
        f.close()

    print 'verified addr list length : ' + str(len(verified_addr_list))

    start_idx= input('Enter the start page : ')
    end_idx = input('Enter the end page : ')

    for i in range(start_idx, end_idx):
        #l = vp.verified_contract_list()
        print str(i)
        if(i % 100 == 0):
            print 'save point!'
            with open('./db/source_list', 'wb') as f:
                pickle.dump(sources, f)
                f.close()

        sources[verified_addr_list[i]] = gs.sourceget(verified_addr_list[i])

    with open('./db/source_list', 'wb') as f:
        pickle.dump(sources, f)
        f.close()



if __name__ == '__main__':
    main()
