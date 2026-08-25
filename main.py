"""
ALEXA Voice Assistant - Desktop App
EXACT MATCH to HTML web version

SETUP:
1. Save as alexa_ui.py (same folder as main.py)
2. pip install PySide6
3. python alexa_ui.py
4. Click mic → starts main.py, click again → stops main.py
"""

import sys
import subprocess
import os
import signal
import math
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QLabel, QPushButton, QStackedWidget
)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRectF, QPointF
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QRadialGradient,QLinearGradient


class AnimatedBackground(QWidget):
    """Animated background with floating orbs - matches HTML"""
    def __init__(self):
        super().__init__()
        self.orb1_x = -200
        self.orb1_y = -200
        self.orb2_x = 0
        self.orb2_y = 0
        self.orb3_x = 0
        self.orb3_y = 0
        self.gradient_offset = 0
        
        # Animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self._animate)
        self.timer.start(50)
        
        self.time = 0
    
    def _animate(self):
        """Animate floating orbs and gradient"""
        self.time += 0.05
        
        # Orb 1 movement (top-left)
        self.orb1_x = -200 + math.sin(self.time * 0.5) * 50
        self.orb1_y = -200 + math.cos(self.time * 0.3) * 50
        
        # Orb 2 movement (bottom-right)
        self.orb2_x = math.sin(self.time * 0.3 + 2) * 30
        self.orb2_y = math.cos(self.time * 0.4 + 2) * 30
        
        # Orb 3 movement (right side)
        self.orb3_x = math.sin(self.time * 0.4 + 4) * 50
        self.orb3_y = math.cos(self.time * 0.5 + 4) * 30
        
        # Gradient shift
        self.gradient_offset = (self.gradient_offset + 0.2) % 100
        
        self.update()
    
    def paintEvent(self, event):
        """Draw animated background"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Animated gradient background
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        
        # Shift colors based on animation
        offset = self.gradient_offset / 100
        gradient.setColorAt(0, QColor(0, 0, 0))
        gradient.setColorAt(0.25 + offset * 0.1, QColor(10, 10, 10))
        gradient.setColorAt(0.5 + offset * 0.1, QColor(26, 26, 26))
        gradient.setColorAt(0.75 + offset * 0.1, QColor(10, 10, 10))
        gradient.setColorAt(1, QColor(0, 0, 0))
        
        painter.fillRect(self.rect(), gradient)
        
        # Draw floating orbs (blurred circles)
        painter.setOpacity(0.1)
        
        # Orb 1 (top-left, 400px)
        self._draw_blurred_orb(painter, self.orb1_x, self.orb1_y, 400)
        
        # Orb 2 (bottom-right, 300px)
        orb2_x = self.width() - 150 + self.orb2_x
        orb2_y = self.height() - 150 + self.orb2_y
        self._draw_blurred_orb(painter, orb2_x, orb2_y, 300)
        
        # Orb 3 (right side, 350px)
        orb3_x = self.width() - 175 + self.orb3_x
        orb3_y = self.height() // 2 + self.orb3_y
        self._draw_blurred_orb(painter, orb3_x, orb3_y, 350)
        
        painter.setOpacity(1.0)
    
    def _draw_blurred_orb(self, painter, x, y, size):
        """Draw a blurred orb (simulates blur filter)"""
        gradient = QRadialGradient(x, y, size / 2)
        gradient.setColorAt(0, QColor(255, 255, 255, 25))
        gradient.setColorAt(0.5, QColor(255, 255, 255, 10))
        gradient.setColorAt(1, QColor(255, 255, 255, 0))
        
        painter.setBrush(gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPointF(x, y), size / 2, size / 2)


class BackendRunner:
    """Runs your main.py"""
    def __init__(self, script_path="main.py"):
        self.script_path = script_path
        self.process = None
        self.is_running = False
    
    def start(self):
        if self.is_running: return
        try:
            print(f" Starting {self.script_path}...")
            self.process = subprocess.Popen(
                [sys.executable, self.script_path],
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0
            )
            self.is_running = True
            print(f" Running")
        except Exception as e:
            print(f"❌ Error: {e}")
            self.is_running = False
    
    def stop(self):
        if not self.is_running or not self.process: return
        try:
            print(f" Stopping...")
            if sys.platform == "win32":
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(self.process.pid)],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            self.process.wait(timeout=2)
            self.is_running = False
            self.process = None
            print("✅ Stopped")
        except:
            if self.process: self.process.kill()
            self.is_running = False
            self.process = None


class MicrophoneButton(QWidget):
    """Custom microphone button - matches HTML exactly"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(180, 180)
        self.is_listening = False
        self.glow_opacity = 0
        self.glow_scale = 0.8
        self.glow_timer = QTimer()
        self.glow_timer.timeout.connect(self._update_glow)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
    
    def set_listening(self, listening):
        self.is_listening = listening
        if listening:
            self.glow_timer.start(50)
        else:
            self.glow_timer.stop()
            self.glow_opacity = 0
            self.glow_scale = 0.8
        self.update()
    
    def _update_glow(self):
        """Pulsing glow animation"""
        self.glow_scale += 0.02
        if self.glow_scale > 1.4:
            self.glow_scale = 0.8
            self.glow_opacity = 0
        else:
            progress = (self.glow_scale - 0.8) / 0.6
            self.glow_opacity = math.sin(progress * math.pi)
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        center = QPointF(90, 90)
        
        # Glow ring
        if self.is_listening and self.glow_opacity > 0:
            glow_radius = 90 * self.glow_scale
            gradient = QRadialGradient(center, glow_radius)
            color = QColor(255, 255, 255)
            color.setAlphaF(self.glow_opacity * 0.2)
            gradient.setColorAt(0, color)
            color.setAlphaF(0)
            gradient.setColorAt(0.7, color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(gradient)
            painter.drawEllipse(center, glow_radius, glow_radius)
        
        # Button circle
        if self.is_listening:
            painter.setBrush(QColor(255, 255, 255, 26))
            painter.setPen(QPen(QColor(255, 255, 255, 77), 2))
        else:
            painter.setBrush(QColor(255, 255, 255, 13))
            painter.setPen(QPen(QColor(255, 255, 255, 26), 2))
        painter.drawEllipse(QRectF(0, 0, 180, 180))
        
        # Microphone icon
        icon_color = QColor(255, 255, 255) if self.is_listening else QColor(136, 136, 136)
        painter.setPen(QPen(icon_color, 3))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        
        # Capsule
        painter.drawRoundedRect(73, 70, 34, 40, 17, 17)
        # Stand
        painter.drawLine(90, 110, 90, 124)
        # Base
        painter.drawLine(76, 124, 104, 124)
        
        # Sound waves
        if self.is_listening:
            wave_color = QColor(icon_color)
            wave_color.setAlpha(153)
            painter.setPen(QPen(wave_color, 2))
            painter.drawArc(40, 73, 24, 36, 30*16, 120*16)
            painter.drawArc(34, 68, 30, 46, 30*16, 120*16)
            painter.drawArc(116, 73, 24, 36, 30*16, 120*16)
            painter.drawArc(122, 68, 30, 46, 30*16, 120*16)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Find MainWindow parent
            parent = self.parent()
            while parent and not isinstance(parent, MainWindow):
                parent = parent.parent()
            if parent:
                parent._on_mic_clicked()


class SplashScreen(QWidget):
    """Splash screen - matches HTML"""
    def __init__(self):
        super().__init__()
        self.circle_rotation = 0
        self.mic_opacity = 0
        self.text_opacity = 0
        self.loading_progress = 0
        self.animation_time = 0
        
        # Black background
        self.setStyleSheet("QWidget { background: #000000; }")
        
        self.timer = QTimer()
        self.timer.timeout.connect(self._update)
        self.timer.start(16)
    
    def _update(self):
        self.animation_time += 16
        
        # Circles always rotating (start at 0.8s)
        if self.animation_time > 800:
            self.circle_rotation += 2
        
        # Mic fades in at 0.3s
        if 300 < self.animation_time < 800:
            self.mic_opacity = min(1.0, (self.animation_time - 300) / 500)
        elif self.animation_time >= 800:
            self.mic_opacity = 1.0
        
        # Text fades in at 0.5s
        if 500 < self.animation_time < 1200:
            self.text_opacity = min(1.0, (self.animation_time - 500) / 700)
        elif self.animation_time >= 1200:
            self.text_opacity = 1.0
        
        # Loading bar at 0.9s, completes in 2s
        if 900 < self.animation_time < 2900:
            self.loading_progress = min(100, ((self.animation_time - 900) / 2000) * 100)
        elif self.animation_time >= 2900:
            self.loading_progress = 100
        
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor(0, 0, 0))
        
        # Dynamic center based on window size
        center = QPointF(self.width() / 2, self.height() / 2 - 50)
        
        # Calculate circle opacity (fade in from 0.8s to 1.8s)
        circle_opacity = 0.0
        if self.animation_time > 800:
            if self.animation_time < 1800:
                circle_opacity = min(1.0, (self.animation_time - 800) / 1000)
            else:
                circle_opacity = 1.0
        
        # Draw rotating circles with GAPS (incomplete circles like HTML)
        if circle_opacity > 0:
            painter.setOpacity(circle_opacity)
            
            # Outer circle (white, rotates forward) - 270° arc (gap at top)
            painter.save()
            painter.translate(center)
            painter.rotate(self.circle_rotation)
            painter.translate(-center)
            painter.setPen(QPen(QColor(255, 255, 255), 3, Qt.PenStyle.SolidLine))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            # Draw 270° arc (leaving 90° gap at top)
            rect = QRectF(center.x() - 110, center.y() - 110, 220, 220)
            painter.drawArc(rect, 90 * 16, 270 * 16)  # Start at 90°, span 270°
            painter.restore()
            
            # Middle circle (gray, rotates reverse) - 270° arc (gap at bottom)
            painter.save()
            painter.translate(center)
            painter.rotate(-self.circle_rotation * 1.3)
            painter.translate(-center)
            painter.setPen(QPen(QColor(204, 204, 204), 3, Qt.PenStyle.SolidLine))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            # Draw 270° arc (leaving 90° gap at bottom)
            rect = QRectF(center.x() - 80, center.y() - 80, 160, 160)
            painter.drawArc(rect, 180 * 16, 270 * 16)  # Start at 180°, span 270°
            painter.restore()
            
            # Inner circle (light gray, rotates fast forward) - 270° arc (gap at top)
            painter.save()
            painter.translate(center)
            painter.rotate(self.circle_rotation * 2)
            painter.translate(-center)
            painter.setPen(QPen(QColor(153, 153, 153), 3, Qt.PenStyle.SolidLine))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            # Draw 270° arc (leaving 90° gap at top)
            rect = QRectF(center.x() - 50, center.y() - 50, 100, 100)
            painter.drawArc(rect, 90 * 16, 270 * 16)  # Start at 90°, span 270°
            painter.restore()
            
            painter.setOpacity(1.0)
        
        # Draw microphone icon (fades in at 0.3s)
        if self.mic_opacity > 0:
            painter.setOpacity(self.mic_opacity)
            painter.setPen(QPen(QColor(255, 255, 255), 3))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            
            # Capsule (centered)
            mic_x = center.x() - 14
            mic_y = center.y() - 16
            painter.drawRoundedRect(mic_x, mic_y, 28, 32, 14, 14)
            # Stand
            painter.drawLine(center.x(), center.y() + 16, center.x(), center.y() + 30)
            # Base
            painter.drawLine(center.x() - 11, center.y() + 30, center.x() + 11, center.y() + 30)
            painter.setOpacity(1.0)
        
        # Draw "ALEXA" text (fades in at 0.5s)
        if self.text_opacity > 0:
            painter.setOpacity(self.text_opacity)
            
            # "ALEXA" title
            painter.setPen(QColor(255, 255, 255))
            font = QFont("Segoe UI", 48, QFont.Weight.Light)
            font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 8)
            painter.setFont(font)
            text_y = center.y() + 120
            painter.drawText(QRectF(0, text_y, self.width(), 80), Qt.AlignmentFlag.AlignCenter, "ALEXA")
            
            # "VOICE ASSISTANT" subtitle
            painter.setPen(QColor(102, 102, 102))
            font = QFont("Segoe UI", 14, QFont.Weight.Light)
            font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 4)
            painter.setFont(font)
            subtitle_y = text_y + 70
            painter.drawText(QRectF(0, subtitle_y, self.width(), 30), Qt.AlignmentFlag.AlignCenter, "VOICE ASSISTANT")
            painter.setOpacity(1.0)
        
        # Draw loading bar (appears at 0.9s)
        if self.loading_progress > 0:
            bar_width = min(320, self.width() - 100)
            bar_x = (self.width() - bar_width) / 2
            bar_y = self.height() - 100
            
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(26, 26, 26))
            painter.drawRoundedRect(bar_x, bar_y, bar_width, 3, 2, 2)
            
            # Progress fill
            progress_width = int(bar_width * (self.loading_progress / 100))
            painter.setBrush(QColor(255, 255, 255))
            painter.drawRoundedRect(bar_x, bar_y, progress_width, 3, 2, 2)
            
            # "INITIALIZING SYSTEM..." text
            painter.setPen(QColor(102, 102, 102))
            font = QFont("Segoe UI", 12)
            font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 2)
            painter.setFont(font)
            painter.drawText(QRectF(0, bar_y + 20, self.width(), 30), Qt.AlignmentFlag.AlignCenter, "INITIALIZING SYSTEM...")


