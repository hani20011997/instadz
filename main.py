from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from android.storage import app_storage_path
from kivy.utils import platform
import threading
import time
import os
import json
import requests
import random

class InstagramVotingApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage_path = app_storage_path() if platform == 'android' else './'
        self.sessions_dir = os.path.join(self.storage_path, 'sessions')
        os.makedirs(self.sessions_dir, exist_ok=True)
        
        # Initialize app data
        self.accounts = []
        self.activation_checked = False
        self.speed_delay = 2
        self.post_id = ""
        self.current_code = ""
        self.max_accounts = 5000
        self.used_accounts_count = 0

    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Activation Section
        self.layout.add_widget(Label(text="أدخل كود التفعيل:"))
        self.activation_input = TextInput(hint_text="كود التفعيل", multiline=False)
        self.layout.add_widget(self.activation_input)
        
        self.activation_button = Button(text="تفعيل", size_hint=(1, 0.2))
        self.activation_button.bind(on_press=self.activate)
        self.layout.add_widget(self.activation_button)
        
        return self.layout

    def activate(self, instance):
        code = self.activation_input.text.strip()
        activation_file = os.path.join(self.storage_path, 'activation_codes.txt')
        
        if not os.path.exists(activation_file):
            self.show_popup("خطأ", "ملف الأكواد غير موجود!")
            return

        with open(activation_file, 'r', encoding='utf-8') as f:
            codes = f.read().splitlines()

        if code in codes:
            self.activation_checked = True
            self.current_code = code
            codes.remove(code)
            
            with open(activation_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(codes))
                
            self.layout.clear_widgets()
            self.build_main_interface()
        else:
            self.show_popup("خطأ", "كود التفعيل غير صحيح!")

    def build_main_interface(self):
        # Post ID Input
        self.layout.add_widget(Label(text="أدخل معرف المنشور:"))
        self.post_input = TextInput(hint_text="مثال: C7Kt0ixsXnX", multiline=False)
        self.layout.add_widget(self.post_input)
        
        # Speed Input
        self.layout.add_widget(Label(text="السرعة (ثواني بين كل تصويت):"))
        self.speed_input = TextInput(text="2", multiline=False)
        self.layout.add_widget(self.speed_input)
        
        # Accounts Input
        self.layout.add_widget(Label(text="الحسابات (user:pass:proxy):"))
        self.account_input = TextInput(hint_text="حساب واحد في كل سطر", multiline=True)
        self.layout.add_widget(self.account_input)
        
        # Buttons
        btn_layout = BoxLayout(size_hint=(1, 0.2))
        self.load_button = Button(text="تحميل الحسابات")
        self.load_button.bind(on_press=self.load_accounts)
        btn_layout.add_widget(self.load_button)
        
        self.start_button = Button(text="بدء التصويت")
        self.start_button.bind(on_press=self.start_voting)
        btn_layout.add_widget(self.start_button)
        
        self.layout.add_widget(btn_layout)
        
        # Status Label
        self.status_label = Label(text="جاهز...", size_hint=(1, 0.2))
        self.layout.add_widget(self.status_label)

    def load_accounts(self, instance):
        accounts_text = self.account_input.text.strip()
        if not accounts_text:
            self.show_popup("خطأ", "لم تدخل أي حسابات!")
            return
            
        new_accounts = []
        for line in accounts_text.split('\n'):
            parts = line.strip().split(':')
            if len(parts) >= 2:
                account = {
                    'username': parts[0],
                    'password': parts[1],
                    'proxy': parts[2] if len(parts) > 2 else None
                }
                new_accounts.append(account)

        if len(new_accounts) + self.used_accounts_count > self.max_accounts:
            self.show_popup("تحذير", "لقد تجاوزت الحد الأقصى للحسابات!")
            return
            
        self.accounts.extend(new_accounts)
        self.used_accounts_count += len(new_accounts)
        self.status_label.text = f"تم تحميل {len(new_accounts)} حساب. الإجمالي: {self.used_accounts_count}"
        
        # Save accounts to file
        backup_file = os.path.join(self.storage_path, 'accounts_backup.txt')
        with open(backup_file, 'a', encoding='utf-8') as f:
            for acc in new_accounts:
                f.write(f"{acc['username']}:{acc['password']}\n")

    def start_voting(self, instance):
        try:
            self.speed_delay = float(self.speed_input.text)
        except ValueError:
            self.show_popup("خطأ", "السرعة يجب أن تكون رقمًا!")
            return
            
        self.post_id = self.post_id = self.post_input.text.strip()
        if not self.post_id:
            self.show_popup("خطأ", "يجب إدخال معرف المنشور!")
            return
            
        if not self.accounts:
            self.show_popup("خطأ", "لا توجد حسابات محملة!")
            return
            
        self.status_label.text = "جارٍ التصويت..."
        
        for account in self.accounts:
            threading.Thread(
                target=self.vote_with_account,
                args=(account['username'], account['password'], account['proxy'])
            ).start()
            time.sleep(self.speed_delay)
            
        self.status_label.text = "تم الانتهاء من التصويت!"

    def vote_with_account(self, username, password, proxy=None):
        session_file = os.path.join(self.sessions_dir, f'{username}.json')
        try:
            # Simulate voting (replace with actual API calls)
            time.sleep(random.uniform(1, 3))
            
            # Log status
            log_msg = f"تم التصويت على المنشور {self.post_id} باستخدام حساب {username}"
            self.log_status(username, log_msg)
            
        except Exception as e:
            self.log_status(username, f"فشل: {str(e)}")

    def log_status(self, username, message):
        log_file = os.path.join(self.storage_path, 'log.txt')
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{time.ctime()}] {username}: {message}\n")

    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.8, 0.4)
        )
        popup.open()

if __name__ == '__main__':
    InstagramVotingApp().run()
