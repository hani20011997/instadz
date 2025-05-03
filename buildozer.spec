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
android.ndk_version = 25b
android.sdk_version = 34
android.archs = arm64-v8a

[buildozer]
log_level = 2
