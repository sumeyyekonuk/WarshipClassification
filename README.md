# ⚓ Naval Vessel Recognition System

YOLOv8 tabanlı savaş gemisi sınıflandırma projesi. Görüntüden gemi türünü tanıyan, bilinmeyen nesneleri reddedebilen bir masaüstü uygulaması.

---

## 🚢 Sınıflar

| Sınıf | Açıklama | Görüntü Sayısı |
|---|---|---|
| AhmadYani | Malezya fırkateyni | 85 |
| Anzac | Avustralya/Yeni Zelanda fırkateyni | 106 |
| ArleighBurke | ABD destroyer sınıfı | 120 |
| FFS | Fransız fırkateyni | 132 |
| Heybeliada | Türk korvet sınıfı | 60 |
| Lekiu | Malezya fırkateyni | 128 |
| LMV | Hafif deniz aracı | 61 |
| Type45 | İngiliz destroyer sınıfı | 158 |
| bilinmeyen | İnsan, at, uçak, araba, yelkenli, konteyner vb. | 60 |

> **bilinmeyen** sınıfı sayesinde model, gemilerle karşılaştığında sınıflandırma yapar; gemi olmayan nesnelerle karşılaştığında ise "bilinmeyen" olarak etiketler.

---

## 🏗️ Proje Yapısı

```
naval_classification/
├── main.py          # PyQt5 masaüstü arayüzü
├── best.pt          # Eğitilmiş YOLOv8 model ağırlıkları (~10MB)
├── requirements.txt
└── README.md
```

---

## 🧠 Model

- **Mimari:** YOLOv8s-cls (classification)
- **Eğitim:** Google Colab (T4 GPU)
- **Epoch:** 50
- **Görüntü boyutu:** 224x224
- **Batch size:** 32
- **Dropout:** 0.3
- **Veri seti:** [Roboflow - Warship Classification 4Dec](https://universe.roboflow.com/smu-gkbdw/warship-classification-4dec) (960 görüntü, v6)
- **Validation Accuracy:** ~97.7%

---

## 🖥️ Kurulum

```bash
# 1. Repoyu klonla
git clone https://github.com/sumeyyekonuk/WarshipClassification.git
cd WarshipClassification

# 2. Sanal ortam oluştur (opsiyonel)
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Bağımlılıkları yükle
pip install -r requirements.txt

# 4. Çalıştır
python main.py
```

---

## 📦 Gereksinimler

```
ultralytics
PyQt5
opencv-python
Pillow
torch
torchvision
```

---

## 🗂️ Eğitim Kodu

Model Google Colab'da eğitilmiştir:

```python
from ultralytics import YOLO

model = YOLO("yolov8s-cls.pt")

results = model.train(
    data="/content/Warship-Classification-4Dec-5",
    epochs=50,
    imgsz=224,
    batch=32,
    name="warship_model_v5",
    patience=10,
    dropout=0.3
)
```

<img width="1242" height="866" alt="Ekran görüntüsü 2026-05-21 183505" src="https://github.com/user-attachments/assets/9cbcd1dd-d674-48aa-b344-41ffc67cc53b" />
<img width="1188" height="833" alt="Ekran görüntüsü 2026-05-21 183519" src="https://github.com/user-attachments/assets/24d08784-0a73-4187-b740-318c7a8e39cb" />
<img width="1263" height="828" alt="Ekran görüntüsü 2026-05-21 183533" src="https://github.com/user-attachments/assets/8a274841-7abe-4539-aadd-32af1808afdb" />
<img width="1172" height="810" alt="Ekran görüntüsü 2026-05-21 183549" src="https://github.com/user-attachments/assets/c81ec254-1622-449c-b7de-5866e38ab111" />
<img width="1097" height="762" alt="Ekran görüntüsü 2026-05-21 183607" src="https://github.com/user-attachments/assets/edec2996-d4f0-4a88-b125-5be0644ec050" />
