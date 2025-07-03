[app]
# معلومات التطبيق الأساسية
title = InstaDZ
package.name = instadz
package.domain = com.dz
version = 1.0

# إعدادات الملفات والمصادر
source.dir = .
source.main = main.py
source.include_exts = py,png,jpg,kv,atlas,json,txt,xml
source.include_patterns = assets/*,sessions/*,*.txt,backup_rules.xml

# المتطلبات
requirements = 
    python3,
    kivy==2.1.0,
    requests==2.31.0,
    pillow==10.0.0,
    pyjnius==1.4.2,
    openssl,
    urllib3==1.26.18,
    certifi,
    cython==0.29.36

# إعدادات Android الأساسية
android.archs = arm64-v8a
android.ndk = 25b
android.api = 33
android.minapi = 21
android.build_tools_version = 34.0.0
android.sdk_dir = %(android_sdk_dir)s
android.ndk_path = %(android_ndk_dir)s
android.p4a_dir = %(p4a_dir)s
android.gradle_dependencies = 'com.android.support:multidex:1.0.3'

# الأذونات
android.permissions = 
    INTERNET,
    ACCESS_NETWORK_STATE,
    ACCESS_WIFI_STATE,
    READ_EXTERNAL_STORAGE,
    WRITE_EXTERNAL_STORAGE

# مكونات التطبيق
orientation = portrait
fullscreen = 0
icon = icon.png
presplash = presplash.png
android.entrypoint = org.kivy.android.PythonActivity
android.allow_backup = True

# تحسينات الأداء
android.memory = 2048
android.no_compile_pyo = 1
android.optimize = 1
android.enable_androidx = 1

[buildozer]
# إعدادات البناء
log_level = 2
warn_on_root = 1
target = android
p4a.branch = develop
android.accept_sdk_license = True
android.skip_update = True
