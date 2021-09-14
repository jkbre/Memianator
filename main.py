import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
from PyQt5.QtCore import Qt as qtc
import sys
import random
import requests
import praw

class RedditApi():
    def __init__(self):
        self.api_ids()
        self.source_set()
        self.meme_grapper()
    
    def api_ids(self):
        self.reddit = praw.Reddit(client_id='wLiJD2nHgMwjBdwK9Yq_kQ', \
                     client_secret='qBm_AGDozO34GJwYgRssRgX_o_cyRg', \
                     user_agent='Memianator', \
                     username='dewfdcs2', \
                     password='Scholar/Compile/Nurture3')
    
    def source_set(self):
        self.subreddit = self.reddit.subreddit('memes')

    def meme_grapper(self):
        all_subs = []

        hot = self.subreddit.hot(limit=50)

        for submission in hot:
            all_subs.append(submission)

        random_sub = random.choice(all_subs)

        self.url_title = random_sub.title
        self.url_address = random_sub.url

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.api = RedditApi()

        self.setWindowTitle('Memianator')
        self.setLayout(qtw.QVBoxLayout())
        self.keypad()

        self.show()

    def keypad(self):
        container = qtw.QWidget()
        container.setLayout(qtw.QGridLayout())

        # Meme
        image = qtg.QImage()
        image.loadFromData(requests.get(self.api.url_address).content)

        image_label = qtw.QLabel()
        pixmap = qtg.QPixmap(image)
        smaller_pixmap = pixmap.scaled(400, 400, qtc.KeepAspectRatio, qtc.SmoothTransformation)

        image_label.setPixmap(smaller_pixmap)


        # Buttons        
        btn_back = qtw.QPushButton('Back', clicked = self.back_meme)
        btn_next = qtw.QPushButton('Next', clicked = self.next_meme)
        btn_save = qtw.QPushButton('Save', clicked = self.save_meme)
        

        # Adding the buttons to the layout
        container.layout().addWidget(image_label,0,0,1,6)
        container.layout().addWidget(btn_back,1,0,1,2)
        container.layout().addWidget(btn_next,1,4,1,2)
        container.layout().addWidget(btn_save,1,2,1,2)
        self.layout().addWidget(container)

    def back_meme(self):
        pass
    def next_meme(self):
        pass
    def save_meme(self):
        pass

app = qtw.QApplication([])
mw = MainWindow()
app.setStyle(qtw.QStyleFactory.create('Fusion'))
sys.exit(app.exec_())