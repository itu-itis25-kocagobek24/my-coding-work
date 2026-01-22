# main_app.py
import sys
import math
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGraphicsScene, QGraphicsView,
    QGraphicsLineItem, QMessageBox, QGraphicsEllipseItem
)
from PyQt5.uic import loadUi
from PyQt5.QtCore import QPointF, QTimer, Qt, QLine
from PyQt5.QtGui import QColor, QBrush, QPen

from aerial_controller import AerialController

class MapView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragMode(QGraphicsView.NoDrag)
        self.panning = False
        self.last_mouse_pos = None
        self.center_lat = 0.000
        self.center_lon = 0.000
        self.scale_factor = 1.0
        self.main_window = None

    def set_main_window(self, main_window):
        self.main_window = main_window

    def set_center_coordinates(self, lat, lon):
        self.center_lat = float(lat)
        self.center_lon = float(lon)
        self.centerOn(QPointF(0, 0))

    def draw_grid(self):
        """3km'lik alanda 100m aralıklı ızgara"""
        SCENE_HALF_METERS = 3000
        PIXELS_PER_100M = 100.0
        scene_half_pixels = (SCENE_HALF_METERS / 100.0) * PIXELS_PER_100M
        GRID_SPACING = 100.0

        pen = QPen(QColor(200, 200, 200), 1, Qt.DotLine)

        # Dikey çizgiler
        x = -scene_half_pixels
        while x <= scene_half_pixels:
            line = QGraphicsLineItem(x, -scene_half_pixels, x, scene_half_pixels)
            line.setPen(pen)
            self.scene().addItem(line)
            x += GRID_SPACING

        # Yatay çizgiler
        y = -scene_half_pixels
        while y <= scene_half_pixels:
            line = QGraphicsLineItem(-scene_half_pixels, y, scene_half_pixels, y)
            line.setPen(pen)
            self.scene().addItem(line)
            y += GRID_SPACING

    def wheelEvent(self, event):
        """Zoom"""
        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor
        zoom = zoom_in_factor if event.angleDelta().y() > 0 else zoom_out_factor
        self.scale(zoom, zoom)
        self.scale_factor *= zoom

    def mousePressEvent(self, event):
        """Kontroller"""
        scene_pos = self.mapToScene(event.pos())
        
        PIXELS_PER_100M = 100.0
        dx = scene_pos.x() / PIXELS_PER_100M
        dy = -scene_pos.y() / PIXELS_PER_100M

        clicked_lat = self.center_lat + (dy * 100.0) / 111000.0
        meters_per_deg_lon = 111320.0 * math.cos(math.radians(self.center_lat))
        clicked_lon = self.center_lon + (dx * 100.0) / meters_per_deg_lon

        if event.button() == Qt.LeftButton:
            if self.main_window and hasattr(self.main_window, 'drone_handler'):
                success = self.main_window.drone_handler.send_goto_command(clicked_lat, clicked_lon)
                if success:
                    self.main_window.label_status.setText(f"GUIDED + GOTO: {clicked_lat:.6f}, {clicked_lon:.6f}")

        elif event.button() == Qt.RightButton:
            if self.main_window and hasattr(self.main_window, 'drone_handler'):
                success = self.main_window.drone_handler.set_auto_mode()
                if success:
                    self.main_window.label_status.setText("AUTO moduna alındı")

        elif event.button() == Qt.MidButton:
            self.panning = True
            self.last_mouse_pos = event.pos()
            self.setCursor(Qt.OpenHandCursor)

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.panning and self.last_mouse_pos is not None:
            delta = self.last_mouse_pos - event.pos()
            self.last_mouse_pos = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() + delta.y())
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MidButton and self.panning:
            self.panning = False
            self.setCursor(Qt.ArrowCursor)
            self.last_mouse_pos = None
        super().mouseReleaseEvent(event)

class YkiMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("main_window.ui", self)
        
        self.drone_handler = AerialController()
        self.drone_marker = None
        
        self.setup_map()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_telemetry)
        self.timer.start(1000)
        
        self.update_initial_display()

    def setup_map(self):
        self.scene = QGraphicsScene()
        self.map_view.setScene(self.scene)
        self.map_view.set_main_window(self)
        
        if self.drone_handler.vehicle:
            data = self.drone_handler.get_telemetry()
            if data:
                self.map_view.set_center_coordinates(data["lat"], data["lon"])
                self.map_view.draw_grid()
                
                self.drone_marker = QGraphicsEllipseItem(-8, -8, 16, 16)
                self.drone_marker.setBrush(QBrush(QColor(255, 0, 0)))
                self.drone_marker.setPen(QPen(Qt.black))
                self.drone_marker.setZValue(10)
                self.scene.addItem(self.drone_marker)
        else:
            QMessageBox.warning(self, "Bağlantı Hatası", 
                               "SITL bağlantısı kurulamadı!")

    def update_initial_display(self):
        self.update_telemetry()

    def update_telemetry(self):
        data = self.drone_handler.get_telemetry()
        if not data:
            self.update_status()
            return
        
        self.label_alt.setText(f"{data['alt']:.1f} m")
        self.label_airspeed.setText(f"{data['airspeed']:.1f} m/s")
        self.label_mode.setText(data['mode'])
        self.label_position.setText(f"{data['lat']:.6f}, {data['lon']:.6f}")
        
        pos = self.geo_to_pixel(data["lat"], data["lon"])
        if self.drone_marker:
            self.drone_marker.setPos(pos)
        
        self.update_status()

    def geo_to_pixel(self, lat, lon):
        PIXELS_PER_100M = 100.0
        METERS_PER_DEGREE_LAT = 111000.0
        meters_per_deg_lon = 111320.0 * math.cos(math.radians(self.map_view.center_lat))

        dy_m = (lat - self.map_view.center_lat) * METERS_PER_DEGREE_LAT
        dx_m = (lon - self.map_view.center_lon) * meters_per_deg_lon

        pixel_x = (dx_m / 100.0) * PIXELS_PER_100M
        pixel_y = -(dy_m / 100.0) * PIXELS_PER_100M
        
        return QPointF(pixel_x, pixel_y)

    def update_status(self):
        if self.drone_handler.vehicle:
            data = self.drone_handler.get_telemetry()
            if data:
                if data['armed']:
                    if data.get('airspeed', 0) > 0:
                        status_text = "SİSTEM AKTİF - HAREKET HALİNDE"
                        color = "lightgreen"
                    else:
                        status_text = "SİSTEM AKTİF - HAZIR"
                        color = "lightblue"
                else:
                    status_text = "SİSTEM BAĞLI - ARM EDİLMEMİŞ"
                    color = "yellow"
            else:
                status_text = "SİSTEM BAĞLI - TELEMETRİ ALINAMIYOR"
                color = "orange"
        else:
            status_text = "SİSTEM HATASI - SİMÜLASYON MODU"
            color = "red"
        
        self.label_status.setText(status_text)
        self.label_status.setStyleSheet(f"background-color: {color}; font-weight: bold; padding: 5px;")

    def closeEvent(self, event):
        self.drone_handler.close_connection()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YkiMainWindow()
    window.show()
    sys.exit(app.exec_())
