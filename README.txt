STEP 0
===================================================================
This program can't run directly on the Z: drive. You need
to save it locally to run it.

STEP 1
===================================================================
Put your bearing and distances in vectors.txt

Format is:

bearing1,distance1
bearing2,distance2
etc,etc

Notice:
1. There is no space after the commas
2. There is no comma at the end of each line
3. Bearings are in the format ddd.mmss

STEP 2
===================================================================
Run closure.exe and press enter

It should calculate dE, dN, magnitude and bearing of the misclose

STEP 3
===================================================================
If you press Y to generate a script file you can import
it into AutoCAD and it will automatically draw the boundary + text 
with the correct orientation.

In AutoCAD run the "script" command, choose the generated script.scr
and press Enter. 