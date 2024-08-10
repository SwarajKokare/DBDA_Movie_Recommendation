import csv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def read_csv_to_list(file_path):
    data_list = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            data_list.append(row)
    return data_list


def write_list_to_csv(file_path, data_list):
    with open(file_path, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(data_list)


def scrape_movie_details(driver):
    movie_data = []
    try:
        title_path = driver.find_element(By.XPATH,
                                         "/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/h1/span")
        title = title_path.text
        movie_data.append(title)
        #
        release_year_element = driver.find_element(By.XPATH,
                                                   "/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[1]/a")
        release_year = release_year_element.text
        movie_data.append(release_year)
        #
        genre = []
        genre_1 = driver.find_element(By.XPATH,
                                      "/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[1]/div[2]/a[1]")
        genre.append(genre_1.text)
        try:
            genre_2 = driver.find_element(By.XPATH,
                                          "/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[1]/div[2]/a[2]")
        except NoSuchElementException:
            movie_data.append(genre)
        else:
            genre.append(genre_2.text)
            try:
                genre_3 = driver.find_element(By.XPATH,
                                              "/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[1]/div[2]/a[3]")
            except NoSuchElementException:
                movie_data.append(genre)
            else:
                genre.append(genre_3.text)
                movie_data.append(genre)

        duration_element = driver.find_element(By.XPATH,
                                               "/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[3]")
        duration = duration_element.text
        movie_data.append(duration)

        imdb_rating_element = driver.find_element(By.XPATH,
                                                  "/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[2]/div/div[1]/a/span/div/div[2]/div[1]/span[1]")
        imdb_rating = float(imdb_rating_element.text)
        movie_data.append(imdb_rating)

        viewership_element = driver.find_element(By.XPATH,
                                                 "/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[2]/a")
        viewership = viewership_element.text
        movie_data.append(viewership)

        try:
            user_votes_element = driver.find_element(By.XPATH,
                                                     "/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[2]/div/div[1]/a/span/div/div[2]/div[3]")
        except NoSuchElementException:
            user_votes_element = 'NA'
        user_votes = user_votes_element.text
        movie_data.append(user_votes)

        synopsis_element1 = driver.find_element(By.XPATH,
                                                "/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/p/span[1]")
        synopsis1 = synopsis_element1.text
        movie_data.append(synopsis1)

        synopsis_element2 = driver.find_element(By.XPATH,
                                                "/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/p/span[2]")
        synopsis2 = synopsis_element2.text
        movie_data.append(synopsis2)

        synopsis_element3 = driver.find_element(By.XPATH,
                                                "/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/p/span[3]")
        synopsis3 = synopsis_element3.text
        movie_data.append(synopsis3)

        director_element = driver.find_element(By.XPATH,
                                               "/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[2]/div/ul/li[1]/div/ul/li/a")
        director = director_element.text
        movie_data.append(director)

        stars = []
        try:
            star_1 = driver.find_element(By.CSS_SELECTOR, "#__next > main > div > section.ipc-page-background.ipc-page"
                                                          "-background--base.sc-c41b9732-0.NeSef > section > "
                                                          "div:nth-child(5) > section > section > "
                                                          "div.sc-92625f35-4.iDcoFI > div.sc-92625f35-6.gHKhNg > "
                                                          "div.sc-92625f35-10.dwKwMe > section > div.sc-b7c53eda-3.vXcqY "
                                                          "> div > ul > "
                                                          "li.ipc-metadata-list__item.ipc-metadata-list-item--link > div "
                                                          "> ul > li:nth-child(1) > a")
            stars.append(star_1.text)
            star_2 = driver.find_element(By.CSS_SELECTOR, "#__next > main > div > section.ipc-page-background.ipc-page"
                                                          "-background--base.sc-c41b9732-0.NeSef > section > "
                                                          "div:nth-child(5) > section > section > "
                                                          "div.sc-92625f35-4.iDcoFI > div.sc-92625f35-6.gHKhNg > "
                                                          "div.sc-92625f35-10.dwKwMe > section > div.sc-b7c53eda-3.vXcqY "
                                                          "> div > ul > "
                                                          "li.ipc-metadata-list__item.ipc-metadata-list-item--link > div "
                                                          "> ul > li:nth-child(2) > a")
            stars.append(star_2.text)
            star_3 = driver.find_element(By.CSS_SELECTOR,
                                         "#__next > main > div > section.ipc-page-background.ipc-page"
                                         "-background--base.sc-c41b9732-0.NeSef > section > "
                                         "div:nth-child(5) > section > section > "
                                         "div.sc-92625f35-4.iDcoFI > div.sc-92625f35-6.gHKhNg > "
                                         "div.sc-92625f35-10.dwKwMe > section > div.sc-b7c53eda-3.vXcqY "
                                         "> div > ul > "
                                         "li.ipc-metadata-list__item.ipc-metadata-list-item--link > div "
                                         "> ul > li:nth-child(3) > a")
            stars.append(star_3.text)
            movie_data.append(stars)
        except NoSuchElementException:
            movie_data.append(stars)
            link_to_click = driver.find_element(By.XPATH, "/html/body/div[2]/main/div/section[1]/section/div["
                                                          "3]/section/section/div[3]/div[1]/div[1]/div/a")
            link_to_click.click()

            # Wait for the image to load
            time.sleep(2)  # You may adjust the sleep time as needed

            # Fetch the image link
            image_element = driver.find_element(By.XPATH, "//*[@id='__next']/main/div[2]/div[3]/div[5]/img")
            image_link = image_element.get_attribute("src")
            movie_data.append(image_link)
        else:
            link_to_click = driver.find_element(By.XPATH, "/html/body/div[2]/main/div/section[1]/section/div["
                                                          "3]/section/section/div[3]/div[1]/div[1]/div/a")
            link_to_click.click()

            # Wait for the image to load
            time.sleep(2)  # You may adjust the sleep time as needed

            # Fetch the image link
            image_element = driver.find_element(By.XPATH, "//*[@id='__next']/main/div[2]/div[3]/div[5]/img")
            image_link = image_element.get_attribute("src")
            movie_data.append(image_link)
        return movie_data

    except NoSuchElementException:
        print("Link or image not found")
        # return movie_data
        return movie_data


chrome_driver_path = "C:\\Users\\sbmal\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
service = Service(chrome_driver_path)
chrome_options = Options()
driver = webdriver.Chrome(service=service, options=chrome_options)

csv_filename = "./modified_links.csv"
link_list = []
with open(csv_filename, mode='r', newline='') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        link = row[0]
        link_list.append(link)

link_list_mod = link_list[1001:1005]   ## CHANGE BATCH HERE

with open("Batch_x.csv", 'a', newline='') as file:  # CHANGE CSV FILE NAME AS BATCH NO
    for i in range(len(link_list_mod)):
        link = link_list_mod[i]
        driver.get(link)
        data = scrape_movie_details(driver)
        writer = csv.writer(file)
        if data:
            writer.writerow(data)

driver.quit()