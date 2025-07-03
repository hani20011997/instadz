from instagrapi import Client
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
import threading
import time
import os
import smtplib
import json
from email.mime.text import MIMEText
import random

class InstagramVotingApp(App):
    def build(self):
        self.accounts = []
        self.activation_checked = False
        self.speed_delay = 2
        self.post_id = ""
        self.current_code = ""
        self.max_accounts = 5000
        self.used_accounts_count = 0

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.status_label = Label(text="أدخل كود التفعيل:")
        self.layout.add_widget(self.status_label)

        self.activation_input = TextInput(hint_text="كود التفعيل", multiline=False)
        self.layout.add_widget(self.activation_input)

        self.activation_button = Button(text="تفعيل", on_press=self.activate)
        self.layout.add_widget(self.activation_button)

        return self.layout

    def activate(self, instance):
        code = self.activation_input.text.strip()
        if not os.path.exists("activation_codes.txt"):
            self.status_label.text = "ملف الأكواد غير موجود!"
            return

        with open("activation_codes.txt", "r", encoding="utf-8") as f:
            codes = f.read().splitlines()

        if code in codes:
            self.activation_checked = True
            self.current_code = code
            self.used_accounts_count = 0
            codes.remove(code)
            with open("activation_codes.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(codes))
            self.layout.clear_widgets()
            self.build_main_interface()
        else:
            self.status_label.text = "كود غير صالح!"
            threading.Thread(target=self.send_recovery_email, args=(code,)).start()

    def build_main_interface(self):
        self.layout.add_widget(Label(text="post ID أو رابط المنشور"))
        self.post_input = TextInput(hint_text="مثال: C7Kt0ixsXnX", multiline=False)
        self.layout.add_widget(self.post_input)

        self.layout.add_widget(Label(text="السرعة (ثواني بين كل تصويت)"))
        self.speed_input = TextInput(hint_text="مثال: 2", multiline=False)
        self.layout.add_widget(self.speed_input)

        self.account_input = TextInput(hint_text="أدخل الحسابات بصيغة user:pass أو user:pass:proxy", multiline=True)
        self.layout.add_widget(self.account_input)

        self.load_button = Button(text="تحميل الحسابات", on_press=self.load_accounts)
        self.layout.add_widget(self.load_button)

        self.start_button = Button(text="بدء التصويت", on_press=self.start_voting)
        self.layout.add_widget(self.start_button)

        self.status_label = Label(text="جاهز.")
        self.layout.add_widget(self.status_label)

    def show_limit_popup(self):
        popup = Popup(title='الحد الأقصى',
                      content=Label(text='لقد وصلت للحد الأقصى من الحسابات المسموح بها لهذا الكود.'),
                      size_hint=(0.8, 0.4))
        popup.open()

    def load_accounts(self, instance):
        text = self.account_input.text.strip()
        lines = text.split("\n")
        new_accounts = []

        for line in lines:
            parts = line.strip().split(":")
            if len(parts) >= 2:
                username = parts[0]
                password = parts[1]
                proxy = ":".join(parts[2:]) if len(parts) > 2 else None
                new_accounts.append((username, password, proxy))

        if len(new_accounts) + self.used_accounts_count > self.max_accounts:
            self.show_limit_popup()
            return

        self.accounts.extend(new_accounts)
        self.used_accounts_count += len(new_accounts)

        with open("accounts_backup.txt", "a", encoding="utf-8") as f:
            for acc in new_accounts:
                f.write(":".join([a for a in acc if a]) + "\n")

        self.status_label.text = f"تم تحميل {len(new_accounts)} حساب. الإجمالي: {self.used_accounts_count}"

    def vote_with_account(self, username, password, proxy=None, competitor=1):
        session_file = f"sessions/{username}.json"
        cl = Client()

        try:
            if proxy:
                cl.set_proxy(proxy)

            if os.path.exists(session_file):
                with open(session_file, "r", encoding="utf-8") as f:
                    settings = json.load(f)
                cl.set_settings(settings)

            cl.login(username, password)

            # حفظ الجلسة
            os.makedirs("sessions", exist_ok=True)
            with open(session_file, "w", encoding="utf-8") as f:
                json.dump(cl.get_settings(), f)

            time.sleep(random.randint(2, 5))

            if competitor == 1:
                cl.post_like(self.post_id)
                self.log_status(username, "تم التصويت بنجاح.")
            else:
                cl.post_unlike(self.post_id)
                self.log_status(username, "تم إلغاء التصويت بنجاح.")
        except Exception as e:
            self.log_status(username, f"فشل: {str(e)}")

    def log_status(self, username, message):
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{username}] {message}\n")

    def start_voting(self, instance):
        try:
            self.speed_delay = int(self.speed_input.text.strip())
        except ValueError:
            self.status_label.text = "الرجاء إدخال رقم صحيح للسرعة."
            return

        self.post_id = self.post_input.text.strip()
        if not self.post_id:
            self.status_label.text = "الرجاء إدخال معرف المنشور."
            return

        if not self.accounts:
            self.status_label.text = "لا توجد حسابات محملة."
            return

        self.status_label.text = "جارٍ التصويت..."

        competitor = 1  # يمكن تعديل هذا حسب الحاجة

        for username, password, proxy in self.accounts:
            threading.Thread(target=self.vote_with_account, args=(username, password, proxy, competitor)).start()
            time.sleep(self.speed_delay)

        self.status_label.text = "انتهى التصويت."

    def send_recovery_email(self, code):
        msg = MIMEText(f"محاولة تفعيل باستخدام كود غير مسجل: {code}")
        msg["Subject"] = "طلب استعادة كود تفعيل"
        msg["From"] = "noreply@app.com"
        msg["To"] = "hani122312234@gmail.com"

        try:
            server = smtplib.SMTP("smtp.example.com", 587)
            server.starttls()
            server.login("your_email@example.com", "your_password")
            server.send_message(msg)
            server.quit()
        except Exception as e:
            print("فشل إرسال البريد:", e)

if __name__ == '__main__':
    InstagramVotingApp().run()
    
