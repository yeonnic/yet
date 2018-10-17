import re, requests

def get_address(data):
    tmp = data
    list = []
    while(True):
        p = tmp.find('/address/0x')


        if(p == -1):
            break

        p += len('/address/')

        list.append(tmp[p:p+42])
        tmp = tmp[p+42:]
    return list

def verified_contract_list(page=1):
    url = 'http://etherscan.io/contractsVerified/%d?ps=100' %(page)

    response = requests.get(url)

    data = str(response.content)
    data = data[data.find('table table-hover '):]
    data = data[:data.find('</tbody>')]

    address_list = get_address(data)

    return address_list
