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
        
        # Initialize app data
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
        
        # عنوان التطبيق
        title = Label(text="InstaDZ - تفعيل التطبيق", font_size='20sp', size_hint=(1, 0.2))
        self.layout.add_widget(title)
        
        # حقل إدخال الكود
        self.activation_input = TextInput(
            hint_text="أدخل كود التفعيل",
            multiline=False,
            size_hint=(1, 0.15)
        self.layout.add_widget(self.activation_input)
        
        # زر التفعيل
        activate_btn = Button(
            text="تفعيل",
            size_hint=(1, 0.2),
            background_color=(0, 0.7, 0, 1))
        activate_btn.bind(on_press=self.activate)
        self.layout.add_widget(activate_btn)
        
        # حالة التطبيق
        self.status_label = Label(
            text="انتظر التفعيل...",
            size_hint=(1, 0.1))
        self.layout.add_widget(self.status_label)

    def activate(self, instance):
        """معالجة عملية التفعيل"""
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
                
            self.setup_main_interface()
        else:
            self.status_label.text = "كود التفعيل غير صحيح!"
            self.status_label.color = (1, 0, 0, 1)

    def setup_main_interface(self):
        """الواجهة الرئيسية بعد التفعيل"""
        self.layout.clear_widgets()
        
        # شريط العنوان
        title = Label(text="InstaDZ - الواجهة الرئيسية", font_size='20sp', size_hint=(1, 0.15))
        self.layout.add_widget(title)
        
        # قسم إدخال المنشور
        post_layout = BoxLayout(size_hint=(1, 0.15))
        post_layout.add_widget(Label(text="معرف المنشور:", size_hint=(0.3, 1)))
        self.post_input = TextInput(hint_text="مثال: C7Kt0ixsXnX", size_hint=(0.7, 1))
        post_layout.add_widget(self.post_input)
        self.layout.add_widget(post_layout)
        
        # قسم السرعة
        speed_layout = BoxLayout(size_hint=(1, 0.15))
        speed_layout.add_widget(Label(text="السرعة (ثانية):", size_hint=(0.3, 1)))
        self.speed_input = TextInput(text="2", size_hint=(0.7, 1))
        speed_layout.add_widget(self.speed_input)
        self.layout.add_widget(speed_layout)
        
        # قسم الحسابات
        accounts_label = Label(text="الحسابات (user:pass:proxy):", size_hint=(1, 0.1))
        self.layout.add_widget(accounts_label)
        
        self.account_input = TextInput(
            hint_text="حساب واحد في كل سطر",
            multiline=True,
            size_hint=(1, 0.3))
        self.layout.add_widget(self.account_input)
        
        # أزرار التحكم
        btn_layout = BoxLayout(size_hint=(1, 0.15))
        load_btn = Button(text="تحميل الحسابات")
        load_btn.bind(on_press=self.load_accounts)
        btn_layout.add_widget(load_btn)
        
        start_btn = Button(text="بدء التصويت", background_color=(0, 0.7, 0, 1))
        start_btn.bind(on_press=self.start_voting)
        btn_layout.add_widget(start_btn)
        self.layout.add_widget(btn_layout)
        
        # حالة التطبيق
        self.status_label = Label(
            text=f"حسابات محملة: {self.used_accounts_count}/{self.max_accounts}",
            size_hint=(1, 0.1))
        self.layout.add_widget(self.status_label)

    def load_accounts(self, instance):
        """تحميل الحسابات من واجهة المستخدم"""
        accounts_text = self.account_input.text.strip()
        if not accounts_text:
            self.show_popup("تحذير", "لم تقم بإدخال أي حسابات!")
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
            self.show_popup("تحذير", f"تجاوزت الحد الأقصى ({self.max_accounts} حساب)")
            return
            
        self.accounts.extend(new_accounts)
        self.used_accounts_count += len(new_accounts)
        self.status_label.text = f"حسابات محملة: {self.used_accounts_count}/{self.max_accounts}"
        
        # حفظ نسخة احتياطية
        self.save_accounts_backup(new_accounts)

    def save_accounts_backup(self, accounts):
        """حفظ الحسابات في ملف"""
        backup_file = os.path.join(self.storage_path, 'accounts_backup.txt')
        with open(backup_file, 'a', encoding='utf-8') as f:
            for acc in accounts:
                f.write(f"{acc['username']}:{acc['password']}\n")

    def start_voting(self, instance):
        """بدء عملية التصويت"""
        try:
            self.speed_delay = max(1, float(self.speed_input.text))
        except ValueError:
            self.show_popup("خطأ", "يجب أن تكون السرعة رقماً صحيحاً")
            return
            
        self.post_id = self.post_input.text.strip()
        if not self.post_id:
            self.show_popup("خطأ", "يجب إدخال معرف المنشور")
            return
            
        if not self.accounts:
            self.show_popup("خطأ", "لم تقم بتحميل أي حسابات")
            return
            
        self.status_label.text = "جارٍ التصويت..."
        
        # بدء التصويت في خيط منفصل
        threading.Thread(target=self.run_voting_process).start()

    def run_voting_process(self):
        """تشغيل عملية التصويت في الخلفية"""
        for account in self.accounts:
            if not self.post_id:  # إيقاف إذا تم مسح معرف المنشور
                break
                
            self.vote_with_account(account)
            time.sleep(self.speed_delay)
            
        self.status_label.text = f"تم الانتهاء من {len(self.accounts)} تصويت!"

    def vote_with_account(self, account):
        """تنفيذ تصويت بحساب واحد"""
        session_file = os.path.join(self.sessions_dir, f"{account['username']}.json")
        try:
            # محاكاة عملية التصويت (استبدل هذا بمنطق API الحقيقي)
            time.sleep(random.uniform(1, 3))
            
            # تسجيل النجاح
            log_msg = f"تم التصويت على {self.post_id} بواسطة {account['username']}"
            self.log_status(account['username'], log_msg)
            
        except Exception as e:
            self.log_status(account['username'], f"فشل: {str(e)}")

    def log_status(self, username, message):
        """تسجيل أحداث التطبيق"""
        log_file = os.path.join(self.storage_path, 'instadz_log.txt')
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{time.ctime()}] {username}: {message}\n")

    def show_popup(self, title, message):
        """عرض نافذة منبثقة"""
        content = BoxLayout(orientation='vertical', spacing=10)
        content.add_widget(Label(text=message))
        
        btn = Button(text="موافق", size_hint=(1, 0.4))
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.4))
        
        btn.bind(on_press=popup.dismiss)
        content.add_widget(btn)
        popup.open()

if __name__ == '__main__':
    InstaDZApp().run()
