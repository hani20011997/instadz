[app]
title = EvilApp
package.name = evilapp
package.domain = org.evil
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy==2.1.0,pyjnius
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 23.1.7779620
android.arch = arm64-v8a
orientation = portrait
fullscreen = 0
icon = icon.png
presplash = presplash.png
android.entrypoint = org.kivy.android.PythonActivity
android.add_aar =
android.add_jars =
android.add_src =
android.skip_update = False
android.allow_backup = True
android.backup_rules = backup_rules.xml

[buildozer]
log_level = 2
warn_on_root = 1
