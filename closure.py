import numpy as np
import math
from data_types import Angle


def calc_bearing(easting, northing):
    angle = np.arctan(easting/northing)

    bearing_dms = Angle((math.degrees(angle) + 360) % 360, "decimal")

    return bearing_dms
    
def closure(vectors):
    easting = 0
    northing = 0

    easting_list = [0]
    northing_list = [0]

    for i in range(len(vectors)):
        bearing_rad = Angle(vectors[i, 0], "dms").radians
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
    print(f"Number of bearing distances: {len(vectors)}")
    print("==================")
    print(f"Delta E: {easting}")
    print(f"Delta N: {northing}")
    print("==================")
    print(f"Magnitude: {magnitude}")
    print(f"Bearing: {bearing}")
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
        bearing = Angle(vectors[i, 0], "dms")
        distance = vectors[i, 1]

        angle = bearing if bearing.decimal < 179 else Angle(bearing.decimal + 180, "decimal")

        bearing_text = f"text {start} {height} {angle.decimal} {angle.autocad}\n"
        distance_text = f"text {start} {height} {angle.decimal} {distance}\n"

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