class MainWindow(QWidget):
    """Main window - matches HTML with animated background"""
    def __init__(self):
        super().__init__()
        self.backend = BackendRunner("main.py")
        self.is_listening = False
        self._setup_ui()
    
    def _setup_ui(self):
        # Set transparent background for main widget
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Animated background (fills entire widget)
        self.background = AnimatedBackground()
        main_layout.addWidget(self.background)
        
        # Create centered card on top of background
        self.card = QWidget(self)
        self.card.setMinimumSize(600, 700)
        self.card.setMaximumSize(800, 900)
        self.card.setStyleSheet("""
            QWidget {
                background: rgba(20, 20, 20, 180);
                border-radius: 30px;
                border: 1px solid rgba(255, 255, 255, 20);
            }
        """)
        
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(50, 50, 50, 50)
        card_layout.setSpacing(40)
        
        # Header
        header = QHBoxLayout()
        logo_container = QHBoxLayout()
        logo_container.setSpacing(12)
        
        logo_icon = QLabel("🎤")
        logo_icon.setStyleSheet("font-size: 20px; background: transparent; border: none;")
        
        logo_text = QLabel("ALEXA")
        logo_text.setStyleSheet("""
            font-size: 18px;
            color: #ffffff;
            font-weight: 300;
            letter-spacing: 2px;
            background: transparent;
            border: none;
        """)
        
        logo_container.addWidget(logo_icon)
        logo_container.addWidget(logo_text)
        header.addLayout(logo_container)
        header.addStretch()
        card_layout.addLayout(header)
        
        card_layout.addStretch(1)
        
        # Status
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            font-size: 32px;
            color: #cccccc;
            font-weight: 200;
            letter-spacing: 2px;
            background: transparent;
            border: none;
        """)
        card_layout.addWidget(self.status_label)
        
        self.subtitle_label = QLabel("Click microphone to activate")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label.setStyleSheet("""
            font-size: 14px;
            color: #666666;
            font-weight: 300;
            letter-spacing: 1px;
            background: transparent;
            border: none;
        """)
        card_layout.addWidget(self.subtitle_label)
        
        # Mic button
        mic_container = QWidget()
        mic_container.setStyleSheet("background: transparent; border: none;")
        mic_layout = QHBoxLayout(mic_container)
        mic_layout.setContentsMargins(0, 20, 0, 20)
        
        self.mic_button = MicrophoneButton(self.card)
        mic_layout.addStretch()
        mic_layout.addWidget(self.mic_button)
        mic_layout.addStretch()
        card_layout.addWidget(mic_container)
        
        card_layout.addStretch(2)
        
        # Settings button
        settings_btn = QPushButton("⚙️ Settings")
        settings_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 13);
                border: 1px solid rgba(255, 255, 255, 26);
                color: #888888;
                padding: 12px 24px;
                border-radius: 20px;
                font-size: 13px;
                letter-spacing: 1px;
                text-transform: uppercase;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 20);
                border-color: rgba(255, 255, 255, 51);
                color: #ffffff;
            }
        """)
        
        bottom = QHBoxLayout()
        bottom.addStretch()
        bottom.addWidget(settings_btn)
        card_layout.addLayout(bottom)
        
        # Position card initially
        self._center_card()
    
    def _center_card(self):
        """Center the card on the background"""
        card_width = min(700, self.width() - 100)
        card_height = min(800, self.height() - 100)
        self.card.resize(card_width, card_height)
        
        x = (self.width() - self.card.width()) // 2
        y = (self.height() - self.card.height()) // 2
        self.card.move(x, y)
    
    def resizeEvent(self, event):
        """Reposition card and background when window resizes"""
        super().resizeEvent(event)
        if hasattr(self, 'background'):
            self.background.setGeometry(0, 0, self.width(), self.height())
        if hasattr(self, 'card'):
            self._center_card()
    
    def _on_mic_clicked(self):
        if not self.is_listening:
            print("\n🟢 STARTING main.py")
            self.backend.start()
            self.is_listening = True
            self.mic_button.set_listening(True)
            
            self.status_label.setText("Listening")
            self.status_label.setStyleSheet("""
                font-size: 32px;
                color: #ffffff;
                font-weight: 200;
                letter-spacing: 2px;
                background: transparent;
                border: none;
            """)
            self.subtitle_label.setText("Click again to stop")
        else:
            print("🔴 STOPPING main.py\n")
            self.backend.stop()
            self.is_listening = False
            self.mic_button.set_listening(False)
            
            self.status_label.setText("Ready")
            self.status_label.setStyleSheet("""
                font-size: 32px;
                color: #cccccc;
                font-weight: 200;
                letter-spacing: 2px;
                background: transparent;
                border: none;
            """)
            self.subtitle_label.setText("Click microphone to activate")
    
    def closeEvent(self, event):
        if self.backend.is_running:
            self.backend.stop()
        event.accept()


