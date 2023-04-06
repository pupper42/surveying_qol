import math
import numpy as np

class Angle:
    def __init__(self, angle, angle_format):
        if angle_format == "dms":
            self.dms = angle
            self.d = None
            self.m = None
            self.s = None
            self.decimal = None
            self.radians = None
            self.autocad = None
            self.parse_dms()
        elif angle_format == "decimal":
            self.decimal = angle
            self.d = None
            self.m = None
            self.s = None
            self.dms = None
            self.radians = None
            self.autocad = None
            self.parse_decimal()

    def parse_decimal(self):
            total_seconds = self.decimal * 3600

            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.d = int(hours)
            self.m = int(minutes)
            self.s = int(seconds)
            self.dms = float(f"{self.d}.{self.m:02d}{self.s:02d}")
            self.parse_dms()
            
    def parse_dms(self):
        dms_split = math.modf(self.dms)

        ms = str(round(dms_split[0],4)) + "0000"

        self.d = int(float(dms_split[1]))
        self.m = int(ms[2:4])
        self.s = int(ms[4:6])

        self.decimal = self.d + self.m/60 + self.s/3600
        self.radians = math.radians(self.decimal)
        self.autocad = f"{self.d}^{self.m:02d}'" if self.s == "00" else f"{self.d:02d}^{self.m:02d}'{self.s:02d}\""

    def __str__(self):
        return f"{self.d}d{self.m:02d}'" if self.s == "00" else f"{self.d}d{self.m:02d}'{self.s:02d}\""
    
class Vector:
    def __init__(self, r_x, theta_y, vector_format):
        
        if vector_format == "polar":
            self.magnitude = r_x
            self.angle = theta_y

            self.easting = None
            self.northing = None

            self.make_polar_vector()

        elif vector_format == "cartesian":
            self.easting = r_x
            self.northing = theta_y

            self.magnitude = None
            self.angle = None            

            self.make_cartesian_vector()

    def make_polar_vector(self):
        print(self.angle)
        self.easting = self.magnitude * math.sin(self.angle.radians)
        self.northing = self.magnitude * math.cos(self.angle.radians)

    def make_cartesian_vector(self):
        if self.northing == 0:
            self.angle == Angle(0, "decimal")
        else:
            self.angle = Angle((math.degrees(np.arctan(self.easting/self.northing)) + 360) % 360, "decimal")
        self.magnitude = np.linalg.norm((self.easting, self.northing))

    def __add__(self, other):
        dE = self.easting + other.easting
        dN = self.northing + other.northing
        return Vector(dE, dN, "cartesian")

    def __sub__(self, other):
        dE = self.easting - other.easting
        dN = self.northing - other.easting
        return Vector(dE, dN, "cartesian")
    
    def __str__(self):
        return f"{self.easting}E {self.northing}N"


    
