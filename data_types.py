import math

degree_sign = u"\u00b0"

class Angle:
    def __init__(self, angle: float, angle_format: str):
        """Angle format can be 'dms' or 'deg'"""
        if angle_format == "dms":
            self.dms = angle
            self.d = None
            self.m = None
            self.s = None
            self.deg = None
            self.radians = None
            self.autocad = None
            self.text = None
            self.parse_dms()
        elif angle_format == "deg":
            self.deg = angle
            self.d = None
            self.m = None
            self.s = None
            self.dms = None
            self.radians = None
            self.autocad = None
            self.text = None
            self.parse_deg()

    def parse_deg(self):
            total_seconds = self.deg * 3600

            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            self.d = int(hours)
            self.m = int(minutes)
            self.s = int(seconds)

            self.dms = float(f"{self.d}.{self.m:02d}{self.s:02d}")
            self.radians = math.radians(self.deg)
            self.autocad = f"{self.d}^{self.m:02d}'" if self.s == 0 else f"{self.d:02d}^{self.m:02d}'{self.s:02d}\""
            self.text = f"{self.d}{degree_sign}{self.m:02d}'" if self.s == 0 else f"{self.d:02d}{degree_sign}{self.m:02d}'{self.s:02d}\""
            
    def parse_dms(self):
        dms_split = math.modf(self.dms)

        ms = str(round(dms_split[0],4)) + "0000"

        self.d = int(float(dms_split[1]))
        self.m = int(ms[2:4])
        self.s = int(ms[4:6])

        self.deg = self.d + self.m/60 + self.s/3600
        self.radians = math.radians(self.deg)
        self.autocad = f"{self.d}^{self.m:02d}'" if self.s == 0 else f"{self.d:02d}^{self.m:02d}'{self.s:02d}\""
        self.text = f"{self.d}{degree_sign}{self.m:02d}'" if self.s == 0 else f"{self.d:02d}{degree_sign}{self.m:02d}'{self.s:02d}\""

    def __add__(self, other):
        return Angle(self.deg + other.deg, 'deg')
    
    def __sub__(self, other):
        return Angle(self.deg - other.deg, 'deg')
        
    def __str__(self):
        return self.text
    
    
class Vector:
    def __init__(self, r_x: float, theta_y: float or Angle, vector_format: str):
        """If the vector format is 'polar' then input magnitude and an angle
        
        Otherwise if it's 'cartesian' then input easting and northing"""
        if vector_format == "polar":
            self.magnitude = r_x
            self.angle = theta_y

            self.easting = None
            self.northing = None

            self.mid_e = None
            self.mid_n = None

            self.make_polar_vector()

        elif vector_format == "cartesian":
            self.easting = r_x
            self.northing = theta_y

            self.magnitude = None
            self.angle = None

            self.mid_e = None
            self.mid_n = None         

            self.make_cartesian_vector()

    def make_polar_vector(self):
        self.easting = self.magnitude * math.sin(self.angle.radians)
        self.northing = self.magnitude * math.cos(self.angle.radians)

    def make_cartesian_vector(self):
        if self.northing == 0:
            self.angle == Angle(0, "deg")
        else:
            self.angle = Angle((math.degrees(math.atan(self.easting/self.northing)) + 360) % 360, "deg")
        self.magnitude = math.sqrt(self.easting**2 + self.northing**2)


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
    
    def __mul__(self, other):
        rE = self.easting * other
        rN = self.northing * other
        return Vector(rE, rN, "cartesian")
    
    def __str__(self):
        return f"{self.angle} {self.magnitude}"



    
