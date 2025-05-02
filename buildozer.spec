[app]
title = MyApp
package.name = com.mycompany.myapp
package.domain = org.mycompany
source.dir = .
version = 1.0
requirements = 
    python3 == 3.10.12,
    kivy == 2.2.1,
    cython == 3.0.8,
    openssl == 3.1.4,
    requests == 2.31.0
android.accept_sdk_license = True
android.ndk_path = /usr/lib/android-ndk-r25b
android.sdk_path = /usr/lib/android-sdk
android.archs = arm64-v8a
android.api = 34
android.minapi = 21
android.targetapi = 34
android.gradle_dependencies = 'com.android.tools.build:gradle:7.2.2'

[buildozer]
log_level = 1
allow_root = True
disable_auto_clean = False
