# aerial_controller.py
import time
import math

class AerialController:
    """
    GERÇEK Mission Planner SITL bağlantısı için drone kontrolcüsü
    """
    
    def __init__(self, connection_string='tcp:127.0.0.1:5762'):
        #eğer drone bağlanmaz ise 5762 yerine 5760 dene !!!!!!!!!!!!!!!
        self.connection_string = connection_string
        self.vehicle = None
        self._use_real_dronekit = False
        
        # Önce gerçek dronekit'i dene
        try:
            from dronekit import connect, VehicleMode, LocationGlobalRelative
            self.dronekit = connect
            self.VehicleMode = VehicleMode
            self.LocationGlobalRelative = LocationGlobalRelative
            self._use_real_dronekit = True
            self._connect_to_sitl()
        except ImportError:
            # DroneKit yoksa simülasyon moduna geç
            print("⚠️  DroneKit bulunamadı. Simülasyon modu aktif.")
            self._init_simulation()
        except Exception as e:
            print(f"⚠️  SITL bağlantı hatası: {e}. Simülasyon modu aktif.")
            self._init_simulation()
    
    def _connect_to_sitl(self):
        """Gerçek SITL'e bağlan"""
        try:
            print(f"🔗 SITL'e bağlanıyor: {self.connection_string}")
            self.vehicle = self.dronekit(self.connection_string, wait_ready=True, timeout=10)
            print("✅ GERÇEK SITL BAĞLANTISI BAŞARILI!")
            
            # ARM kontrolü
            if not self.vehicle.armed:
                print("🚀 Drone ARM ediliyor...")
                self.vehicle.armed = True
                while not self.vehicle.armed:
                    time.sleep(0.5)
                print("✅ Drone ARM edildi!")
                
        except Exception as e:
            print(f"❌ SITL bağlantı hatası: {e}")
            self._init_simulation()
    
    def _init_simulation(self):
        """SITL bağlantısı yoksa simülasyon başlat"""
        self.vehicle = True  # Simüle bağlantı
        self._lat = 0.000
        self._lon = 0.000
        self._alt = 100.0
        self._airspeed = 0.0
        self._mode = "GUIDED"
        self._armed = True
        self._target_lat = self._lat
        self._target_lon = self._lon
        self._speed_m_s = 15.0
        
        print("🎮 SİMÜLASYON MODU AKTİF")
        print("✅ Drone ARM edildi")
    
    def get_telemetry(self):
        """Telemetri verilerini al"""
        if not self.vehicle:
            return None
        
        if self._use_real_dronekit and self.vehicle:
            # GERÇEK SITL telemetrisi
            try:
                return {
                    "lat": self.vehicle.location.global_frame.lat,
                    "lon": self.vehicle.location.global_frame.lon,
                    "alt": self.vehicle.location.global_relative_frame.alt,
                    "airspeed": self.vehicle.airspeed if self.vehicle.airspeed else 0.0,
                    "mode": self.vehicle.mode.name,
                    "armed": self.vehicle.armed
                }
            except:
                return None
        else:
            # SİMÜLASYON telemetrisi
            self._simulate_movement()
            return {
                "lat": self._lat,
                "lon": self._lon,
                "alt": self._alt,
                "airspeed": self._airspeed,
                "mode": self._mode,
                "armed": self._armed
            }
    
    def send_goto_command(self, lat, lon, alt=30):
        """GUIDED + GOTO komutu"""
        if not self.vehicle:
            return False
        
        if self._use_real_dronekit and self.vehicle:
            # GERÇEK SITL komutu
            try:
                self.vehicle.mode = self.VehicleMode("GUIDED")
                time.sleep(0.5)
                target = self.LocationGlobalRelative(lat, lon, alt)
                self.vehicle.simple_goto(target)
                print(f"✅ GERÇEK GOTO: {lat:.6f}, {lon:.6f}")
                return True
            except Exception as e:
                print(f"❌ GOTO hatası: {e}")
                return False
        else:
            # SİMÜLASYON komutu
            self._mode = "GUIDED"
            self._target_lat = lat
            self._target_lon = lon
            self._airspeed = self._speed_m_s
            print(f"✅ SİMÜLASYON GOTO: {lat:.6f}, {lon:.6f}")
            return True
    
    def set_auto_mode(self):
        """AUTO modu"""
        if not self.vehicle:
            return False
        
        if self._use_real_dronekit and self.vehicle:
            # GERÇEK SITL komutu
            try:
                self.vehicle.mode = self.VehicleMode("AUTO")
                print("✅ GERÇEK AUTO modu")
                return True
            except Exception as e:
                print(f"❌ AUTO hatası: {e}")
                return False
        else:
            # SİMÜLASYON komutu
            self._mode = "AUTO"
            self._airspeed = 12.0
            print("✅ SİMÜLASYON AUTO modu (RTL benzeri)")
            return True
    
    def _simulate_movement(self):
        """Simülasyon hareketi"""
        if self._mode == "GUIDED" and self._airspeed > 0:
            distance = self._haversine_distance(self._lat, self._lon, self._target_lat, self._target_lon)
            
            if distance > 5.0:
                bearing = self._calculate_bearing(self._lat, self._lon, self._target_lat, self._target_lon)
                step_distance = min(self._airspeed * 1.0, distance)
                
                new_lat, new_lon = self._calculate_new_position(self._lat, self._lon, bearing, step_distance)
                self._lat = new_lat
                self._lon = new_lon
            else:
                self._airspeed = 0.0
        
        elif self._mode == "AUTO" and self._airspeed > 0:
            # RTL benzeri davranış
            home_lat, home_lon = 40.2338, 29.0096
            distance = self._haversine_distance(self._lat, self._lon, home_lat, home_lon)
            
            if distance > 10.0:
                bearing = self._calculate_bearing(self._lat, self._lon, home_lat, home_lon)
                step_distance = min(self._airspeed * 1.0, distance)
                
                new_lat, new_lon = self._calculate_new_position(self._lat, self._lon, bearing, step_distance)
                self._lat = new_lat
                self._lon = new_lon
            else:
                self._airspeed = 0.0
    
    def _haversine_distance(self, lat1, lon1, lat2, lon2):
        """Mesafe hesaplama"""
        R = 6371000
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        
        a = math.sin(delta_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(delta_lambda/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c
    
    def _calculate_bearing(self, lat1, lon1, lat2, lon2):
        """Yön hesaplama"""
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        lambda1 = math.radians(lon1)
        lambda2 = math.radians(lon2)
        
        y = math.sin(lambda2 - lambda1) * math.cos(phi2)
        x = math.cos(phi1)*math.sin(phi2) - math.sin(phi1)*math.cos(phi2)*math.cos(lambda2 - lambda1)
        return math.atan2(y, x)
    
    def _calculate_new_position(self, lat, lon, bearing, distance):
        """Yeni konum hesaplama"""
        R = 6371000
        phi = math.radians(lat)
        lambda_val = math.radians(lon)
        angular_distance = distance / R
        
        new_phi = math.asin(math.sin(phi)*math.cos(angular_distance) + 
                           math.cos(phi)*math.sin(angular_distance)*math.cos(bearing))
        new_lambda = lambda_val + math.atan2(math.sin(bearing)*math.sin(angular_distance)*math.cos(phi),
                                           math.cos(angular_distance) - math.sin(phi)*math.sin(new_phi))
        return math.degrees(new_phi), math.degrees(new_lambda)
    
    def close_connection(self):
        """Bağlantıyı kapat"""
        if self._use_real_dronekit and self.vehicle:
            self.vehicle.close()
        print("🔴 Bağlantı kapatıldı")


