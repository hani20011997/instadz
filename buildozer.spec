[app]

# Basic Info
title = EvilApp
package.name = evilapp
package.domain = org.evil
version = 1.0

# Files and Sources
source.dir = .
source.main = main.py
source.include_exts = py,png,jpg,kv,atlas,json,txt,xml
source.include_patterns = assets/*,res/*,sessions/*,*.txt

# Requirements (Adjusted for your Instagram voting app)
requirements = 
    python3,
    kivy==2.1.0,
    pyjnius,
    instagrapi,
    requests,
    pillow,
    openssl,
    urllib3,
    certifi,
    chardet,
    idna

# Android Config
android.arch = arm64-v8a
android.ndk = 25b
android.sdk = 33
android.api = 33
android.minapi = 21
android.gradle_dependencies = 'com.android.support:multidex:1.0.3'

# Permissions (Minimal required)
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# App Components
orientation = portrait
fullscreen = 0
icon = icon.png
presplash = presplash.png
android.entrypoint = org.kivy.android.PythonActivity
android.allow_backup = False
android.backup_rules = backup_rules.xml

# Performance Optimizations
android.memory = 2048
android.no-compile-pyo = True
android.optimize = True
android.enable_androidx = True

# Buildozer Settings
[buildozer]
log_level = 2
warn_on_root = 1
target = android
p4a.branch = develop
android.accept_sdk_license = True
