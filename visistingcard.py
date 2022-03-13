import os
import numpy as np
import qrcode
from PIL import Image, ImageFont, ImageDraw

class VisitingCard:

    def __init__(self, name: str, subject: str, area: str, education: str, image: str):
        self.name = name
        self.subject = subject
        self.area = area
        self.education = education
        self.image_path = image
        self.email = ".".join(name.lower().split(' ')) + "@sifal.deerwalk.edu.np"
        self.file_name = name.lower().replace(' ', '_') + '.png'
        self.image = None

    
    def create(self, link: str):
        qr_path = self.create_qrcode(link)
        qr = Image.open(qr_path)
        qr = qr.resize((200, 200))
        font_path = os.path.join(os.getcwd(), 'utils', 'opensans.ttf')
        image_path = os.path.join(os.getcwd(), 'utils', 'background.png')
        font1 = ImageFont.truetype(font_path, 45)
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        draw.text((150, 30), self.name, font=font1, fill=(0, 0, 0))
        font2 = ImageFont.truetype(font_path, 18)
        draw.text((150, 100), self.email, font=font2, fill=(0, 150, 255))
        draw.text((75, 275), self.subject, font=font2, fill=(255, 255, 255))
        draw.text((75, 375), self.area, font=font2, fill=(255, 255, 255))
        draw.text((75, 470), self.education, font=font2, fill=(255, 255, 255))
        image.paste(qr, (810, 400))
        profile = Image.open(self.image_path)
        profile = profile.resize((128, 128))
        profile = self.crop_image_circle(profile)
        image.paste(profile, (10, 25), profile)
        self.image = image
        


    def save(self):
        path = os.path.join(os.getcwd(), 'cards', self.file_name)
        self.image.save(path)


    def create_qrcode(self, link: str):
        path = os.path.join(os.getcwd(), 'qrcode', self.file_name)
        image = qrcode.make(link)
        image.save(path)
        return path

    
    @staticmethod
    def crop_image_circle(image):
        npImage = np.array(image)
        h, w = image.size
    
        alpha = Image.new('L', image.size, 0)
        draw = ImageDraw.Draw(alpha)
        draw.pieslice([0, 0, h, w], 0, 360, fill=255)
        npAlpha = np.array(alpha)
        npImage = np.dstack((npImage, npAlpha))
        pfp = Image.fromarray(npImage)
        return pfp





