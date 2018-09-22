'''
Data structures storing info for app. For C4G hackathon. Parts borrowed from
code for Air Spares

@author: grandpaa
'''

import simplejson as json

class DTO:
    keywords = []
    
    def __init__(self, entry_dict: dict = {}):
        for key in self.keywords:
            setattr(self, key, entry_dict[key] 
                               if key in entry_dict.keys() else None)
    
    def __getitem__(self, key):
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        setattr(self, key, value)
        
    def __repr__(self):
#         raw_attr = [key + ': ' + str(getattr(self, key)) 
#                     for key in self.keywords]
#         out = '{' + ', '.join(raw_attr) + '}'
        
        return str(self.__dict__)
        
class User(DTO):
    keywords = ['first_name', 'last_name', 'data']

class UserData(DTO):
    keywords = ['address', 'job', 'age', 'phone', 'history', 'race', 'income']
    
class Item(DTO):
    keywords = ['value', 'description', 'date_added']

class Address(DTO):
    keywords = ['city', 'state', 'street', 'zip']
    
def json_to_user(json_file: object) -> User:
    json_dict = json.load(json_file)
    user = User(json_dict)
    user['data'] = UserData(user['data'])
    user['data']['history'] = [Item(user['data']['history'][i]) 
                               for i in range(len(user['data']['history']))]
    user['data']['address'] = Address(user['data']['address'])
    
    return user

def test():
    json_path = 'joe.json'
    with open(json_path) as json_obj:
        user = json_to_user(json_obj)
    print('done!')

if __name__ == '__main__':
    test()

    








