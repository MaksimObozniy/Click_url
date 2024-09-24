import requests
from environs import Env
from urllib.parse import urlparse


def is_shortened_link(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc == "vk.cc"  


def shorten_link(token, long_url):
    api_url = "https://api.vk.com/method/utils.getShortLink"
    params = {
        "access_token": token,
        "url": long_url,
        "v": "5.131",
    }
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        response_data = response.json()
        return response_data["response"]["short_url"]
    except requests.exceptions.RequestException:
        print("Ошибка при подключении к API или неверный запрос.")
        return None
    except KeyError:
        print("Ошибка: неожиданный формат ответа API.")
        return None


def count_clicks(token, short_link):
    api_url = "https://api.vk.com/method/utils.getLinkStats"
    params = {
        "access_token": token,
        "key": short_link.split('/')[-1],
        "v": "5.131",
        "interval": "forever"
    }
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        response_data = response.json()
        return response_data["response"]["stats"][0]["views"]
    except requests.exceptions.RequestException:
        print("Ошибка при подключении к API или неверный запрос.")
        return None
    except KeyError:
        print("Ошибка: неожиданный формат ответа API.")
        return None


def main():
    env = Env()
    env.read_env()
    
    token = env.str("VK_API_KEY")
    user_input = input("Введите ссылку: ")

    if is_shortened_link(user_input):
        clicks_count = count_clicks(token, user_input)
        if clicks_count is not None:
            print(f"Количество кликов по ссылке: {clicks_count}")
    else:
        short_link = shorten_link(token, user_input)
        if short_link:
            print(f"Сокращенная ссылка: {short_link}")
        else:
            print("Не удалось сократить ссылку.")


if __name__ == "__main__":
    main()
    
