import bbatch
from pprint import pprint as pp

def get_data(get_json_bool=False):
    '''
    just calls bbatch.py functions to get the data, which you will need to run bbatch.py at
    least once to create.
    '''
    data = bbatch.get_data_dict(
        empty=False, data_is_json=get_json_bool
    )
    return data


def look_for_file_type(dataset, key, value, contains=True):
    '''
    key: 'abspath', 'charset', or 'mime'
    value: what you're looking for in the dataset.
    contains defaults to True and checks if string inside of the string
    set to False will do the opposite
    '''
    rt_ls = []
    for fn in dataset.keys():
        if contains:
            if value in dataset[fn][key]:
                entry = {
                    'name': fn, 
                    'param': key,
                    'value': value
                }
                rt_ls.append(entry)
        else:
            if value not in dataset[fn][key]:
                entry = {
                    'name': fn, 
                    'param': key,
                    'value': dataset[fn][key]
                }
                rt_ls.append(entry)
    return rt_ls

def get_all_mime_types(dataset, key):
    '''
    Finds the occurences of different mime and charset values found in the files in your dataset
    '''
    assert key == 'mime' or key == 'charset' or key == 'abspath'
    occuring_values = set()
    for fn in dataset.keys():
        value = dataset[fn][key]
        if value not in occuring_values:
            occuring_values.add(value)
    return occuring_values
    
            
data = get_data()
htmls = look_for_file_type(data, 'mime', 'html')
notbin = look_for_file_type(data, 'charset', 'binary', contains=False)

mimes_found = get_all_mime_types(data, 'mime')
charsets_found = get_all_mime_types(data, 'charset')

pp(htmls)
pp(notbin)

pp(mimes_found)
pp(charsets_found)
