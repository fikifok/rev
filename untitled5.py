# -*- coding: utf-8 -*-
"""
Created on Sun May  4 22:30:11 2025

@author: e
"""

import os, json

cfg_path = os.path.join("config", "settings.json")
print("Dosya var mı? ", os.path.exists(cfg_path))

# Eğer varsa içeriğini gösterelim
if os.path.exists(cfg_path):
    with open(cfg_path, "r", encoding="utf-8") as f:
        data = f.read()
    print("İçerik:\n", data)

    # JSON olarak ayrıştırmayı deneyelim
    try:
        obj = json.loads(data)
        print("Geçerli JSON, anahtarlar:", list(obj.keys()))
    except Exception as e:
        print("JSON hatası:", e)