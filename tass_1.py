from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = ChromeOptions()
# options.add_argument('--headless')
driver = Chrome(options=options)

data = []

#  Для всех статей - сбор ссылок и названия
driver.get("https://tass.ru/ekonomika")

# Wait for the titles and links to become available
wait = WebDriverWait(driver, 10)
button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'ds_ext_button-4gOSC') and contains(@class, 'ds_ext_button--secondary-wd4YM') and contains(@class, 'ds_ext_button--large-3Q9j1') and contains(@class, 'ds_ext_button--stretch-F6Pzo') and contains(text(), 'Загрузить больше результатов')]")))
button.click()

cur_len = 0
prev_len = 1

while prev_len != cur_len:
    titles = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "tass_pkg_title_wrapper-i0jgn")))
    titles_arr = [title.text for title in titles]
    links = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "tass_pkg_link-v5WdK")))
    links_arr = [link.get_attribute("href") for link in links]
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    prev_len = cur_len
    cur_len = len(titles_arr)

print(len(titles_arr))
print(len(links_arr))
print(titles_arr)
print(links_arr)


for title, link in zip(titles_arr, links_arr):
    under_data = []

    under_data.append(title)
    under_data.append(link)

    # Для каждой статьи - сбор подзаголовка, текста, даты публикации и тегов
    driver.get(link)

    date = driver.find_element(By.CLASS_NAME, "ds_ext_marker-kFsBk").text
    under_data.append(date)

    lead = driver.find_element(By.CLASS_NAME, "NewsHeader_lead__6Z9If").text
    under_data.append(lead)

    paragraphs = driver.find_elements(By.CLASS_NAME, "Paragraph_paragraph__nYCys")
    paragraphs_arr = [paragraph.text for paragraph in paragraphs]
    under_data.append(paragraphs_arr)

    tags = driver.find_elements(By.CLASS_NAME, "Tags_tag__tRSPs")
    tags_arr = [tag.text for tag in tags]
    under_data.append(tags_arr)

    data.append(under_data)
    print(under_data)

print(data)