class AlexaApp(QMainWindow):
    """Main application"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ALEXA")
        
        # Resizable window with minimum size
        self.setMinimumSize(700, 800)
        self.resize(900, 1000)  # Default size
        
        self.setStyleSheet("QMainWindow { background: #000000; }")
        
        # Stacked widget
        self.stacked = QStackedWidget()
        self.setCentralWidget(self.stacked)
        
        self.splash = SplashScreen()
        self.main_window = MainWindow()
        
        self.stacked.addWidget(self.splash)
        self.stacked.addWidget(self.main_window)
        self.stacked.setCurrentWidget(self.splash)
        
        # Fade in
        self.setWindowOpacity(0)
        fade = QPropertyAnimation(self, b"windowOpacity")
        fade.setDuration(500)
        fade.setStartValue(0)
        fade.setEndValue(1)
        fade.start()
        self._fade = fade
        
        # Switch after 3 seconds
        QTimer.singleShot(3000, self._show_main)
    
    def _show_main(self):
        fade_out = QPropertyAnimation(self, b"windowOpacity")
        fade_out.setDuration(400)
        fade_out.setStartValue(1)
        fade_out.setEndValue(0)
        
        def switch():
            self.stacked.setCurrentWidget(self.main_window)
            fade_in = QPropertyAnimation(self, b"windowOpacity")
            fade_in.setDuration(500)
            fade_in.setStartValue(0)
            fade_in.setEndValue(1)
            fade_in.start()
            self._fade_in = fade_in
        
        fade_out.finished.connect(switch)
        fade_out.start()
        self._fade_out = fade_out
    
    def closeEvent(self, event):
        if hasattr(self.main_window, 'backend'):
            if self.main_window.backend.is_running:
                self.main_window.backend.stop()
        event.accept()


if __name__ == "__main__":
    print("\n" + "="*60)
    print("ALEXA VOICE ASSISTANT")
    print("="*60)
    print("\n🎤 Click mic → Runs main.py")
    print("🎤 Click again → Stops main.py\n")
    print("="*60 + "\n")
    
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = AlexaApp()
    window.show()
    sys.exit(app.exec())