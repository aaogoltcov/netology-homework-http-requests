import requests


def file_translate(file_path):
    with open(file_path, encoding='utf8') as file:
        data = list(lines.strip() for lines in file)
        print(f'\nОткрыли и готовимся переводить файл: {file_path}')
    data_for_translate = {
        'text': data
    }
    target_language = 'ru'
    translate_url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    translate_parameters = {
        'key': 'trnsl.1.1.20200222T125629Z.55162f4331fe9395.0dcd326d13c274c98ef3365495e16dfe6b715fcb',
        'text': data_for_translate,
        'lang': target_language,
        'options': 1
    }
    translate_result = requests.post(translate_url, params=translate_parameters, data=data_for_translate)
    print(f'Перевели файл: {file_path}')
    file_name = (file_path.split('.')[0].upper() + '-' + target_language.upper() + '.' + file_path.split('.')[1])
    print(f'Готовимся к сохранению нового файла: {file_name}')
    with open(file_name, 'wb') as file_new:
        file_new.write(translate_result.content)
    print(f'Сохранили новый файл на локальном диске: {file_name}')
    return file_name, translate_result


def translation_to_disk(file_name, oauth_token):
    save_link = 'https://cloud-api.yandex.net:443/v1/disk/resources/upload'
    params_link = {
        'path': file_name,
        'overwrite': 'true'
    }
    headers = {
        'Accept': 'application/json',
        'Authorization': oauth_token
    }
    upload_link = (requests.get(save_link, params=params_link, headers=headers)).json()["href"]
    print(f'Запросили ссылку для сохранения переведенного на Ya диске: {file_name}')
    print(f'Ссылка для сохранения на Ya диске получена: {upload_link}')
    with open(file_name, 'r') as file:
        file = file.read()
        upload_file = requests.put(upload_link, data=file.encode('utf-8'), headers=headers)
    if upload_file.status_code == 201:
        print(f'Ох!!! Не может этого быть, но мы сохранили переведенный файл на Ya диске: {file_name}')
    else:
        print(f'Что-то пошло не так... Не удалось сохранить файл на уделенном диске: {file_name}')


def main(file_name, oauth_token):
    file_name = file_translate(file_name)
    translation_to_disk(file_name, oauth_token)
    return oauth_token


if __name__ == '__main__':
    oauth_token = 'AgAAAAAdIqkHAADLW1N-g4TL3Uh-uTPOvwIiHa8'
    # oauth_token = 'OAuth ' + input('Для будущей загрузки файла на Ya диск, введите OAuth токен (без "OAuth "): ')
    main('FR.txt', oauth_token)
    main('DE.txt', oauth_token)
    main('ES.txt', oauth_token)
