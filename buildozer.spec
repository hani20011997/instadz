[app]
title = InstaDZ
package.name = instadz
package.domain = com.dz
version = 1.0

source.dir = .
source.main = main.py
source.include_exts = py,png,jpg,kv,atlas,json,txt,xml
source.include_patterns = assets/*,sessions/*,*.txt

requirements = 
    python3,
    kivy==2.1.0,
    requests==2.31.0,
    pillow==10.0.0,
    pyjnius==1.4.2,
    openssl,
    urllib3,
    certifi,
    cython==0.29.36

android.archs = arm64-v8a
android.ndk = 25b
android.api = 33
android.minapi = 21
android.build_tools_version = 34.0.0
android.sdk_dir = %(android_sdk_dir)s
android.ndk_path = %(android_ndk_dir)s
android.gradle_dependencies = 'com.android.support:multidex:1.0.3'

android.permissions = INTERNET, ACCESS_NETWORK_STATE

orientation = portrait
fullscreen = 0
icon = icon.png
presplash = presplash.png
android.entrypoint = org.kivy.android.PythonActivity
android.allow_backup = False

[buildozer]
log_level = 2
warn_on_root = 1
target = android
p4a.branch = develop
android.accept_sdk_license = True
