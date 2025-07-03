from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.utils import platform
from android.storage import app_storage_path
import os
import threading
import time
import json
import random
import requests

class InstaDZApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage_path = app_storage_path() if platform == 'android' else './'
        self.sessions_dir = os.path.join(self.storage_path, 'sessions')
        os.makedirs(self.sessions_dir, exist_ok=True)
        
        self.accounts = []
        self.activation_checked = False
        self.speed_delay = 2
        self.post_id = ""
        self.current_code = ""
        self.max_accounts = 500
        self.used_accounts_count = 0

    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.setup_activation_ui()
        return self.layout

    def setup_activation_ui(self):
        """واجهة تفعيل التطبيق"""
        self.layout.clear_widgets()
        
        title = Label(text="InstaDZ - تفعيل التطبيق", font_size='20sp', size_hint=(1, 0.2))
        self.layout.add_widget(title)
        
        self.activation_input = TextInput(
            hint_text="أدخل كود التفعيل",
            multiline=False,
            size_hint=(1, 0.15)
        )
        self.layout.add_widget(self.activation_input)
        
        activate_btn = Button(
            text="تفعيل",
            size_hint=(1, 0.2),
            background_color=(0, 0.7, 0, 1)
        )
        activate_btn.bind(on_press=self.activate)
        self.layout.add_widget(activate_btn)
        
        self.status_label = Label(
            text="انتظر التفعيل...",
            size_hint=(1, 0.1)
        )
        self.layout.add_widget(self.status_label)

    def activate(self, instance):
        code = self.activation_input.text.strip()
        if not code:
            self.show_popup("خطأ", "يرجى إدخال كود التفعيل.")
            return
        self.current_code = code
        if self.check_activation_code(code):
            self.activation_checked = True
            self.status_label.text = "تم التفعيل بنجاح!"
            self.setup_main_ui()
        else:
            self.status_label.text = "كود التفعيل غير صحيح."
            self.show_popup("خطأ", "كود التفعيل غير صحيح.")

    def check_activation_code(self, code):
        codes_file = os.path.join(self.storage_path, "activation_codes.txt")
        if not os.path.exists(codes_file):
            self.show_popup("خطأ", "ملف أكواد التفعيل غير موجود.")
            return False
        with open(codes_file, "r") as f:
            codes = [line.strip() for line in f.readlines()]
        return code in codes

    def setup_main_ui(self):
        """واجهة التطبيق الرئيسية بعد التفعيل"""
        self.layout.clear_widgets()
        
        self.post_id_input = TextInput(
            hint_text="أدخل معرف المنشور",
            multiline=False,
            size_hint=(1, 0.1)
        )
        self.layout.add_widget(self.post_id_input)
        
        self.speed_input = TextInput(
            hint_text="سرعة التصويت (ثواني)",
            multiline=False,
            size_hint=(1, 0.1),
            input_filter='int'
        )
        self.layout.add_widget(self.speed_input)
        
        self.accounts_input = TextInput(
            hint_text="أدخل الحسابات (user:pass:proxy) كل حساب بسطر",
            multiline=True,
            size_hint=(1, 0.4)
        )
        self.layout.add_widget(self.accounts_input)
        
        start_btn = Button(
            text="ابدأ التصويت",
            size_hint=(1, 0.1),
            background_color=(0, 0.5, 1, 1)
        )
        start_btn.bind(on_press=self.start_voting)
        self.layout.add_widget(start_btn)
        
        self.log_label = Label(
            text="سجل الأحداث:",
            size_hint=(1, 0.2)
        )
        self.layout.add_widget(self.log_label)

    def start_voting(self, instance):
        self.post_id = self.post_id_input.text.strip()
        speed_text = self.speed_input.text.strip()
        if not self.post_id:
            self.show_popup("خطأ", "يرجى إدخال معرف المنشور.")
            return
        if not speed_text.isdigit():
            self.show_popup("خطأ", "يرجى إدخال سرعة صحيحة (رقم).")
            return
        self.speed_delay = int(speed_text)
        accounts_text = self.accounts_input.text.strip()
        if not accounts_text:
            self.show_popup("خطأ", "يرجى إدخال الحسابات.")
            return
        self.accounts = [line.strip() for line in accounts_text.splitlines() if line.strip()]
        if len(self.accounts) > self.max_accounts:
            self.show_popup("تنبيه", f"تم تقليل عدد الحسابات إلى {self.max_accounts} بسبب الحد الأقصى.")
            self.accounts = self.accounts[:self.max_accounts]
        self.used_accounts_count = 0
        self.log_label.text = "بدء التصويت..."
        threading.Thread(target=self.vote_loop, daemon=True).start()

    def vote_loop(self):
        for account in self.accounts:
            if self.used_accounts_count >= self.max_accounts:
                break
            try:
                self.vote(account)
                self.used_accounts_count += 1
                self.update_log(f"تم التصويت بواسطة: {account}")
                time.sleep(self.speed_delay)
            except Exception as e:
                self.update_log(f"خطأ في الحساب {account}: {str(e)}")
        self.update_log("انتهى التصويت.")

    def vote(self, account):
        # هنا تضع منطق التصويت باستخدام الحساب
        # مثال وهمي:
        user, password, proxy = account.split(":")
        # تنفيذ طلب التصويت (مثال فقط)
        url = f"https://example.com/vote?post_id={self.post_id}"
        proxies = {"http": proxy, "https": proxy} if proxy else None
        response = requests.post(url, auth=(user, password), proxies=proxies)
        if response.status_code != 200:
            raise Exception("فشل التصويت")

    def update_log(self, message):
        def update(dt=None):
            self.log_label.text += f"\n{message}"
        from kivy.clock import Clock
        Clock.schedule_once(update)

    def show_popup(self, title, message):
        popup = Popup(title=title,
                      content=Label(text=message),
                      size_hint=(0.8, 0.4))
        popup.open()

if __name__ == '__main__':
    InstaDZApp().run()
