[app]
title = InstaDZ
package.name = instadz
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3, kivy==2.3.0
orientation = portrait

# إعدادات Android
android.api = 30  # Android 11 (أكثر استقرارًا)
android.minapi = 21
android.sdk =  # اتركه فارغًا ليتحمله Buildozer تلقائيًا
android.ndk = 25b  # أو 23b للإصدارات الأقدم
android.build_tools_version = 30.0.3  # متوافق مع api 30
android.arch = arm64-v8a  # للأجهزة الحديثة

# إعدادات التصحيح
log_level = 2
warn_on_root = 1
