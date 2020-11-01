from celery import Celery
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from collections import Counter
import pandas as pd
import time

def driver_setup():
    PATH_CHD = r'.\chromedriver.exe'
    options = Options()
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    driver = webdriver.Chrome(options=options, executable_path=PATH_CHD)
    return driver

def count_pages(driver, phrase):
    pages = 0
    driver.get('https://www.pracuj.pl/praca/' + phrase + ending_to_phrase)
    elems = driver.find_elements_by_xpath("//a[@class]")
    for elem in elems:
        link = elem.get_attribute("class")
        if 'pagination_trigger' in link:
            pages += 1
    # if only one site page
    if pages == 0:
        pages = 1
    return pages

def get_jobs_links(driver, pages_count, phrase):
    jobs = []
    pages = ['&pn=' + str(number) for number in range(0,20)]
    for page_number in range(1, pages_count + 1):
        time.sleep(2)
        if page_number == 1:
            driver.get('https://www.pracuj.pl/praca/' + phrase + ending_to_phrase)
        elif page_number > 1:
            driver.get('https://www.pracuj.pl/praca/' + phrase + ending_to_phrase + pages[page_number])

        elems = driver.find_elements_by_xpath("//a[@href]")

        for elem in elems:
            link = elem.get_attribute("href")
            if 'oferta' in link:
                if not link in jobs:
                    jobs.append(link)
    return jobs

def get_contet_from_job_post(driver, jobs, phrase):
    content = []
    counter = 0
    for job in jobs:
        counter += 1
        print( f'{counter} job out of {len(jobs)} for {phrase}.')
        time.sleep(1)
        driver.get(job)
        lis = driver.find_elements_by_xpath("//div[@id='description']//ul//li")
        for li in lis:
            content.append(li.text)
    return content

def count_words(data, phrase):
    file_name = phrase + '-words.csv'
    c = Counter(" ".join(data).split(" "))
    list_of_keys = [x[0].lower() for x in [keys for keys in dict(c).items()]]
    list_of_values = [x[1] for x in [keys for keys in dict(c).items()]]
    df = pd.DataFrame.from_dict({'words':list_of_keys, 'count':list_of_values})
    df = df.sort_values(by=['count'], ascending=False)
    df.to_csv(file_name, encoding='utf-8', index=False)

def save_content(data, phrase):
    file_name = phrase + '-content.csv'
    df = pd.DataFrame(data, columns=['Data'])
    df.to_csv(file_name, encoding='utf-8', index=False)


def main(search_phrase):

    global ending_to_phrase
    ending_to_phrase = ';kw?rd=30'

    driver = driver_setup()
    pages_count = count_pages(driver, search_phrase)
    job_offers = get_jobs_links(driver, pages_count, search_phrase)
    job_content = get_contet_from_job_post(driver, job_offers, search_phrase)
    driver.quit()
    save_content(job_content, search_phrase)
    count_words(job_content, search_phrase)

if __name__ == "__main__":
    main()
