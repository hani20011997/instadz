[app]
title = InstaDZ
package.name = com.instadz.app
package.domain = org.instadz
source.dir = .
version = 1.0
requirements = python3,kivy,requests
android.accept_sdk_license = True

# استبدل android.arch بـ android.archs
android.archs = armeabi-v7a
android.ndk_version = 25b
android.sdk_version = 34

# إعدادات إضافية
[buildozer]
log_level = 2
