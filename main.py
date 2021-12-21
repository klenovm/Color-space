import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageDraw

myImage = "image0_3.jpg"
newImage = 'newImage.jpg'

def RGBtoHSL(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    cmin = min(r, g, b)
    cmax = max(r, g, b)
    delta = cmax - cmin
    l = (cmax + cmin) / 2  # яркость
    if delta == 0:
        h = 0  # оттенок
        s = 0
    else:
        s = delta / (1 - abs(2 * l - 1))  # насыщенность
        if cmax == r:
            h = ((g - b) / delta) % 6
        elif cmax == g:
            h = (b-r)/delta+2
        else:
            h =(r-g)/delta+4
        h = h * 60
    if h < 0:
        h += 360

    return h, s, l

def HSLtoRGB(h, s, l):
    c = (1-abs(2*l-1))*s
    x = c*(1-abs((h/60)%2-1))
    m = l-c/2

    if 0<=h<60:
        r, g, b = c, x, 0
    elif 60<=h<120:
        r, g, b = x, c, 0
    elif 120<=h<180:
        r, g, b = 0, c, x
    elif 180<=h<240:
        r, g, b = 0, x, c
    elif 240<=h<300:
        r, g, b = x, 0, c
    elif 300<=h<360:
        r, g, b = c, 0, x

    r, g, b = round((r + m)*255), round((g + m)*255), round((b + m)*255)
    return r, g, b

def RGBtoHSV(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    cmax = max(r, g, b)
    cmin = min(r, g, b)
    delta = cmax - cmin
    if cmax == cmin:
        h = 0
    elif cmax == r:
        h = (60*((g-b)/delta) + 360) % 360
    elif cmax == g:
        h = (60*((b-r)/delta) + 120) % 360
    elif cmax == b:
        h = (60*((r-g)/delta) + 240) % 360
    if cmax == 0:
        s = 0
    else:
        s = delta/cmax
    v = cmax

    return h, s, v

def HSVtoRGB(h, s, v):
    c = v * s
    x = c * (1 - abs((h/60)%2-1))
    m = v - c
    if 0<=h<60:
        r, g, b = c, x, 0
    elif 60<=h<120:
        r, g, b = x, c, 0
    elif 120<=h<180:
        r, g, b = 0, c, x
    elif 180<=h<240:
        r, g, b = 0, x, c
    elif 240<=h<300:
        r, g, b = x, 0, c
    elif 300<=h<360:
        r, g, b = c, 0, x

    r, g, b = round((r + m)*255), round((g + m)*255), round((b + m)*255)
    return r, g, b


class ColorSpase(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def on_click(self): #нажатие кнопки HSL
        ch = self.hField.text() #получение значения H
        ch = int(ch) #перевод str в int
        cs = self.sField.text() #получение значения S
        cs = float(cs)
        cl = self.lField.text() ##получение значения L
        cl = float(cl)
        image = Image.open(myImage)  # Открываем изображение
        draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования
        width = image.size[0]  # Определяем ширину
        height = image.size[1]  # Определяем высоту
        pix = image.load()  # Выгружаем значения пикселей

        for x in range(width): #проходим по всем пикселям и создаем новое изображение
            for y in range(height):
                r, g, b = pix[x, y][0], pix[x, y][1], pix[x, y][2]
                h, s, l = RGBtoHSL(r, g, b) #переводим из RGB в HSL
                if ch < 0:
                    ch = ch % 360
                    ch +=360
                h += ch
                s += cs
                l += cl

                h = h % 360
                if s > 1:
                    s = 1
                elif s < 0:
                    s = 0
                if l > 1:
                    l = 1
                elif l < 0:
                    l = 0
                r, g, b = HSLtoRGB(h, s, l) #переводим из HSL в RGB
                draw.point((x, y), (r, g, b)) #рисуем пиксель
        image.save(newImage, 'JPEG') #сохраняем изображение
        del draw #удаляем инструмент для рисования
        self.pixmap = QPixmap(newImage)
        self.pixmap = self.pixmap.scaledToWidth(600)
        self.pixmap = self.pixmap.scaledToHeight(330)
        self.imageLabel.setPixmap(self.pixmap)
        self.imageLabel.move(190, 20)
        self.show()

    def on_click1(self): #нажатие кнопки HSV
        ch = self.hField.text()
        ch = int(ch)
        cs = self.sField.text()
        cs = float(cs)
        cv = self.vField.text()
        cv = float(cv)
        image = Image.open(myImage)  # Открываем изображение
        draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования
        width = image.size[0]  # Определяем ширину
        height = image.size[1]  # Определяем высоту
        pix = image.load()  # Выгружаем значения пикселей

        for x in range(width): #проходим по всем пикселям
            for y in range(height):
                r, g, b = pix[x, y][0], pix[x, y][1], pix[x, y][2]
                h, s, v = RGBtoHSV(r, g, b)
                if ch < 0:
                    ch = ch % 360
                    ch +=360
                h += ch
                s += cs
                v += cv

                h = h % 360
                if s > 1:
                    s = 1
                elif s < 0:
                    s = 0
                if v > 1:
                    v = 1
                elif v < 0:
                    v = 0
                r, g, b = HSVtoRGB(h, s, v)
                draw.point((x, y), (r, g, b))

        image.save(newImage, 'JPEG')
        del draw
        self.pixmap = QPixmap(newImage)
        self.pixmap = self.pixmap.scaledToWidth(600)
        self.pixmap = self.pixmap.scaledToHeight(330)
        self.imageLabel.setPixmap(self.pixmap)
        self.imageLabel.move(190, 20)
        self.show()

    def on_click2(self):  #показать стандартное изображение
        self.pixmap = QPixmap(myImage)
        self.pixmap = self.pixmap.scaledToWidth(600)
        self.pixmap = self.pixmap.scaledToHeight(330)
        self.imageLabel.setPixmap(self.pixmap)
        self.imageLabel.move(190, 20)
        self.show()

    def initUI(self): #создание интерфейса
        global myImage
        self.resize(800, 380)
        self.setWindowTitle('Colors')

        self.qbtn = QPushButton('HSL', self) #кнопка HSL
        self.qbtn.clicked.connect(self.on_click) #соединение нажатия кнопки с функцией
        self.qbtn.move(20, 140) #перемещение кнопки
        self.qbtn1 = QPushButton('HSV', self) #кнопка HSV
        self.qbtn1.clicked.connect(self.on_click1)
        self.qbtn1.move(20, 170)
        self.st = QPushButton('Стандартное изображение', self)  # кнопка Стандрартное изображение
        self.st.clicked.connect(self.on_click2)
        self.st.move(20, 250)

        self.hl = QLabel("H", self)
        self.hl.move(20, 23)
        self.hField = QLineEdit("0", self)
        self.hField.move(40, 20)
        self.sl = QLabel("S", self)
        self.sl.move(20, 53)
        self.sField = QLineEdit("0", self)
        self.sField.move(40, 50)
        self.ll = QLabel("L", self)
        self.ll.move(20, 83)
        self.lField = QLineEdit("0", self)
        self.lField.move(40, 80)
        self.vl = QLabel("V", self)
        self.vl.move(20, 113)
        self.vField = QLineEdit("0", self)
        self.vField.move(40, 110)

        self.imageLabel = QLabel(self) #изображение
        self.pixmap = QPixmap(myImage)
        self.pixmap = self.pixmap.scaledToWidth(600)
        self.pixmap = self.pixmap.scaledToHeight(330)
        self.imageLabel.setPixmap(self.pixmap)
        self.imageLabel.move(190, 20)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ColorSpase()
    sys.exit(app.exec_())