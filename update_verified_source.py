#!/usr/bin/python
import pickle
import bs4
import sys
import requests
import re

import utils.getsource as gs
import utils.verified_parse as vp

def main():

    sources = {}
    with open('./db/source_list', 'r') as f:
        sources = pickle.load(f)

    start_page = input('Enter the start page : ')
    end_page = input('Enter the end page : ')

    for i in range(start_page, end_page):
        l = vp.verified_contract_list(i+1)
        
        for j in l:
            sources[j] = gs.sourceget(j)
            print j + ' source get'

    with open('./db/source_list', 'wb') as f:
        pickle.dump(sources, f)


if __name__ == '__main__':
    main()
