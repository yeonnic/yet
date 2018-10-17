#!/usr/bin/python
import sys
import re
import argparse
import solc

import utils.verified_parse as vp
import utils.getsource as gs

def constructor_check(data):
    tmp = re.sub('([ ]|[\n]|[\t])', '', data).lower()
    constructor_vuln = False

    fs = re.finditer('(functionconstructor[(])', tmp)

    f_list = [i for i in fs]

    if(len(f_list) > 0):
        constructor_vuln = True

    return constructor_vuln

def access_check(data):
    tmp = re.sub('([ ]|[\n]|[\t])', '', data).lower()
    access_con = False

    fs = re.finditer('require[(][a-zA-Z0-9|_]+[!][=]msg[.]sender[)]', tmp)

    f_list = [i for i in fs]

    if(len(f_list) > 0):
        access_con = True 

    return access_con

def tx_origin_check(data):
    tmp = re.sub('([ ]|[\n]|[\t])', '', data)
    tx_attack = False

    fs = re.finditer('(tx.origin[=][=]|[=][=]tx.origin)', tmp)
    
    f_list = [i for i in fs]

    for i in f_list:
        word = i.group()
        start = i.start()
        end = i.end()

        if(word == '==tx.origin' and tmp[start-10:start] != 'msg.sender'):
            tx_attack = True
        elif(word == 'tx.origin==' and tmp[end:end+10] != 'msg.sender'):
            tx_attack = True

    return tx_attack

def block_check(data):
    tmp = re.sub('([ ]|[\n]|[\t])', '', data)
    block_result = False
    blockhash_vuln = False

    fs = re.finditer('(block[.]|blockhash[(]block[.]number)', tmp)

    f_list = [i for i in fs]

    for i in f_list:
        if(i.group().find('blockhash') != -1):
            print('\x1b[91mblockhash use!!! warring!!!\x1b[0m')
        else:
            block_result = True

    return block_result

def check_main(address='', view_s = False, file_data = ''):

    if(len(address) > 0):
        print('address => ' + address)
        source = gs.sourceget(address)
    elif(len(file_data) > 0):
        print('file check')
        source = file_data
    else:
        return -1

    if view_s:
        gs.view_source(source)

    if(constructor_check(source)):
        print('\x1b[91mconstructor is vuln!!!\x1b[0m')
    if(tx_origin_check(source)):
        print('\x1b[91mtx.orgin is vuln!!!\x1b[0m')
    if(access_check(source)):
        print('\x1b[91maccess check gogo!!\x1b[0m')
    if(block_check(source)):
        print('\x1b[93mblock status using\x1b[0m')
    print('')

def verified_check(page=1):

    addrs = vp.verified_contract_list(page+1)

    for i in addrs:
        check_main(i)

def Usage():
    print("pattern_check [address | verified] [address_value | page_number]")
    exit(-1)

def main():
    viewc = False

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--address', help = "Contract Address")
    parser.add_argument('-v', '--verified')
    parser.add_argument('-vr', '--verified-range')
    parser.add_argument('-f', '--file')
    parser.add_argument('-V', '--view-source', action='store_true')
    
    args = parser.parse_args()
    non_args = parser.parse_args(['-V'])
    
    '''
    if non_args.view_source:
        print 'a'
        viewc = True
    '''
    if args.verified:
        verified_check(int(args.verified))

    if args.address:
        check_main(args.address, view_s = viewc) 

    if args.verified_range:
        for i in range(int(args.verified_range)):
            verified_check(i)

    if args.file:
        f = open(args.file, "r")
        fdata= ''
        tmp = f.read(1024)
        while tmp:
            fdata += tmp
            tmp = f.read(1024)

        check_main(file_data = fdata, view_s = viewc)

'''
    if(len(sys.argv) < 3):
        Usage()
    elif(sys.argv[1] == 'address'):
        check_main(sys.argv[2])
    elif(sys.argv[1] == 'verified'):
        if(sys.argv[2] == 'range'):
            for i in requestsange(int(sys.argv[3])):
                verified_check(i)
        else:
            verified_check(int(sys.argv[2]))
'''


if __name__ == '__main__':
    main()
