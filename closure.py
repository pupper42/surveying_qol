import pandas as pd
from data_types import Angle, Vector
import pyinputplus as pyip

def read_vectors_file(units):

    vectors_file = "vectors.txt"
    vectors = []
    vectors_df = pd.read_csv(vectors_file, header=None)      

    for i in range(len(vectors_df)):

        bearing= Angle(vectors_df[0][i], "dms")
        distance = vectors_df[1][i]

        if units == "Metres" or units == "":
            vector = Vector(distance, bearing, "polar")
        elif units == "Feet and Inches":
            distance = round(float(distance[:distance.index('f')]) * 0.3048 + float(distance[distance.index('f')+1:distance.index('i')]) * 0.0254, 2)
            vector = Vector(distance, bearing, "polar")
        elif units == "Links":
            distance = round(float(distance)*0.201168, 2)
            vector = Vector(distance, bearing, "polar")

        vectors.append(vector)

    return vectors

def closure(vectors):

    misclose = Vector(0, 0, "cartesian")
    boundary_points = [] #Vectors from origin to vertices of the boundary
    midpoints = [] #Vectors from origin to midpoints of boundary lines

    for i in range(len(vectors)):
        midpoints.append(misclose + vectors[i] * 0.5)
        misclose = misclose + vectors[i]
        boundary_points.append(misclose)

    print("==================")
    print("List of bearing distances (converted to m)")
    [print(f"{x.angle}, {x.magnitude}") for x in vectors]
    print("==================")
    print(f"Number of bearing distances: {len(vectors)}")
    print("==================")
    print(f"Delta E (m): {round(misclose.easting, 3)}")
    print(f"Delta N (m): {round(misclose.northing, 3)}")
    print("==================")
    print(f"Magnitude (m): {round(misclose.magnitude, 3)}")
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

        bearing_text = f"text j mc {bearing_start} {height} {text_angle.deg} {angle.autocad}\n"
        distance_text = f"text j mc {distance_start} {height} {text_angle.deg} {vectors[i].magnitude}\n"

        f.write(bearing_text)
        f.write(distance_text)

    f.write(line)
    f.close()
        
def main():    
    print("==================")
    print("Select an option and press Enter to calculate the closure (selecting nothing will default to Metres)")
    units = pyip.inputMenu(["Metres", "Feet and Inches", "Links"], prompt="Distances are in:\n", numbered=True, blank=True)
    units = "Metres" if units == "" else units
    
    print(f"Selected units: {units}")
    try:   
        vectors = read_vectors_file(units)
        boundary_points, midpoints = closure(vectors)
        while True:
            choice = input("Would you like to generate the .scr file (Y/N)? ")
            if choice == "Y" or choice == "y":
                gen_scr(boundary_points, vectors, midpoints)
                print("Done :D")
                break
            elif choice == "N" or choice == "n":
                print("Ok no worries :)")
                break
            else:
                print("Please enter Y or N!")
                continue
    except Exception as e:
        print("vectors.txt not found or formatted incorrectly for the chosen units!")
        print(f"Error message: {e}")
        print("If you think this is a bug, please let me know :)")
    
while True:
    main()