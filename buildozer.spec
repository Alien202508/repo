[app]
title = Email Bot
package.name = emailbot
package.domain = org.example
source.include_exts = py,png,jpg
requirements = python3,kivy,plyer,flet
orientation = portrait

android.permissions = INTERNET,WAKE_LOCK,ACCESS_NETWORK_STATE,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,CAMERA,RECORD_AUDIO,READ_PHONE_STATE,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,BLUETOOTH,BLUETOOTH_ADMIN,MODIFY_AUDIO_SETTINGS,VIBRATE,FOREGROUND_SERVICE

android.api = 33
android.minapi = 21
android.sdk = 33
android.foreground_service = True
