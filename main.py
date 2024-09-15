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
    
    response = requests.get(api_url, params=params)
    response.raise_for_status()  
    
    data = response.json()
    
    if "error" in data:
        return None
        
    return data.get("response", {}).get("short_url")


def count_clicks(token, short_link):
    parsed_url = urlparse(short_link)
    if parsed_url.netloc != "vk.cc":
        return "Неверный домен! Ожидается ссылка с vk.cc"
    
    api_url = "https://api.vk.com/method/utils.getLinkStats"
    
    params = {
        "access_token": token,
        "key": parsed_url.path.strip('/'),
        "v": "5.131",
        "interval": "forever"
    }
    
    response = requests.get(api_url, params=params)
    
    response.raise_for_status()
    
    response_data = response.json()
    
    if "error" in response_data:
        return "Ошибка при получении статистики"
    
    return response_data.get("response", {}).get("stats", [{}])[0].get("clicks", 0)



def main():
    env = Env()
    env.read_env()

    token = env.str("VK_API_KEY")
    user_input = input("Введите ссылку: ")


    if is_shortened_link(user_input):
        try:
            clicks_count = count_clicks(token, user_input)
            if isinstance(clicks_count, str):
                print(clicks_count)
            elif clicks_count is not None:
                print(f"Количество кликов по ссылке: {clicks_count}")
            else:
                print("Не удалось получить количество кликов.")
        except requests.exceptions.HTTPError:
            print("Ошибка HTTP при запросе!")
    else:
        short_link = shorten_link(token, user_input)
        
        if short_link:
            print(f"Сокращенная ссылка: {short_link}")
        else:
            print("Не удалось сократить ссылку.")


if __name__ == "__main__":
    main()

