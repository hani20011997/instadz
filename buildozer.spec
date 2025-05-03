[app]
title = MyApp
package.name = com.example.myapp
package.domain = org.example
source.dir = .
version = 1.0
requirements = 
    python3,
    kivy==2.2.1,
    cython==3.0.0,
    openssl

android.accept_sdk_license = True
android.ndk_path = /home/runner/android-sdk/ndk/25b
android.sdk_path = /home/runner/android-sdk
android.archs = arm64-v8a
android.targetapi = 34
android.minapi = 21

[buildozer]
log_level = 2
