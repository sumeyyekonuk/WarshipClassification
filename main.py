import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel,
                              QPushButton, QFileDialog, QVBoxLayout,
                              QHBoxLayout, QWidget, QGraphicsDropShadowEffect,
                              QScrollArea, QFrame)
from PyQt5.QtGui import QPixmap, QFont, QColor, QPalette
from PyQt5.QtCore import Qt
from ultralytics import YOLO

WARSHIP_DATA = [
    {"name": "AhmadYani",    "country": "Indonesia",     "code": "ID", "type": "Frigate"},
    {"name": "Anzac",        "country": "Australia / NZ","code": "AU", "type": "Frigate"},
    {"name": "ArleighBurke", "country": "USA",           "code": "US", "type": "Destroyer"},
    {"name": "FFS",          "country": "France",        "code": "FR", "type": "Frigate"},
    {"name": "Heybeliada",   "country": "Turkey",        "code": "TR", "type": "Corvette"},
    {"name": "Lekiu",        "country": "Malaysia",      "code": "MY", "type": "Frigate"},
    {"name": "LMV",          "country": "Italy",         "code": "IT", "type": "Patrol Vessel"},
    {"name": "Type45",       "country": "UK",            "code": "GB", "type": "Destroyer"},
    {"name": "bilinmeyen",   "country": "Unknown",       "code": "??", "type": "Unidentified"},
]

BG_DEEP   = "#060d16"
BG_PANEL  = "#040c18"
BG_CARD   = "#0a1520"
BG_CARD_A = "#0d2040"
BORDER    = "#1a3045"
BORDER_A  = "#4fc3f7"
TEXT_PRI  = "#e8f4ff"
TEXT_SEC  = "#6ab0cc"
TEXT_ACT  = "#4fc3f7"
ACCENT    = "#4fc3f7"
GREEN     = "#00e676"
RED       = "#ef5350"


class ShipCard(QWidget):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.setFixedHeight(68)
        self.active = False
        self._build()

    def _build(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 12, 6)
        layout.setSpacing(10)

        # Renkli arka planlı ülke kodu etiketi
        self.flag_label = QLabel(self.data["code"])
        self.flag_label.setFixedSize(42, 42)
        self.flag_label.setAlignment(Qt.AlignCenter)
        self.flag_label.setFont(QFont("Consolas", 11, QFont.Bold))
        self.flag_label.setStyleSheet("""
            background: #0d2a40;
            border: 1px solid #1a4060;
            border-radius: 6px;
            color: #4fc3f7;
            letter-spacing: 1px;
        """)
        layout.addWidget(self.flag_label)

        # Dikey ayırıcı
        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setFixedWidth(1)
        sep.setStyleSheet("background: #1e3550; border: none;")
        layout.addWidget(sep)

        # İsim + detay
        info = QVBoxLayout()
        info.setSpacing(3)

        self.name_label = QLabel(self.data["name"])
        name_font = QFont()
        name_font.setFamilies(["JetBrains Mono", "Cascadia Code", "Fira Code", "Consolas"])
        name_font.setPointSize(11)
        name_font.setBold(True)
        self.name_label.setFont(name_font)
        self.name_label.setStyleSheet(
            f"color: {TEXT_PRI}; background: transparent; letter-spacing: 1px;"
        )

        detail_text = f"{self.data['country']}  ·  {self.data['type']}"
        self.detail_label = QLabel(detail_text)
        detail_font = QFont()
        detail_font.setFamilies(["JetBrains Mono", "Cascadia Code", "Fira Code", "Consolas"])
        detail_font.setPointSize(9)
        self.detail_label.setFont(detail_font)
        self.detail_label.setStyleSheet(
            f"color: {TEXT_SEC}; background: transparent;"
        )

        info.addWidget(self.name_label)
        info.addWidget(self.detail_label)
        layout.addLayout(info)
        layout.addStretch()

        self._set_style(active=False)

    def _set_style(self, active):
        if active:
            self.setStyleSheet(f"""
                ShipCard {{
                    background: {BG_CARD_A};
                    border-radius: 8px;
                    border-left: 3px solid {BORDER_A};
                    border-top: 1px solid #1e4060;
                    border-bottom: 1px solid #1e4060;
                    border-right: 1px solid #1e4060;
                }}
            """)
            self.name_label.setStyleSheet(
                f"color: {TEXT_ACT}; background: transparent; letter-spacing: 1px;"
            )
            self.detail_label.setStyleSheet(
                "color: #a8d8f0; background: transparent;"
            )
        else:
            self.setStyleSheet(f"""
                ShipCard {{
                    background: {BG_CARD};
                    border-radius: 8px;
                    border-left: 2px solid {BORDER};
                    border-top: 1px solid #111e2e;
                    border-bottom: 1px solid #111e2e;
                    border-right: 1px solid #111e2e;
                }}
            """)
            self.name_label.setStyleSheet(
                f"color: {TEXT_PRI}; background: transparent; letter-spacing: 1px;"
            )
            self.detail_label.setStyleSheet(
                f"color: {TEXT_SEC}; background: transparent;"
            )

    def set_active(self, active):
        self.active = active
        self._set_style(active)


class WarshipApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.model = YOLO("best.pt")
        self.cards = {}
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Warship Classification")
        self.setFixedSize(1020, 660)
        self.setStyleSheet(f"QMainWindow {{ background-color: {BG_DEEP}; }}")

        central = QWidget()
        central.setStyleSheet(f"background: {BG_DEEP};")
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Sol panel ──────────────────────────────────────────
        left = QWidget()
        left.setFixedWidth(665)
        left.setStyleSheet(f"background: {BG_DEEP};")
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(30, 28, 20, 28)
        left_layout.setSpacing(18)

        # Header
        header = QWidget()
        header.setFixedHeight(68)
        header.setStyleSheet("""
            background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                stop:0 #0d1a2e, stop:0.6 #101c30, stop:1 #0d1a2e);
            border-radius: 12px;
            border: 1px solid #162030;
        """)
        hl = QHBoxLayout(header)
        hl.setContentsMargins(18, 0, 18, 0)

        anchor = QLabel("⚓")
        anchor_font = QFont()
        anchor_font.setFamilies(["Segoe UI Emoji", "Noto Color Emoji", "Apple Color Emoji"])
        anchor_font.setPointSize(22)
        anchor.setFont(anchor_font)
        anchor.setStyleSheet(f"color: {ACCENT}; background: transparent;")
        anchor.setFixedWidth(40)

        tc = QVBoxLayout()
        tc.setSpacing(2)

        title_font = QFont()
        title_font.setFamilies(["JetBrains Mono", "Cascadia Code", "Fira Code", "Consolas"])
        title_font.setPointSize(14)
        title_font.setBold(True)

        sub_font = QFont()
        sub_font.setFamilies(["JetBrains Mono", "Cascadia Code", "Fira Code", "Consolas"])
        sub_font.setPointSize(8)

        t1 = QLabel("WARSHIP CLASSIFICATION")
        t1.setFont(title_font)
        t1.setStyleSheet(f"color: {TEXT_PRI}; background: transparent; letter-spacing: 2px;")

        t2 = QLabel("Naval Vessel Recognition System")
        t2.setFont(sub_font)
        t2.setStyleSheet("color: #4a8aaa; background: transparent; letter-spacing: 1px;")

        tc.addWidget(t1)
        tc.addWidget(t2)

        self.dot = QLabel("●")
        self.dot.setFont(QFont("Arial", 12))
        self.dot.setStyleSheet(f"color: {GREEN}; background: transparent;")

        rdy = QLabel("READY")
        rdy_font = QFont()
        rdy_font.setFamilies(["JetBrains Mono", "Cascadia Code", "Fira Code", "Consolas"])
        rdy_font.setPointSize(8)
        rdy_font.setBold(True)
        rdy.setFont(rdy_font)
        rdy.setStyleSheet(f"color: {GREEN}; background: transparent; letter-spacing: 1px;")

        hl.addWidget(anchor)
        hl.addLayout(tc)
        hl.addStretch()
        hl.addWidget(self.dot)
        hl.addSpacing(6)
        hl.addWidget(rdy)
        left_layout.addWidget(header)

        # Görüntü alanı
        img_wrap = QWidget()
        img_wrap.setStyleSheet("""
            background: #080e18;
            border-radius: 12px;
            border: 1px solid #111e2e;
        """)
        iw_layout = QVBoxLayout(img_wrap)
        iw_layout.setContentsMargins(8, 8, 8, 8)

        placeholder_font = QFont()
        placeholder_font.setFamilies(["JetBrains Mono", "Cascadia Code", "Fira Code", "Consolas"])
        placeholder_font.setPointSize(10)

        self.image_label = QLabel("Select an image to analyze")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedHeight(320)
        self.image_label.setFont(placeholder_font)
        self.image_label.setStyleSheet("""
            color: #2a5a7a;
            border: 1px dashed #1a3550;
            border-radius: 8px;
            letter-spacing: 1px;
        """)
        iw_layout.addWidget(self.image_label)
        left_layout.addWidget(img_wrap)

        # Sonuç kutusu
        res = QWidget()
        res.setFixedHeight(60)
        res.setStyleSheet("""
            background: #080e18;
            border-radius: 10px;
            border: 1px solid #111e2e;
        """)
        rl = QHBoxLayout(res)
        rl.setContentsMargins(20, 0, 20, 0)

        self.res_icon = QLabel("◈")
        self.res_icon.setFont(QFont("Arial", 16))
        self.res_icon.setStyleSheet("color: #1a3a5a; background: transparent;")
        self.res_icon.setFixedWidth(30)

        res_font = QFont()
        res_font.setFamilies(["JetBrains Mono", "Cascadia Code", "Fira Code", "Consolas"])
        res_font.setPointSize(12)
        res_font.setBold(True)

        conf_font = QFont()
        conf_font.setFamilies(["JetBrains Mono", "Cascadia Code", "Fira Code", "Consolas"])
        conf_font.setPointSize(11)

        self.res_label = QLabel("Awaiting analysis...")
        self.res_label.setFont(res_font)
        self.res_label.setStyleSheet("color: #2a5a7a; background: transparent; letter-spacing: 1px;")

        self.conf_label = QLabel("")
        self.conf_label.setFont(conf_font)
        self.conf_label.setStyleSheet("color: #1a3a5a; background: transparent;")
        self.conf_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        rl.addWidget(self.res_icon)
        rl.addWidget(self.res_label)
        rl.addStretch()
        rl.addWidget(self.conf_label)
        left_layout.addWidget(res)

        # Buton
        btn_font = QFont()
        btn_font.setFamilies(["JetBrains Mono", "Cascadia Code", "Fira Code", "Consolas"])
        btn_font.setPointSize(11)
        btn_font.setBold(True)

        btn = QPushButton("⬡  SELECT IMAGE")
        btn.setFixedHeight(50)
        btn.setFont(btn_font)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #0a3060, stop:1 #0d4080);
                color: #c8e8ff;
                border-radius: 10px;
                border: 1px solid #1a5090;
                letter-spacing: 3px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #0d4080, stop:1 #1060a0);
                border: 1px solid #4fc3f7;
                color: #ffffff;
            }
            QPushButton:pressed { background: #061830; }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(10, 50, 100, 200))
        shadow.setOffset(0, 4)
        btn.setGraphicsEffect(shadow)
        btn.clicked.connect(self.select_image)
        left_layout.addWidget(btn)

        root.addWidget(left)

        # ── Sağ panel ─────────────────────────────────────────
        right = QWidget()
        right.setStyleSheet(f"""
            background: {BG_PANEL};
            border-left: 1px solid #0f1e30;
        """)
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(14, 24, 14, 20)
        right_layout.setSpacing(10)

        panel_title_font = QFont()
        panel_title_font.setFamilies(["JetBrains Mono", "Cascadia Code", "Fira Code", "Consolas"])
        panel_title_font.setPointSize(10)
        panel_title_font.setBold(True)

        panel_title = QLabel("VESSEL DATABASE")
        panel_title.setFont(panel_title_font)
        panel_title.setStyleSheet(
            "color: #7ab8d4; letter-spacing: 3px; background: transparent;"
        )
        right_layout.addWidget(panel_title)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFixedHeight(1)
        line.setStyleSheet("background: #1a3550; border: none;")
        right_layout.addWidget(line)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{ border: none; background: transparent; }}
            QScrollBar:vertical {{
                background: {BG_PANEL};
                width: 5px;
                border-radius: 2px;
            }}
            QScrollBar::handle:vertical {{
                background: #2a5070;
                border-radius: 2px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {ACCENT};
            }}
        """)

        cards_widget = QWidget()
        cards_widget.setStyleSheet("background: transparent;")
        cards_layout = QVBoxLayout(cards_widget)
        cards_layout.setContentsMargins(0, 0, 4, 0)
        cards_layout.setSpacing(5)

        for data in WARSHIP_DATA:
            card = ShipCard(data)
            self.cards[data["name"]] = card
            cards_layout.addWidget(card)

        cards_layout.addStretch()
        scroll.setWidget(cards_widget)
        right_layout.addWidget(scroll)

        count_font = QFont()
        count_font.setFamilies(["JetBrains Mono", "Cascadia Code", "Fira Code", "Consolas"])
        count_font.setPointSize(9)

        count_label = QLabel(f"{len(WARSHIP_DATA)} vessel classes")
        count_label.setFont(count_font)
        count_label.setStyleSheet("color: #4a8aaa; background: transparent;")
        count_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(count_label)

        root.addWidget(right)

    def select_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "",
            "Images (*.png *.jpg *.jpeg)"
        )
        if not path:
            return

        pixmap = QPixmap(path).scaled(
            640, 312, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.image_label.setStyleSheet("border: 1px solid #1a3550; border-radius: 8px;")
        self.image_label.setPixmap(pixmap)

        results = self.model.predict(path, verbose=False)
        probs = results[0].probs
        top_class = results[0].names[probs.top1]
        confidence = probs.top1conf.item() * 100

        for card in self.cards.values():
            card.set_active(False)

        if top_class in self.cards:
            self.cards[top_class].set_active(True)

        if top_class == "bilinmeyen" or confidence < 60:
            self.res_icon.setStyleSheet(f"color: {RED}; background: transparent;")
            self.res_label.setStyleSheet(
                f"color: {RED}; background: transparent; letter-spacing: 1px;"
            )
            self.res_label.setText("Unidentified Vessel")
            self.conf_label.setText(f"{confidence:.1f}%")
            self.conf_label.setStyleSheet("color: #b71c1c; background: transparent;")
        else:
            data = next((d for d in WARSHIP_DATA if d["name"] == top_class), None)
            code = data["code"] if data else "??"
            self.res_icon.setStyleSheet(f"color: {ACCENT}; background: transparent;")
            self.res_label.setStyleSheet(
                f"color: {TEXT_PRI}; background: transparent; letter-spacing: 1px;"
            )
            self.res_label.setText(f"[{code}]  {top_class}")
            self.conf_label.setText(f"{confidence:.1f}%")
            self.conf_label.setStyleSheet(
                f"color: {GREEN}; background: transparent; font-weight: bold;"
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(6, 13, 22))
    app.setPalette(palette)
    window = WarshipApp()
    window.show()
    sys.exit(app.exec_())