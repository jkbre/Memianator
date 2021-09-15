import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
from PyQt5.QtCore import Qt as qtc
import sys
import os
import requests
import praw
import shutil

class RedditApi():
    def __init__(self):
        self.dev = ''
        self.api_ids()
        self.memes_init()
    
    def api_ids(self):
        self.reddit = praw.Reddit(client_id='wLiJD2nHgMwjBdwK9Yq_kQ', \
                                  client_secret='qBm_AGDozO34GJwYgRssRgX_o_cyRg', \
                                  user_agent='Memianator', \
                                #   username='dewfdcs2', \
                                #   password='Scholar/Compile/Nurture3'\
                                  )
        if self.dev == 'on':
            print(self.reddit.read_only)
    
    def memes_init(self, rang = 'hot', num = 10):
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
            if self.dev == 'on':
                print('zatrzymało')
        elif self.sub_idx > self.limit_num-1:
            self.sub_idx = self.limit_num-1
            if self.dev == 'on':
                print('zatrzymało')
        else:
            self.url_id = self.all_subs[self.sub_idx].id
            self.url_title = self.all_subs[self.sub_idx].title
            self.url_address = self.all_subs[self.sub_idx].url
            if self.dev == 'on':
                print(self.url_address)

    def meme_saver(self):
        filename = self.url_address.split("/")[-1]
        r = requests.get(self.url_address, stream = True)
        r.raw.decode_content = True
        with open(filename,'wb') as meme:
            shutil.copyfileobj(r.raw, meme)

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.dev = 'on'

        self.api = RedditApi()
        self.setWindowTitle('Memianator')
        self.setLayout(qtw.QVBoxLayout())
        self.GUI()

        self.show()

    def GUI(self):
        container = qtw.QWidget()
        container.setLayout(qtw.QGridLayout())

        # Sub name
        self.sub_label = qtw.QPlainTextEdit(self.api.subreddit.title)
        self.sub_label.setReadOnly(True)

        # Meme Image
        self.title_label = qtw.QPlainTextEdit()
        self.title_label.setReadOnly(True)
        self.meme_label = qtw.QLabel()
        self.meme_show()

        # Counter
        self.count =  qtw.QLineEdit()
        self.count.setReadOnly(True)
        self.counter_set()


        # Buttons        
        btn_back = qtw.QPushButton('Back', clicked = self.back_meme)
        btn_next = qtw.QPushButton('Next', clicked = self.next_meme)
        btn_save = qtw.QPushButton('Save', clicked = self.api.meme_saver)
        btn_save_as = qtw.QPushButton('Save As', clicked = self.meme_as_saver)
        

        # Adding the buttons to the layout
        container.layout().addWidget(self.sub_label,0,0,1,6)
        container.layout().addWidget(self.title_label,1,0,1,5)
        container.layout().addWidget(self.count,1,5,1,1)
        container.layout().addWidget(self.meme_label,2,0,1,6)
        container.layout().addWidget(btn_back,3,0,2,2)
        container.layout().addWidget(btn_next,3,4,2,2)
        container.layout().addWidget(btn_save,3,2,1,2)
        container.layout().addWidget(btn_save_as,4,2,1,2)
        self.layout().addWidget(container)

    def meme_show(self):
        self.title_label.setPlainText(self.api.url_title)
        meme = qtg.QImage()
        meme.loadFromData(requests.get(self.api.url_address).content)
        
        pixmap = qtg.QPixmap(meme)
        if pixmap.isNull() == False:
            smaller_pixmap = pixmap.scaled(500, 500, qtc.KeepAspectRatio, qtc.SmoothTransformation)       
            self.meme_label.setPixmap(smaller_pixmap)
        else:
            if self.dev == 'on':
                print('url')
            url = '<a href="' + self.api.url_address + '">'+ self.api.url_address +'</a>'
            self.meme_label.setText(url)
            self.meme_label.setOpenExternalLinks(True)
        ## https://www.reddit.com/r/learnpython/comments/k7xk7r/failed_minimal_tag_size_sanity_pyqt5/
        
        if self.dev == 'on':
            print(self.api.url_address)

    def counter_set(self):
        number = str(self.api.sub_idx+1) + '/' + str(self.api.limit_num)
        self.count.setText(number)

    def back_meme(self):
        self.api.meme_switcher(-1)
        self.meme_show()
        self.counter_set()

    def next_meme(self):
        self.api.meme_switcher(1)
        self.meme_show()
        self.counter_set()
        
    def meme_as_saver(self):
        try:
            first_name = './' + self.api.url_address.split("/")[-1]
            r = requests.get(self.api.url_address, stream = True)
            r.raw.decode_content = True
            filename, selectedFilter = qtw.QFileDialog.getSaveFileName(self, 'Save Meme As', first_name)
            with open(filename,'wb') as meme:
                shutil.copyfileobj(r.raw, meme)
        except:
            pass

app = qtw.QApplication([])
mw = MainWindow()
app.setStyle(qtw.QStyleFactory.create('Fusion'))
sys.exit(app.exec_())