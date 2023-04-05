STEP 0
===================================================================
This program can't run directly on the Z: drive. You need
to save it locally to run it.

STEP 1
===================================================================
Put your bearing and distances in a .txt file in the vectors folder.
The format should be like this:

bearing1,distance1
bearing2,distance2
etc,etc

Notice:
1. There is no space after the commas
2. There is no comma at the end of each line

There is an example.txt in the vectors folder (as an example hehe)
The last.txt file saves the last used file. It shouldn't be deleted
(it will regenerate itself anyway if you do)

STEP 2
===================================================================
Run closure.exe
Type the name of your .txt file (you don't need to include the .txt) and press Enter
If you want to use the last used .txt file, press Enter without typing anything

It should calculate dE, dN, magnitude and bearing of the misclose

===================================================================
I can't count how many times I've made a typo when doing closures on the HP35s and
having to redo everything again :eyeroll:

Hope this program makes it easier for everyone :)

P.S. Maybe in the future I'll make a C++ version of this... the Python one is ~25MB
because it has to include all the dependencies... a C++ version will be much
more lightweight and faster
