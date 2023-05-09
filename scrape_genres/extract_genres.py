from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from tqdm.auto import tqdm

import time

def pull_from_movielens(path_target_words: str, your_login: str, your_password, verbose: bool = False):
    
    LOGIN_PAGE = "https://movielens.org/login" # the loging page
    ACCOUNT = your_login # add here your login
    PASSWORD = your_password # add here your password
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    actions = ActionChains(driver)

    wait = WebDriverWait(driver, 1)
    driver.get(LOGIN_PAGE)
    wait.until(EC.element_to_be_clickable((By.XPATH, 
    '//*[@id="root"]/ui-view/ng-component/div/ui-view/auth-template/div/div[2]/ui-view/login-page/div/form/div[1]/label/input'))).send_keys(ACCOUNT)
    wait.until(EC.element_to_be_clickable((By.XPATH, 
    '//*[@id="root"]/ui-view/ng-component/div/ui-view/auth-template/div/div[2]/ui-view/login-page/div/form/div[2]/label/input'))).send_keys(PASSWORD)
    wait.until(EC.element_to_be_clickable((By.XPATH, 
    '//*[@id="root"]/ui-view/ng-component/div/ui-view/auth-template/div/div[2]/ui-view/login-page/div/form/div[3]/button'))).click()

    movie_genres = list()
    not_found = list()
    
    with open(r'C:\Coding_Projects\MovieLens_dataset\scrape_genres\no_info_ids.txt', mode='r', encoding='utf-8') as f:
        movie_ids = f.readlines()
        movie_ids = movie_ids[0].split(',')
        movie_ids = [int(i) for i in movie_ids[:-1]]

    for w in tqdm(movie_ids):             
        try:
            driver.get(f"https://movielens.org/movies/{w}") # get the page with the movie
            driver.implicitly_wait(1)
            out_text = driver.find_element(By.XPATH, 
            '/html/body/ui-view/ng-component/div/ui-view/ng-component/ui-view/ng-component/div[2]/div/ui-view/movie-page/div/div[1]').text 
            # print(out_text)
            temp_str = str(w) + '|'+ out_text
            movie_genres.append(temp_str)
        except:
            print('\nMISSED\n')
            not_found.append(w)

    with open(r'C:\Coding_Projects\MovieLens_dataset\scrape_genres\pulled_texts_new.txt', mode='w', encoding='utf-8') as f2:
        for i in movie_genres:
            f2.write(i+'\n')
    print(not_found)
    driver.close() 
    
    pass

# https://10minutemail.net/
# ehl10126@nezid.com
# qwerty42
# Admin42

pull_from_movielens(
    r'C:\Coding_Projects\MovieLens_dataset\scrape_genres\no_info_ids.txt', 
    'qwerty42',
    'Admin42')
