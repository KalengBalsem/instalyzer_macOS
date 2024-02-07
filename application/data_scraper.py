import requests             # to scrape data
import random, time, json   # to scrape data politely

header_list = [
        {
            'User-Agent': 'Mozilla/5.0 (Android; Mobile; rv:40.0)',
            'X-Asbd-Id': '129477',
            'X-Ig-Www-Claim': '0',
            'X-Ig-App-Id': '936619743392459',
            'X-Requested-With': 'XMLHttpRequest'
        },

        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'X-Asbd-Id': '129477',
            'X-Ig-Www-Claim': '0',
            'X-Ig-App-Id': '936619743392459',
            'X-Requested-With': 'XMLHttpRequest'
        },

        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            'X-Asbd-Id': '129477',
            'X-Ig-Www-Claim': '0',
            'X-Ig-App-Id': '936619743392459',
            'X-Requested-With': 'XMLHttpRequest'
        },

        {
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 5.0; Trident/5.0)',
            'X-Asbd-Id': '129477',
            'X-Ig-Www-Claim': '0',
            'X-Ig-App-Id': '936619743392459',
            'X-Requested-With': 'XMLHttpRequest'
        },

        {
            'User-Agent': 'Mozilla/5.0 (Windows 98; Win 9x 4.90) AppleWebKit/534.2 (KHTML, like Gecko) Chrome/21.0.849.0 Safari/534.2',
            'X-Asbd-Id': '129477',
            'X-Ig-Www-Claim': '0',
            'X-Ig-App-Id': '936619743392459',
            'X-Requested-With': 'XMLHttpRequest'
        }
    ]

def scrape_data(username):
    # add delay
    time.sleep(random.uniform(7, 11))
    ####
    
    profile_url = f'https://www.instagram.com/api/v1/users/web_profile_info/?username={username}'

    scraping_success = False
    try:
        response = requests.get(profile_url, headers=random.choice(header_list), timeout=10)
        with open(f'scraper/scraped_data/{username}0.json', 'w') as file:
            data = response.json()   # it will raise an error here if the response is not in json
            json.dump(data, file)
        print('Data scraped successfully.')
        scraping_success = True 
    except:
        print('Failed to scrape the data.')
    return scraping_success

def scrape_more(username, iteration):   # MAXIMUM iteration without proxy = 3 (to avoid burdening the website)
    more_scraping_success = False
    for i in range(iteration):
        try:
            with open(f'scraper/scraped_data/{username}{i}.json', 'r') as file:
                profile_response = json.load(file)
            # get user id the first iteration
            if i == 0: 
                user_id = profile_response['data']['user']['id'] # defining user_id once.
            
            # defining end cursor to follow through
            end_cursor = profile_response['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor'][:-2]  # [:-2] is to remove "==" at the end of end_cursor 
            if end_cursor:
                # keeps following the end_cursor using unique IG URL (last updated: Jan 2024)
                post_url = f'''
                        https://www.instagram.com/graphql/query/?doc_id=17991233890457762&variables=%7B%22id%22%3A%22{user_id}%22%2C%22after%22%3A%22{end_cursor}%3D%3D%22%2C%22first%22%3A12%7D
                '''
                # add delay
                time.sleep(random.uniform(7, 11))
                ####  

                response = requests.get(post_url, headers=random.choice(header_list), timeout=20)
                data = response.json()

                # store JSON data in file
                with open(f'scraper/scraped_data/{username}{i+1}.json', 'w') as file:
                    json.dump(data, file)

                print(f'{username}\'s iteration {i+1} data scraped successfuly!')
                more_scraping_success = True
            else:
                return more_scraping_success
        except:
            print(f'{username}\'s iteration {i+1} iteration data failed')
    return more_scraping_success
