from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from main import VideoStream

class DownloaderApp(BoxLayout):
    def __init__(self, **kwargs):
        super(DownloaderApp, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Espacio vacio 1
        fill_space1 = BoxLayout(size_hint_y=None, height=40)
        self.add_widget(fill_space1)

        # Primera fila
        self.first_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        label1 = Label(text='URL:')
        text_box1 = TextInput(multiline=False, text = 'https://www.youtube.com/watch?v=A2LEaF1jCeA')
        button1 = Button(text='Preview')
        button1.bind(on_press=self.visualize)
        self.first_row.add_widget(label1)
        self.first_row.add_widget(text_box1)
        self.first_row.add_widget(button1)
        self.add_widget(self.first_row)

        # Segunda fila
        preview_image = Image(source='preview_image.jpg')  # Reemplaza 'ruta_de_tu_imagen.jpg' con la ruta de tu preview_image
        self.add_widget(preview_image)

        # Tercera fila
        self.third_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        button2 = Button(text='Advanced')
        button2.bind(on_press=self.togle_advanced)
        self.third_row.add_widget(button2)

        label2 = Label(text='itag:', opacity=0)
        self.third_row.add_widget(label2)
        
        text_box2 = TextInput(multiline=False, opacity=0)
        self.third_row.add_widget(text_box2)

        button3 = Button(text='Download')
        self.third_row.add_widget(button3)

        self.add_widget(self.third_row)

        # Cuarta fila
        self.fourth_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=190)
        text_box3 = TextInput(multiline=True, text='D\nE\nF', readonly=True, opacity=0)
        text_box4 = TextInput(multiline=True, text='A\nB\nC', readonly=True, opacity=0)
        self.fourth_row.add_widget(text_box4)
        self.fourth_row.add_widget(text_box3)

        self.add_widget(self.fourth_row)

    def togle_advanced(self, instance):
        if self.fourth_row.children[0].opacity == 0:

            # self.third_row.children[0].opacity = 1
            self.third_row.children[1].opacity = 1
            self.third_row.children[1].text = ''
            self.third_row.children[1].readonly = False
            self.third_row.children[2].opacity = 1

            self.fourth_row.children[0].opacity = 1
            self.fourth_row.children[1].opacity = 1
        
        else: 
            # self.third_row.children[0].opacity = 0
            self.third_row.children[1].opacity = 0
            self.third_row.children[1].text = ''
            self.third_row.children[1].readonly = True
            self.third_row.children[2].opacity = 0

            self.fourth_row.children[0].opacity = 0
            self.fourth_row.children[1].opacity = 0

    def visualize(self, instance):
        url = self.first_row.children[1].text
        video = VideoStream(url)
        self.children[2].source = 'thumbnail.jpg'
        self.fourth_row.children[0].text = str(video.videos_frame)
        self.fourth_row.children[1].text = str(video.audios_frame)


class MyApp(App):
    def build(self):
        return DownloaderApp()
    

if __name__ == '__main__':
    MyApp().run()