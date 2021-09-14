import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
from PyQt5.QtCore import Qt as qtc
import sys
import requests
import praw

class RedditApi():
    def __init__(self):
        self.api_ids()
        self.meme_init()
        self.dev = 'on'
    
    def api_ids(self):
        self.reddit = praw.Reddit(client_id='wLiJD2nHgMwjBdwK9Yq_kQ', \
                     client_secret='qBm_AGDozO34GJwYgRssRgX_o_cyRg', \
                     user_agent='Memianator', \
                     username='dewfdcs2', \
                     password='Scholar/Compile/Nurture3')
    
    def meme_init(self, rang = 'hot', num = 10):
        self.subreddit = self.reddit.subreddit('memes')
        self.limit_num = num
        self.all_subs = []
        self.sub_idx = 0

        if rang == 'hot':
            meme_list = self.subreddit.hot(limit=self.limit_num)

        for submission in meme_list:
            self.all_subs.append(submission)

        self.url_id = self.all_subs[self.sub_idx].id
        self.url_title = self.all_subs[self.sub_idx].title
        self.url_address = self.all_subs[self.sub_idx].url

    def meme_switcher(self, itt):
        self.sub_idx = self.sub_idx + itt
        if self.sub_idx < 0:
            self.sub_idx = 0
        elif self.sub_idx > self.limit_num-1:
            self.sub_idx = self.limit_num-1
            if self.dev == 'on':
                print('zatrzymało')
        else:
            self.url_id = self.all_subs[self.sub_idx].id
            self.url_title = self.all_subs[self.sub_idx].title
            self.url_address = self.all_subs[self.sub_idx].url

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.api = RedditApi()
        self.meme_label = qtw.QLabel()
        self.setWindowTitle('Memianator')
        self.setLayout(qtw.QVBoxLayout())
        self.keypad()

        self.show()

    def keypad(self):
        container = qtw.QWidget()
        container.setLayout(qtw.QGridLayout())

        # Meme
        meme = qtg.QImage()
        meme.loadFromData(requests.get(self.api.url_address).content)
        pixmap = qtg.QPixmap(meme)
        smaller_pixmap = pixmap.scaled(400, 400, qtc.KeepAspectRatio, qtc.SmoothTransformation)       
        self.meme_label.setPixmap(smaller_pixmap)

        # Buttons        
        btn_back = qtw.QPushButton('Back', clicked = self.back_meme)
        btn_next = qtw.QPushButton('Next', clicked = self.next_meme)
        btn_save = qtw.QPushButton('Save', clicked = self.save_meme)
        

        # Adding the buttons to the layout
        container.layout().addWidget(self.meme_label,0,0,1,6)
        container.layout().addWidget(btn_back,1,0,1,2)
        container.layout().addWidget(btn_next,1,4,1,2)
        container.layout().addWidget(btn_save,1,2,1,2)
        self.layout().addWidget(container)

    def back_meme(self):
        self.api.meme_switcher(-1)

        meme = qtg.QImage()
        meme.loadFromData(requests.get(self.api.url_address).content)

        pixmap = qtg.QPixmap(meme)
        smaller_pixmap = pixmap.scaled(400, 400, qtc.KeepAspectRatio, qtc.SmoothTransformation)
               
        self.meme_label.setPixmap(smaller_pixmap)

    def next_meme(self):
        self.api.meme_switcher(1)

        meme = qtg.QImage()
        meme.loadFromData(requests.get(self.api.url_address).content)

        pixmap = qtg.QPixmap(meme)
        smaller_pixmap = pixmap.scaled(400, 400, qtc.KeepAspectRatio, qtc.SmoothTransformation)
                
        self.meme_label.setPixmap(smaller_pixmap)
        
    def save_meme(self):
        pass

app = qtw.QApplication([])
mw = MainWindow()
app.setStyle(qtw.QStyleFactory.create('Fusion'))
sys.exit(app.exec_())