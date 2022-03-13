import requests
import os
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By

class DataExtractor:

    def __init__(self, path: str, url: str):
        service = Service(executable_path=path)
        self.url = url 
        self.browser = Firefox(service=service)
        self.links = []


    def extract_links(self) -> int:
        self.browser.get(self.url)
        elements = self.browser.find_elements(By.XPATH, '/html/body/div[3]/div/*')

        for element in elements:
            link = element.find_element(By.TAG_NAME, 'a').get_attribute('href')
            self.links.append(link)

        return len(self.links)

    
    def get_profile_data(self, index: int) -> list:
        link = self.links[index]
        self.browser.get(link)
        name = self.browser.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/h4').text
        subject = self.browser.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/h6[1]').text
        area = self.browser.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/ul[1]').text
        area = area.split('\n')
        area[0] = area[0].split(',')[0]
        area = ", ".join(area)
        education = self.browser.find_element(By.XPATH, '/html/body/div[3]/div/div[1]/table/tbody').text
        education = education.split('\n')
        education.remove('Education')
        education[0] = education[0].split('from')[0]
        education = ", ".join(education[:2])
        image_link = self.browser.find_element(By.CLASS_NAME, 'faculty-img').get_attribute('src')
        file_name = name.lower().replace(' ', '_') + '.png'
        image = self.download_image(image_link, file_name)
        return [name, subject, area, education, image]


    
    @staticmethod
    def download_image(link, filename) -> str:
        res = requests.get(link)
        path = os.path.join(os.getcwd(), 'images', filename)
        file = open(path, 'wb')
        file.write(res.content)
        file.close()
        return path

        

    


