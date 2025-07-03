[app]
title = InstaDZ
package.name = instadz
package.domain = com.dz
version = 1.0

source.dir = .
source.main = main.py
source.include_exts = py,png,jpg,kv,txt
source.include_patterns = *.txt

requirements =
    python3,
    kivy==2.1.0,
    openssl

android.archs = arm64-v8a
android.api = 33
android.minapi = 21
android.build_tools_version = 33.0.0

android.permissions = INTERNET

orientation = portrait
fullscreen = 0
icon = icon.png
presplash = presplash.png

[buildozer]
log_level = 2
warn_on_root = 1
