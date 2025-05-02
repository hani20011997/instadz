[app]
title = MyApp
package.name = com.mycompany.myapp
package.domain = org.mycompany
source.dir = .
version = 1.0
requirements = 
    python3 == 3.10.12,
    kivy == 2.2.1,
    openssl == 3.1.4,
    requests == 2.31.0
android.accept_sdk_license = True
android.ndk_path = /usr/lib/android-ndk-r25b
android.sdk_path = /usr/lib/android-sdk
android.archs = arm64-v8a

[buildozer]
log_level = 2
disable_auto_clean = False
