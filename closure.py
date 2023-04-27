import numpy as np
import math
from data_types import Angle, Vector

def read_vectors_file() -> np.ndarray:

    vectors_file = "vectors.txt"
    vectors = []

    while True:
        wait = input()
        try:
            vectors_csv = np.genfromtxt(vectors_file, delimiter=',', dtype=None, encoding='utf-8-sig', case_sensitive=False)              
            break
        except:
            print("vectors.txt not found or incorrect format! Please check if the file is formatted correctly")
            continue

    for i in range(len(vectors_csv)):
        bearing= Angle(vectors_csv[i, 0], "dms")
        distance = vectors_csv[i, 1]        
        vector = Vector(distance, bearing, "polar")
        vectors.append(vector)

    return vectors

def closure(vectors: np.ndarray):

    misclose = Vector(0, 0, "cartesian")
    boundary_points = [] #Vectors from origin to vertices of the boundary
    midpoints = [] #Vectors from origin to midpoints of boundary lines

    for i in range(len(vectors)):
        midpoints.append(misclose + vectors[i] * 0.5)
        misclose = misclose + vectors[i]
        boundary_points.append(misclose)

    print("==================")
    print(f"Number of bearing distances: {len(vectors)}")
    print("==================")
    print(f"Delta E: {round(misclose.easting, 3)}")
    print(f"Delta N: {round(misclose.northing, 3)}")
    print("==================")
    print(f"Magnitude: {round(misclose.magnitude, 3)}")
    print(f"Bearing: {misclose.angle}")
    print("==================")

    return boundary_points, midpoints

def gen_scr(boundary_points, vectors, midpoints):
    path = "script.scr"
    boundary_points.reverse()
    coordinates = []

    for i in range(len(boundary_points)):
        coordinates.append(f"{boundary_points[i].easting},{boundary_points[i].northing}")
    coordinates.append("0,0")
    line = "pline " + " ".join(coordinates) + "\n"
    f = open(path, "w")
    

    for i in range(len(boundary_points)):
        
        height = "0.875"

        angle = vectors[i].angle
        text_angle = angle if angle.deg < 179 else Angle(angle.deg - 180, "deg")
        
        bearing_start = f"{midpoints[i].easting + Vector(1, angle - Angle(90, 'deg'), 'polar').easting},{midpoints[i].northing + Vector(1, angle - Angle(90, 'deg'), 'polar').northing}"
        distance_start = f"{midpoints[i].easting + Vector(1, angle + Angle(90, 'deg'), 'polar').easting},{midpoints[i].northing + Vector(1, angle + Angle(90, 'deg'), 'polar').northing}"

        bearing_text = f"text j c {bearing_start} {height} {text_angle.deg} {angle.autocad}\n"
        distance_text = f"text j c {distance_start} {height} {text_angle.deg} {vectors[i].magnitude}\n"

        f.write(bearing_text)
        f.write(distance_text)

    f.write(line)
    f.close()
        
def main():    
    print("Press Enter to calculate the closure")

    vectors = read_vectors_file()
    boundary_points, midpoints = closure(vectors)

    while True:
        choice = input("Would you like to generate the .scr file (Y/N)? ")
        if choice == "Y" or "y":
            gen_scr(boundary_points, vectors, midpoints)
            print("Done!")
            break
        elif choice == "N" or "n":
            break
        else:
            print("Please enter Y or N!")
            continue

while True:
    main()