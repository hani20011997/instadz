[app]
title = MyApp
package.name = com.myapp.example
package.domain = org.example
source.dir = .
version = 1.0
requirements = 
    python3,
    kivy==2.2.1,
    cython==3.0.8,
    requests==2.31.0
android.accept_sdk_license = True
android.ndk_version = 25b
android.sdk_version = 34
android.archs = arm64-v8a, armeabi-v7a
android.wakelock = True
android.meta_data = com.example.metadata=value

[buildozer]
log_level = 2
