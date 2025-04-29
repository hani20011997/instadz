from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from activation_codes import valid_codes

class InstaDZApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.logo = Label(text="ddzl", font_size=32, color=(1, 1, 1, 1))
        self.layout.add_widget(self.logo)

        self.code_input = TextInput(
            hint_text='ادخل كود التفعيل',
            size_hint=(1, 0.2),
            multiline=False
        )
        self.layout.add_widget(self.code_input)

        self.check_button = Button(
            text='تحقق من الكود',
            size_hint=(1, 0.2),
            background_color=(0, 1, 0, 1),
            color=(1, 1, 1, 1)
        )
        self.check_button.bind(on_press=self.check_code)
        self.layout.add_widget(self.check_button)

        return self.layout

    def check_code(self, instance):
        entered_code = self.code_input.text.strip()
        if entered_code in valid_codes:
            self.show_popup('نجاح', 'loged')
        else:
            self.show_popup('خطأ', 'error')

    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(None, None),
            size=(300, 200)
        )
        popup.open()

if __name__ == '__main__':
    InstaDZApp().run()
