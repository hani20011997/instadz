[app]
title = EvilApp
package.name = evilapp
package.domain = org.evil
version = 1.0

source.dir = .
source.main = main.py
source.include_exts = py,png,jpg,kv,atlas,json,txt,xml
source.include_patterns = assets/*,*.txt

requirements = 
    python3,
    kivy==2.1.0,
    requests==2.31.0,
    pillow==10.0.0,
    pyjnius==1.4.2,
    openssl,
    urllib3==1.26.18

android.arch = arm64-v8a
android.ndk = 25b
android.sdk = 33
android.api = 33
android.minapi = 21
android.permissions = INTERNET, ACCESS_NETWORK_STATE

orientation = portrait
fullscreen = 0
icon = icon.png
presplash = presplash.png

[buildozer]
log_level = 2
warn_on_root = 1
