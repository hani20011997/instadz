[app]
title = InstaDZ
package.name = instadz
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3, kivy==2.3.0, openssl
orientation = portrait

android.api = 30
android.minapi = 21
android.ndk = 23b
android.archs = arm64-v8a
android.build_tools = 30.0.3
android.sdk =

# android.release_keystore = /path/to/keystore
# android.release_storepassword = PASSWORD
# android.release_keypassword = PASSWORD
# android.release_keyalias = ALIAS

log_level = 2
warn_on_root = 1
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
