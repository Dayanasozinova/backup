from os import path
import requests
from pprint import pprint
import json
import time
from tqdm import tqdm

class API_VK:
  def __init__(self,file_vk):
    with open(file_vk, 'r') as f:
      token = f.read().strip()
    self.token = token

  def get_id(self):

    question = input('Вы будете делать запрос через id или username? ')
    
    if question == 'id':
      get_id = input('Введите id пользователя: ')
      self.get_photos(get_id)

    elif question == 'username':
      get_username = input('Введите username пользователя: ')
      id = str(self.get_user_id(get_username))
      self.get_photos(id)

    else: 
      print('!!!Ошибка!!!\nОтвет некоректен.\nЗапустите код снова.')
  

  def get_user_id(self,user_name):
    URL = 'https://api.vk.com/method/users.get'
    params = {
      'user_ids': user_name,
      'v':'5.131', 
      'access_token': self.token}
    res_1 = requests.get(URL, params=params)
    res_1 = res_1.json()
    return res_1['response'][0]['id']


  def get_photos(self,id):
    URL = 'https://api.vk.com/method/photos.get'
    params = {
      'owner_id': id,                  #552934290
      'album_id': 'profile',
      'extended': '1', 
      'photo_sizes': '1', 
      'v':'5.131', 
      'access_token': self.token}
    res = requests.get(URL, params=params)
    res_json = res.json()

    data_list =[]
    name_list = []
    for item in res_json['response']['items']:        
      data_dict = {}        
      size_list = []
    
      for size in item['sizes']:            
        p = size['height']*size['width']
        size_list.append(p)
            
      max_size = max(size_list)

      index = int(size_list.index(max_size))
      
      
      if str(item['likes']['count'])  in name_list:
        data_dict['file_name'] = str(item['likes']['count'] + item['date']) + '.jpg'
        data_dict['path'] = item['sizes'][index]['url']
        data_dict['size'] = item['sizes'][index]['type']
        name_list.append(str(item['likes']['count']) + str(item['date']))
        data_list.append(data_dict)
      else:
        data_dict['file_name'] = str(item['likes']['count']) + '.jpg'
        data_dict['path'] = item['sizes'][index]['url']
        data_dict['size'] = item['sizes'][index]['type']
        name_list.append(str(item['likes']['count']))
        data_list.append(data_dict)

      with open("data_file.json", "w") as write_file:
            json.dump(data_list, write_file)
      
    return data_list


class YaUploader:
  def __init__(self, file_ya):
    with open(file_ya, 'r') as f:
      token_ya = f.read().strip()
    self.token = token_ya

  def create_date(self, date):
    url_1 = "https://cloud-api.yandex.net/v1/disk/resources/"
    headers_1 = { "Accept": "application/json", "Authorization": "OAuth " + self.token}
    params_1 = {'path': date}
    r_1 = requests.put(url=url_1, params=params_1, headers=headers_1)
    # res_1 = r_1.json()
    # pprint(json.dumps(res_1, sort_keys=True, indent=4, ensure_ascii=False))

  def upload (self, path, url):
    headers = {"Accept": "application/json", "Authorization": "OAuth " + self.token}        
    params = {'path': str(path), 'url': str(url)}        
    url = "https://cloud-api.yandex.net/v1/disk/resources/upload/"
    r = requests.post(url=url, params=params, headers=headers)
    # res = r.json()
    # pprint(json.dumps(res, sort_keys=True, indent=4, ensure_ascii=False))

def programm():
  file_vk = str(input('Введите файл, в котором храниться токен VK: '))
  
  login = API_VK(file_vk)    
  id = login.get_id()            
  get_photos = login.get_photos(id)
    
  file_ya = str(input('Введите файл, в котором храниться токен Yandex Disk: ')) 
  
  uploader = YaUploader(file_ya)

  date = str(input('Введите название папки, в которой будут храниться фотографии из VK: '))
  uploader.create_date(date)

  count = int(input('Сколько фотографий загрузить: '))

  i = 0
  if len(get_photos) < count:
    print('У данного аккаунта меньше фотографий. Запустите код снова.')
    
  else:
    for path in get_photos:
      for i in tqdm(range(1)):
        time.sleep(1)
      i += 1  
      name = path['file_name']
      url = path['path']
      path_to_file = f'/{date}/{name}'
      uploader.upload(path_to_file, url)
    print("Фотографии загружены.")
    
    
if __name__ == '__main__':
  programm()
  