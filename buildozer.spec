[app]
title = MyApp
package.name = com.example.myapp
package.domain = org.example
source.dir = .
version = 1.0
requirements = python3,kivy==2.2.1,cython==3.0.0,openssl,requests

# ملفات الموارد (أيقونة، شاشة البداية...)
icon.filename = %(source.dir)s/data/icon.png
presplash.filename = %(source.dir)s/data/splash.png

android.accept_sdk_license = True

android.ndk_path = /home/runner/android-sdk/ndk/25b
android.sdk_path = /home/runner/android-sdk

[buildozer]
android.archs = arm64-v8a
android.targetapi = 34
android.minapi = 21

# ملفات يجب تضمينها داخل APK
source.include_exts = py,png,jpg,kv,atlas
source.include_patterns = assets/*,images/*,data/*

# إعدادات Buildozer
[buildozer]
log_level = 2
p4a.branch = 2023.08.25
p4a.source_dir = .buildozer/android/platform/python-for-android
p4a.recommended_ndk_version = 25b
p4a.bootstrap = sdl2
orientation = portrait

# إعدادات التوقيع للتصدير بنسخة Release
android.release_keystore = /path/to/keystore.keystore
android.release_keystore_password = password
android.release_keyalias = alias
android.release_keypassword = password

# الأذونات المطلوبة للتطبيق
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# التبعيات الإضافية لـ Gradle
android.gradle_dependencies = com.android.tools.build:gradle:7.2.2,com.google.firebase:firebase-core:21.1.1

# البيانات التعريفية (meta-data) الإضافية
android.meta_data = com.google.android.gms.version=@integer/google_play_services_version

# إضافة عناصر مخصصة إلى ملف AndroidManifest.xml
android.extra_manifest_xml = 
    <application>
        <meta-data android:name="com.google.android.gms.ads.APPLICATION_ID" android:value="ca-app-pub-xxxxxxxx~yyyyyyyyyy"/>
    </application>

# تحسينات الأداء
java_max_heap_size = 2G
android.skip_compile = False
