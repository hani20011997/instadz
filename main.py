from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.utils import platform
from android.storage import app_storage_path
import os
import hashlib
from datetime import datetime

class InstaDZApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage_path = app_storage_path() if platform == 'android' else './'
        self.activation_file = os.path.join(self.storage_path, 'activation_codes.txt')
        
        # إعدادات التفعيل
        self.activation_checked = False
        self.current_code = ""
        self.attempts = 0
        self.MAX_ATTEMPTS = 3
        
        # التحقق من ملف الأكواد عند التهيئة
        self.ensure_activation_file()

    def ensure_activation_file(self):
        """التأكد من وجود ملف الأكواد"""
        if not os.path.exists(self.activation_file):
            self.create_default_activation_file()

    def create_default_activation_file(self):
        """إنشاء ملف أكواد افتراضي إذا لم يوجد"""
        default_codes = [
            "EMERGENCY-CODE-1234",
            "BACKUP-CODE-5678"
        ]
        with open(self.activation_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(default_codes))

    def validate_code(self, code):
        """التحقق من صحة الكود مع معالجة الأخطاء"""
        try:
            if not os.path.exists(self.activation_file):
                return False
                
            with open(self.activation_file, 'r+', encoding='utf-8') as f:
                codes = {line.strip() for line in f if line.strip()}
                
                if code in codes:
                    codes.remove(code)
                    f.seek(0)
                    f.write('\n'.join(codes))
                    f.truncate()
                    return True
        except Exception as e:
            print(f"Error validating code: {e}")
        return False

    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.setup_activation_ui()
        return self.layout

    def setup_activation_ui(self):
        """واجهة تفعيل التطبيق"""
        self.layout.clear_widgets()
        
        # عناصر الواجهة
        title = Label(text="تفعيل التطبيق", font_size='24sp', size_hint=(1, 0.2))
        
        self.code_input = TextInput(
            hint_text="أدخل كود التفعيل",
            multiline=False,
            size_hint=(1, 0.15),
            password=True
        )
        
        activate_btn = Button(
            text="تفعيل الآن",
            size_hint=(1, 0.2),
            background_color=(0, 0.5, 0.8, 1)
        )
        activate_btn.bind(on_press=self.on_activate)
        
        self.status_label = Label(
            text="لديك 3 محاولات متبقية",
            size_hint=(1, 0.1))
        
        # إضافة العناصر للواجهة
        self.layout.add_widget(title)
        self.layout.add_widget(self.code_input)
        self.layout.add_widget(activate_btn)
        self.layout.add_widget(self.status_label)

    def on_activate(self, instance):
        """معالجة ضغط زر التفعيل"""
        code = self.code_input.text.strip()
        
        if not code:
            self.show_error("يجب إدخال كود التفعيل")
            return
            
        if self.attempts >= self.MAX_ATTEMPTS:
            self.show_error("تجاوزت الحد الأقصى للمحاولات")
            return
            
        if self.validate_code(code):
            self.activation_success()
        else:
            self.handle_failed_attempt()

    def activation_success(self):
        """إجراءات بعد التفعيل الناجح"""
        self.activation_checked = True
        self.current_code = self.code_input.text
        self.show_popup("تم التفعيل", "تم تفعيل التطبيق بنجاح!")
        # هنا يمكنك الانتقال للواجهة الرئيسية

    def handle_failed_attempt(self):
        """معالجة المحاولة الفاشلة"""
        self.attempts += 1
        remaining = self.MAX_ATTEMPTS - self.attempts
        self.show_error(f"كود غير صحيح. محاولات متبقية: {remaining}")

    def show_error(self, message):
        """عرض رسالة خطأ"""
        self.status_label.text = message
        self.status_label.color = (1, 0, 0, 1)

    def show_popup(self, title, message):
        """عرض نافذة منبثقة"""
        content = BoxLayout(orientation='vertical', spacing=10)
        content.add_widget(Label(text=message))
        
        btn = Button(text="تم", size_hint=(1, 0.4))
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.4))
        
        btn.bind(on_press=popup.dismiss)
        content.add_widget(btn)
        popup.open()

if __name__ == '__main__':
    InstaDZApp().run()
