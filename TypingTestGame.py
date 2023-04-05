from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.popup import Popup
from kivy.graphics import Rectangle
from kivy.core.image import Image
from kivy.graphics import Rectangle, Color
from kivy.core.image import Image as CoreImage


import random

class TypingTest(GridLayout):
     SENTENCES = [
        "The quick brown fox jumps over the lazy dog",
        "She sells seashells by the seashore",
        "She sells seashells by the seashore",
        "I went for a run this morning.",
        "The cat is sleeping on the couch.",
        "She always drinks coffee in the morning.",
        "He loves to play video games with his friends",
        "The restaurant we went to last night had great food.",
        "I need to buy some groceries after work.",
        "The flowers in the garden are beautiful.",
        "He is going on a trip to Europe next month.",
        "I'm really tired and need to go to bed.",
        "The music playing in the background is soothing",
        "She is wearing a beautiful dress to the party.",
        "The children were playing in the park."
        "The sun rose over the horizon, casting a warm glow on the countryside.",
        "The sound of children laughing and playing filled the air, creating a cheerful atmosphere.",
        "I enjoy going for long walks in the park on sunny days.",
        "She studied hard for her exams and was rewarded with good grades.",
        "The restaurant was crowded, but we managed to find a table.",
        "He had a great sense of humor and could always make me laugh."]

    

     def __init__(self, **kwargs):
        super(TypingTest, self).__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 1)
            source = 'images/keyboard.jpg'
            image = CoreImage(source).texture
            self.bg = Rectangle(texture=image, pos=self.pos, size=self.size)
            self.bind(pos=self.update_bg, size=self.update_bg)


        self.cols = 1
        self.spacing = 0
        self.prompt = DecoratedLabel(text="Type the following sentence", font_size=45, color=(0,0,0,1) )
        self.add_widget(self.prompt)

        self.sentence_text = Label(text="", color=(1,0,0,1), font_size=20)
        self.add_widget(self.sentence_text)
        self.input_text = TextInput(multiline=False, size_hint=(0.8, None), height=50, pos_hint={"center_x": 0.5, "center_y": 0.5}, font_size=24)
        self.input_text.foreground_color = (0, 1, 0, 1) 
        self.add_widget(self.input_text)

        self.result_text = Label(text="",font_size=17, color=(0,1,0,1))
        self.add_widget(self.result_text)

        self.restart_button = Button(text="Restart")
        self.restart_button = Button(text="Restart", size_hint=(1, .3), pos_hint={"center_x": 0.5}, font_size=25,background_color=(48/255,84/255,150/255,1), background_normal='')
        self.add_widget(self.restart_button)
        self.restart_button.bind(on_press=self.restart_test)
        self.restart_test()
        
        self.showInfo_button = Button(text="?", size_hint=(1, .3), pos_hint={"center_x": 0.5}, font_size=25,background_color=(12/255,84/255,50/255,1), background_normal='')
        self.showInfo_button.bind(on_release=self.show_info_popup)
        self.add_widget(self.showInfo_button)

     def update_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size

     
     def start_timer(self, *args):
        self.start_time = Clock.schedule_interval(self.update_timer, 1)
        self.total_time = 0
        self.num_words_typed = 0

     def update_timer(self, *args):
        self.total_time += 1
        self.result_text.text = "Time: {}".format(self.total_time)

     def check_result(self, instance):
        input_sentence = self.input_text.text.strip()
        num_correct = 0
        num_words_typed = len(input_sentence.split())
        for i in range(min(len(input_sentence), len(self.current_sentence))):
            if input_sentence[i] == self.current_sentence[i]:
                num_correct += 1
        accuracy = num_correct / len(self.current_sentence) * 100
        self.result_text.text = "Accuracy: {:.2f}%, Time: {}, WPM: {}".format(
            accuracy, self.total_time, self.calculate_wpm(num_words_typed))
        self.start_time.cancel()

        # Color coding for accuracy
        if accuracy >= 90:
            self.result_text.color = get_color_from_hex("#16FF00")  # green
        elif accuracy > 50:
            self.result_text.color = get_color_from_hex("#FFA500")  # orange
        else:
            self.result_text.color = get_color_from_hex("#FF0000")  # red

        # Color coding for WPM
        wpm = self.calculate_wpm(num_words_typed)
        if wpm >= 40:
            self.result_text.color = get_color_from_hex("#16FF00")  # green
        else:
            self.result_text.color = get_color_from_hex("#FFA500")  # orange

        if accuracy == 100 and wpm >= 45:
         content = Label(text="Congratulations, you are a typing master!\n \n \nAccuracy: {:.2f}% Time: {}  WPM: {}".format(
                accuracy, self.total_time, wpm), font_size=19, color=(0,1,0,1))
         popup = Popup(title="", content=content, size_hint=(0.8, 0.8))
         popup.open()

     def calculate_wpm(self, num_words_typed):
        if self.total_time == 0:
            return 0
        else:
            return int(num_words_typed / self.total_time * 60)
        
     def restart_test(self, *args):
        self.current_sentence = random.choice(self.SENTENCES)
        self.sentence_text.text = ">>> :   " + self.current_sentence + "   : <<<"
        self.input_text.focus = True
        self.input_text.text = ""
        self.result_text.text = "Type the sentence and press enter"
        self.input_text.bind(on_text_validate=self.check_result)
        self.start_time = Clock.schedule_once(self.start_timer, 1)

     def show_info_popup(self, *args):
        content = Label(text="        Typing Test Game\n\n-English typing speed test\n-There is a function to check the accuracy.\n-There is a print speed check function in WPM units.\n-There is a timer function.\n-If the accuracy is 100 percent and the speed is greater than 45 wpm, \nthere will be a pop-up with a message.")
        popup = Popup(title="About App", content=content, size_hint=(0.8, 0.8))
        popup.open()


class DecoratedLabel(Label):
    font_size = NumericProperty(20)
    font_name = StringProperty('Roboto-Bold.ttf')
    color = (1, 1, 1, 1)
    background_color = (0, 0, 1, 1)

class DecoratedSentenceLabel(DecoratedLabel):
    background_color = (1, 1, 0, 1)  
    padding = (20, 20)  



class TypingTestApp(App):
    def build(self):
        Window.clearcolor = (0.8, 0.2, 0.4)
        return TypingTest()
    
if __name__ == '__main__':
    TypingTestApp().run()
