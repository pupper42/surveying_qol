import numpy as np
import math

def dms_to_rad(dms):
    dms_split = math.modf(dms)

    ms = str(round(dms_split[0],4)) + "0000"

    d = float(str(dms_split[1]))
    m = float(ms[2:4])
    s = float(ms[4:6])

    decimal = d + m/60 + s/3600

    rad = math.radians(decimal)
    return rad

def calc_bearing(easting, northing):
    angle = np.arctan(easting/northing)
    angle_degrees = (math.degrees(angle) + 360) % 360

    total_seconds = angle_degrees * 3600

    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    bearing_dms = str(int(hours)) + "d " + str(int(minutes)) + "m " + str(seconds) + "s"
    return bearing_dms
    
def closure(vectors):
    easting = 0
    northing = 0

    easting_list = [0]
    northing_list = [0]

    for i in range(len(vectors)):
        bearing = vectors[i, 0]
        bearing_rad = dms_to_rad(bearing)
        distance = vectors[i, 1]
        dE = distance * np.sin(bearing_rad)
        dN = distance * np.cos(bearing_rad)


        easting = easting + dE
        northing = northing + dN

        easting_list.append(easting)
        northing_list.append(northing)

        magnitude = np.linalg.norm((easting, northing))

    
    bearing = calc_bearing(easting, northing)

    print("==================")
    print("Number of bearing distances: " + str(len(vectors)))
    print("==================")
    print("Delta E: " + str(easting))
    print("Delta N: " + str(northing))
    print("==================")
    print("Magnitude: " + str(magnitude))
    print("Bearing: " + bearing)
    print("==================")

    return easting_list, northing_list

def gen_scr(easting_list, northing_list, vectors):
    path = "scr/" + "script" + ".scr"

    easting_list = [str(x) for x in easting_list]
    northing_list = [str(x) for x in northing_list]
    coordinates = []
    midpoints = []

    for i in range(len(easting_list)):
        coordinates.append(easting_list[i] + "," + northing_list[i])

    line = "pline " + " ".join(coordinates) + "\n"
    f = open(path, "w")
    

    for i in range(len(easting_list) - 1):
        start = (easting_list[i] + "," + northing_list[i])
        height = "0.875"
        bearing = vectors[i, 0]
        distance = vectors[i, 1]

        bearing_decimal = math.degrees(dms_to_rad(bearing))
        angle = bearing_decimal if bearing_decimal < 179 else bearing_decimal + 180


        dms_split = math.modf(bearing)

        ms = str(round(dms_split[0],4)) + "0000"

        d = str(int(dms_split[1]))
        m = ms[2:4]
        s = ms[4:6]
        dms = d + "^" + m + "'" if s == "00" else d + "^" + m + "'" + s + "\""

        bearing_text = "text " + start + " " + height + " " + str(angle) + " " + dms + "\n"
        distance_text = "text " + start + " " + height + " " + str(angle) + " " + str(distance) + "\n"
        f.write(bearing_text)
        f.write(distance_text)
    f.write(line)
    f.close()
        

def main():

    last_file = "vectors/last.txt"
    
    print("This program calculates survey closures")
    
    while True:
        f_name = input("File name OR press Enter for last used: ")
        f_path = "vectors/" + f_name

        try:
            if f_name == "":                       
                f = open(last_file, "r")  
                f_path = f.read()    
                f.close() 
                if ".txt" in f_path:
                    vectors = np.genfromtxt(f_path, delimiter=',', dtype=None, encoding='utf-8-sig', case_sensitive=False)
                else:
                    vectors = np.genfromtxt(f_path + ".txt", delimiter=',', dtype=None, encoding='utf-8-sig', case_sensitive=False)              
                break

            elif ".txt" in f_path:
                vectors = np.genfromtxt(f_path, delimiter=',', dtype=None, encoding='utf-8-sig', case_sensitive=False)
                break
            else:
                vectors = np.genfromtxt(f_path + ".txt", delimiter=',', dtype=None, encoding='utf-8-sig', case_sensitive=False)
                break

        except:
            print("File not found or incorrect format! Please check the name and if the file is formatted correctly")
            continue
    
    f = open(last_file, "w")
    f.write(f_path)
    f.close()

    easting_list, northing_list = closure(vectors)

    while True:
        choice = input("Would you like to generate the .scr file (Y/N)? ")
        if choice == "Y" or "y":
            gen_scr(easting_list, northing_list, vectors)
            break
        elif choice == "N" or "n":
            break
        else:
            print("Please enter Y or N!")
            continue

   
while True:
    main()