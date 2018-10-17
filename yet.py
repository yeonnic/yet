#!/usr/bin/python
import solc
import re
import argparse

import utils.verified_parse as vp
import utils.getsource as gs

class tree:
    def __init__(self, ast=None, source_ = None):
        if(ast == None and len(source_) > 0):
            compiled = solc.compile_source(source_)
            self.ast = compiled[compiled.keys()[0]]['ast']
        else:
            self.ast = ast
        self.source = source_
        self.tmp = []
        self.owner = {}
        self.constructor_list = []
        self.function_list = []
        self.modifier_list = []
        self.ifstatements = []
        self.get_global_variables()
        self.get_function_list(self.ast)
        self.get_modifier_list(self.ast)
        for i in self.function_list+self.modifier_list:
            self.search_only_owner_check(i)

    def get_global_variables(self):
        self.global_variables = contract_global_variable_list(self.ast)

    def get_function_list(self, ast):
        if ast['name'] == 'FunctionDefinition':
            if ast['attributes']['isConstructor']:
                self.constructor_list.append(ast)
            else:
                self.function_list.append(ast)
        try:
            if len(ast['children']) > 0:
                for i in ast['children']:
                    self.get_function_list(i)
        except Exception as e:
            pass
    def get_modifier_list(self, ast):
        if ast['name'] == 'ModifierDefinition':
            self.modifier_list.append(ast)
        try:
            if len(ast['children']) > 0:
                for i in ast['children']:
                    self.get_modifier_list(i)
        except Exception as e:
            pass

    def get_ifstatment_list(self, function_list):
        print 'get_ifstatment_list called!'


    def search_only_owner_check(self, ast):

        if ast['name'] == 'FunctionCall' :
            try:
                children = ast['children']
                value = children[0]['attributes']['value']
                if value == 'require' or value == 'assert':
                    try:
                        if children[1]['name'] == 'BinaryOperation' and children[1]['attributes']['operator'] == '==':
                            children2 = children[1]['children']
                            for i in range(len(children2)):
                                    if children2[i]['name'] == 'Identifier':
                                        try:
                                            refer_id = children2[i]['attributes']['referencedDeclaration']
                                            self.owner[refer_id] = self.global_variables[refer_id]
                                            print ast['src']
                                        except:
                                            #print 'no refer'
                                            pass
                    except Exception as e:
                        #print 'search_only_owner_check error N02 ',e
                        pass

            except Exception as e:
                #print 'search_only_owner_check error N01 ',e
                pass
        try:
            if len(ast['children']) > 0:
                for i in ast['children']:
                    self.search_only_owner_check(i)
        except Exception as e:
            #print 'search_only_owner_check error N00',e
            #error_source(self.source, ast)
            pass

def error_source(source, ast):
    if(source != None):
        #l = ast['src'].split(':')
        #f = int(l[0])
        #s = int(l[1])
        #t = int(l[2])
        print ast

        #print source[f:f+s:t]

def contract_global_variable_list(ast):

    result = {}

    tmp = ast['children']
    for i in range(len(tmp)):
        if tmp[i]['name'] == 'ContractDefinition':
            tmp2 = tmp[i]['children']
            for j in range(len(tmp2)):
                if tmp2[j]['name'] == "VariableDeclaration":
                    result[tmp2[j]['id']] = tmp2[j]['attributes']
    
    return result

#def (ast):

def access_check(ast):

    tmp = contract_global_variable_list(ast)

    for i in tmp:
        print i

def vuln_check(source):
    compiled = solc.compile_source(source)
    ast = compiled[compiled.keys()[0]]['ast']

    access_check(ast)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--address", help = "Contract address")
    parser.add_argument("-f", "--file", help = "File Name")

    args = parser.parse_args()

    if args.address:
        print 'args.address'
    elif args.file:
        f = open(args.file, "r")
        tmp = f.read(1024)
        data = ''
        while tmp:
            data += tmp
            tmp = f.read(1024)
        vuln_check(data)
    else:
        print parser.print_help()


if __name__ == "__main__":
    main()

a = solc.compile_source(open("./test.sol", "r").read(1000000))['<stdin>:Owned']['ast']
b = tree(a)
