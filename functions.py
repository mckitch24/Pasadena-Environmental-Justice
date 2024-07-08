import censusgeocode as cg

def address_to_tract(address):
    result = cg.address(address, city='Pasadena', state='CA', returntype = 'geographies')
    tract = result[0]['geographies']['Census Tracts'][0]['GEOID']
    return tract