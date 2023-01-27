# Fiber-photometry-analysis
For analysis of fiber photometry recordings aquired using equipment from tucker davis technologies.

This repo contains two python scripts placed in two separate folders. 

In the "Create fiber photometry animations"
folder, there is a python script called "Movie_making.py" which can be used to generate fiber photometry animations.
In this folder, there is a text file describing the required inputs and  the output of the script. 
Note! It is important that you do not move the Move_making.py script from its original folder without moving the ffmpeg.exe file to the same location.
The ffmpeg.exe file is used for generating the animation, and if it is not placed in the same folder as the 
Movie_making.py script, the script won´t be able to find it. 

In the "Fiber photometry analysis" folder, there is a python script called "Fiber photometry analysis" which can be used
to visualize whole recording calcium or to perform peri analysis. In the folder there is also a txt file and a jpg
file. The txt is describing the some of required inputs (and some advice on which parameters to use) and the output of the script.
The jpg file contains an image showing the workflow of the analysis. 




Guides:

- [Installation guide for repo using pip](https://www.youtube.com/channel/UCojU2f3z4_5d-jA-NTxQS-Q)

- [Installation guide for repo using anaconda](https://www.youtube.com/watch?v=IJxzP_HgnjU)


- [Overlaying fiber photometry animation with behavioral video](https://www.youtube.com/watch?v=QeO9nzUtW3M)


