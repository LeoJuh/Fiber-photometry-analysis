# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 15:51:56 2022

@author: aboo_
"""

import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import tdt
import numpy as np
import re
import matplotlib
from matplotlib import animation
from matplotlib.animation import FuncAnimation
import scipy.sparse as sparse
from scipy.sparse.linalg import splu
import matplotlib.pyplot as plt
import warnings
matplotlib.rcParams['text.usetex'] = False

### Setting path to FFMPEG

Current_working_directory = Path(__file__).parent.resolve()
ffmpeg_path = Path.joinpath(Current_working_directory, "ffmpeg.exe")

matplotlib.rcParams['animation.ffmpeg_path'] = ffmpeg_path


### speyediff and whittaker_smooth will be used as  
### functions for smoothing. 
"""
WHITTAKER-EILERS SMOOTHER in Python 3 using numpy and scipy
based on the work by Eilers [1].
    [1] P. H. C. Eilers, "A perfect smoother", 
        Anal. Chem. 2003, (75), 3631-3636
coded by M. H. V. Werts (CNRS, France)
tested on Anaconda 64-bit (Python 3.6.4, numpy 1.14.0, scipy 1.0.0)
Read the license text at the end of this file before using this software.
Warm thanks go to Simon Bordeyne who pioneered a first (non-sparse) version
of the smoother in Python.
"""


def speyediff(N, d, format='csc'):
    """
    (utility function)
    Construct a d-th order sparse difference matrix based on 
    an initial N x N identity matrix
    
    Final matrix (N-d) x N
    """
    
    assert not (d < 0), "d must be non negative"
    shape     = (N-d, N)
    diagonals = np.zeros(2*d + 1)
    diagonals[d] = 1.
    for i in range(d):
        diff = diagonals[:-1] - diagonals[1:]
        diagonals = diff
    offsets = np.arange(d+1)
    spmat = sparse.diags(diagonals, offsets, shape, format=format)
    return spmat


def whittaker_smooth(y, lmbd, d):
    """
    Implementation of the Whittaker smoothing algorithm,
    based on the work by Eilers [1].
    [1] P. H. C. Eilers, "A perfect smoother", Anal. Chem. 2003, (75), 3631-3636
    
    The larger 'lmbd', the smoother the data.
    For smoothing of a complete data series, sampled at equal intervals
    This implementation uses sparse matrices enabling high-speed processing
    of large input vectors
    
    ---------
    
    Arguments :
    
    y       : vector containing raw data
    lmbd    : parameter for the smoothing algorithm (roughness penalty)
    d       : order of the smoothing 
    
    ---------
    Returns :
    
    z       : vector of the smoothed data.
    """

    m = len(y)
    E = sparse.eye(m, format='csc')
    D = speyediff(m, d, format='csc')
    coefmat = E + lmbd * D.conj().T.dot(D)
    z = splu(coefmat).solve(y)
    return z    


### browse_directory() and assign() are functions that will be used 
### for the initial GUI.

def browse_directory():
    
    """This function allows the user to select the path 
    containing all subject tdt files in one experiment"""
    
    global folder_selected
    global path_to_experiment
    folder_selected = filedialog.askdirectory()
    Text_path.insert(0, f"{folder_selected}")
    path_to_experiment = Text_path.get()
      
def assign():

    """ This function will initially check whether the input is acceptable.
        If all requirements are fullfilled, it will extract the values. Lastly,
        it will destroy and quit the GUI, which will allow for code that is happening
        after the mGui to be executed."""
    
    ### Variables that are going to be used outside this function are assigned as global.
    global Time_range_movie 
    global Duration
    global Baseline
    global Start_time
    global Title
    
    ### In the below section will the input be checked if it 
    ### fullfills the conditions. 
    
    ### Checking if "Enter start time of animation" input field is empty and 
    ### raises an error if true
    if len(Start_time_entry.get()) == 0:
        tk.messagebox.showerror(title = "Error", message = "The \"Enter start time of animation\" field was left empty, please fill it in.")
        raise Exception("The \"Enter start time of animation\" field was left empty, please fill it in.")
    
    ### We want to check that the data input into the "Enter start time of animation" field is numeric
    ### since it should be a number corresponding to the time of the behavioral event.
    ### However since the .get() function returns a string (and will always be a non-integer), we have to use a try-except block.
    try:  
        float(Start_time_entry.get())
        
    except ValueError: 
        tk.messagebox.showerror(title = "Error", message = "You inputted a non-number into the \"Enter start time of animation\", please input a number instead.")
        raise Exception("You inputted a non-number into the \"Enter start time of animation\", please input a number instead.")

    ### Checking if "Enter animation duration" field is empty and 
    ### raises an error if true
    if len(Duration_entry.get()) == 0:
        tk.messagebox.showerror(title = "Error", message = "The \"Enter duration of animation\" field was left empty, please fill it in.")
        raise Exception("The \"Enter duration of animation\" field was left empty, please fill it in.")
    
    ### We want to check that the data input into the "Enter animation duration" field is numeric
    ### since it should be a number corresponding to the duration of the animation.
    ### However since the .get() function returns a string (and will always be a non-integer), we have to use a try-except block.
    try:  
        float(Duration_entry.get())
        
    except ValueError: 
        tk.messagebox.showerror(title = "Error", message = "You inputted a non-number into the \"Enter duration of animation\" field, please input a number instead.")
        raise Exception("You inputted a non-number into the \"Enter duration of animation\" field, please input a number instead.") 
           
    ### Checking if any of the entry fields for the baseline time range are empty.
    if (len(base_pre_entry.get()) == 0) or (len(base_post_entry.get()) == 0):
        tk.messagebox.showerror(title = "Error", message = "Atleast one of the The \"Enter baseline time range:\" entry fields was left empty, please fill it in.")
        raise Exception("Atleast one of the The \"Enter baseline time range:\" entry field was left empty, please fill it in.")
    
    ### We want to check that the data input into the "Enter baseline time range time of animation" fields are numeric
    ### since it should be a number corresponding to the time range of the baseline.
    ### However since the .get() function returns a string (and will always be a non-integer), we have to use a try-except block.
    try:  
        float(base_pre_entry.get())
        float(base_post_entry.get())
        
    except ValueError: 
        tk.messagebox.showerror(title = "Error", message = "You inputted a non-number into atleast one of the  \"Enter baseline time range\", entry fields, please input a number instead.")
        raise Exception("You inputted a non-number into the \"Enter baseline time range\", please input a number instead.")

    ### This checks whether the duration is lower than 0 (i.e., non-negative),
    ### and raises an error if true.
    if float(Duration_entry.get()) < 0:
        tk.messagebox.showerror(title = "Error", message = "The inputted Duration needs to be higher than 0")
        raise Exception("The right field of the extraction time range fields needs to be higher than 0")
        
    ### This checks whether the start time of the baseline is lower than 0 and raises an error if true. 
    if float(base_pre_entry.get()) < 0:
        tk.messagebox.showerror(title = "Error", message = "The baseline start time point needs to be 0 or higher")
        raise Exception("The baseline start time point needs to be 0 or higher")
    
    ### This checks whether the start time of the baseline is higher than the end time of the baseline, and raises an error if true. 
    if float(base_pre_entry.get()) > float(base_post_entry.get()):
        tk.messagebox.showerror(title = "Error", message = "The end time point of the baseline is lower than the baseline start time point")
        raise Exception("The end time point of the baseline is lower than the baseline start timepoint")
    
    ### Extracting the values
    Start_time = float(Start_time_entry.get())
    Duration  = float(Duration_entry.get())
    Baseline = (float(base_pre_entry.get()), float(base_post_entry.get()))
    Title = Title_entry.get()

    ### If this point is reached, i.e. the "Click here to finish" button has been clicked 
    ### and no errors have been raised (all inputted data is correct) the GUI will be
    ### closed (mGui.destroy) and the loop will be broken (mGui.quit()). This
    ### will allow for the code below the mGui.mainloop() to be run.   
    mGui.destroy()       
    mGui.quit()
    
### Initializing GUI.
mGui = tk.Tk()

### Objects shown before clicking any checkbox
mGui.geometry("400x250+500+300")
mGui.title("Choosing parameters for Movie making")

### Creating entry boxes.
Text_path = tk.Entry(mGui)
Start_time_entry = tk.Entry(mGui)
Duration_entry = tk.Entry(mGui)
base_pre_entry = tk.Entry(mGui)
base_post_entry = tk.Entry(mGui)
Title_entry = tk.Entry(mGui)

### Creating labels
Start_time_label = tk.Label(mGui, text="Enter start time of animation:",font=("Arial", 10), anchor="w")
Duration_label = tk.Label(mGui, text="Enter duration of animation:",font=("Arial", 10), anchor="w")
base_label = tk.Label(mGui, text="Enter baseline time range:",font=("Arial", 10), anchor="w")
base_to_label = tk.Label(mGui, text="to", font=("Arial", 10))
Title_entry_label = tk.Label(mGui, text="Enter title for video:", font=("Arial", 10))

### Creating browse and exit button
browse_Button = tk.Button(mGui, text="Click here to import subject PATH:", command=browse_directory)
Exit_Button = tk.Button(mGui, text="Click here to finish", command=assign)

### Placing buttons and checkboxes
Text_path.place(relx=0.52, rely=0.01, relwidth=0.42, relheight=0.09)
browse_Button.place(relx=0.005, rely=0.01, relwidth=0.5, relheight=0.09)
Exit_Button.place(relx=0.31, rely=0.90, relwidth=0.28, relheight=0.088)
Start_time_label.place(relx=0.02, rely=0.19, relwidth=0.43, relheight=0.08) 
Start_time_entry.place(relx=0.51, rely=0.19, relwidth=0.2, relheight=0.09)   
Duration_label.place(relx=0.04, rely=0.34, relwidth=0.41, relheight=0.07)  
Duration_entry.place(relx=0.51, rely=0.34, relwidth=0.2, relheight=0.09)
base_label.place(relx=0.055, rely=0.48, relwidth=0.39, relheight=0.08)
base_pre_entry.place(relx=0.51, rely=0.48, relwidth=0.07, relheight=0.09)
base_post_entry.place(relx=0.65, rely=0.48, relwidth=0.07, relheight=0.09)
base_to_label.place(relx=0.595, rely=0.505, relwidth=0.03, relheight=0.04)
Title_entry.place(relx=0.51, rely=0.61, relwidth=0.21, relheight=0.09)
Title_entry_label.place(relx=0.165, rely=0.62, relwidth=0.27, relheight=0.04)

### Blocking code after .mainloop until mGui has been destroyed and quitted
mGui.mainloop()

### Variables for analysis
Start = 5

### Getting paths using pathlibs Path function
path_to_experiment = Path(path_to_experiment)
path_str = str(path_to_experiment)

### Getting child and parent name of folder to be used
### for the output mp4 file name
Subject_name = path_to_experiment.name
Exp_name = path_to_experiment.parent.name

### Joining experiment path to the output file name to export video later
Path_for_exporting_video = Path.joinpath(path_to_experiment.parent, f"{Exp_name}, {Subject_name} animation.mp4")

### Reading selected tdt file
subject_data = tdt.read_block(path_to_experiment, t1 = Start)
Subject_name = re.search("([^\/|^\\\]+$)", path_str).group(0) 

if subject_data is None:
    
    mGui = tk.Tk()              # Initializing GUI    
    mGui.withdraw()             # Withdrawing main window, to only display the error message
    tk.messagebox.showerror(title = "Error", message = f"The {Subject_name} folder could not be read by the tdt package")      
    raise Exception("The {Subject_name} folder could not be read by the tdt package")

else:

    ### Sensors names are found using regex in two steps. 
    ### First selecting the relevant streams from the tdt.streams block.
    ### There are some datastreams which are irrelevant for our analysis 
    ### which we ignore.
    name_of_data_streams = str(subject_data.streams)
    pattern_data_streams = r"_\d+[a-zA-Z]"
    matches_data_streams = re.findall(pattern_data_streams, name_of_data_streams)
    
    ### In the second part we extract the sensor type.
    ### For example, if we have a data stream called
    ### _405A, this name tells us it was recorded with the 
    ### sensor A. This regex finds the Sensor name.
    pattern_sensors = r"[a-zA-Z]"
    Sensor_names = re.findall(pattern_sensors, str(matches_data_streams))
    Sensor_names_no_duplicates = list(dict.fromkeys((Sensor_names)))     # 
    
    ### If there are no sensor names, it means that something has gone wrong
    ### and there are no data streams that can be used for analysis
    if len(Sensor_names_no_duplicates) == 0:
        raise Exception("No fiber photometry signals seems to be present in this recording")
        
    if len(Sensor_names_no_duplicates) == 1:
        
        Sensor = Sensor_names_no_duplicates[0]
        Sensor_selection = [True]
    
    ### If there are two sensor names, it means the recording was done with two
    ### fibers. In that case, a GUI created by tkinter will '
    ### pop up, which enables the user to select what sensor to use for the 
    ### recording. 
    if len(Sensor_names_no_duplicates) == 2:
        
        ### Main window is created
        mGui = tk.Tk()
        mGui.geometry("300x350+500+300")
        mGui.title("Select sensor")
              
        ### Text asking (Which sensor do you want to use for analysis?)
        Sensor_question = tk.Label(mGui, text="Which sensor(s) do you want to use for analysis?", font=("Arial", 9, "bold"))

        ### Boolean variables for the sensors. 
        ### If checkboxes 
        Sensor_1_bool = tk.BooleanVar()
        Sensor_2_bool = tk.BooleanVar()   
        
        ### The checkboxes below are connected to the Sensor_1_bool and Sensor_2_bool variables
        ### Upon clicking the checkboxes, they will switch to True. Thus, when th checkboxes
        ### are empty, they will be False variables
        
        ### First checkbox which will contain the sensor name of the sensor in 
        ### the first position in the sensor name list.Upon clicking this checkbox
        ### the Sensor_1_bool variable will be set as True   
        checkbox_sensor_1 = tk.Checkbutton(mGui, 
                                           text=f"Sensor {Sensor_names_no_duplicates[0]}",
                                           variable=Sensor_1_bool,
                                           onvalue=True, 
                                           offvalue=False)
        
        ### First checkbox which will contain the sensor name of the sensor in 
        ### the second position in the sensor name. Upon clicking this checkbox
        ### the Sensor_2_bool variable will be set as True.
        checkbox_sensor_2 = tk.Checkbutton(mGui, 
                                           text=f"Sensor {Sensor_names_no_duplicates[1]}",
                                           variable=Sensor_2_bool,
                                           onvalue=True,
                                           offvalue=False)
        
        # Pack the checkboxes into the window
        checkbox_sensor_1.place(relx=0.2, rely=0.45)
        checkbox_sensor_2.place(relx=0.6, rely=0.45)   
        Sensor_question.place(relx=0.05, rely=0.35)
                       
        def my_function():
            
            """ This function will plot an option to 
                input legend names for the two traces."""
                
            ### Assigning global variables to the entries into the
            ### entry legend fields
            global Entry_legend_name_sensor_1
            global Entry_legend_name_sensor_2
                
            Entry_legend_name_sensor_1 = tk.Entry(mGui)
            Entry_legend_name_sensor_2 = tk.Entry(mGui)
            
            Entry_legend_name_sensor_1_label = tk.Label(mGui, text= f"Enter legend name \n for sensor {Sensor_names_no_duplicates[0]}",font=("Arial", 10), anchor="w")
            Entry_legend_name_sensor_2_label = tk.Label(mGui, text= f"Enter legend name \n for sensor {Sensor_names_no_duplicates[1]}", font=("Arial", 10), anchor="w")                                            
            
            Entry_legend_name_sensor_1_label.place(relx=0.05, rely=0.56, relwidth=0.37, relheight=0.12)
            Entry_legend_name_sensor_2_label.place(relx=0.05, rely=0.75, relwidth=0.37, relheight=0.12)
            Entry_legend_name_sensor_1.place(relx=0.53, rely=0.59, relwidth=0.25, relheight=0.065)
            Entry_legend_name_sensor_2.place(relx=0.53, rely=0.78, relwidth=0.25, relheight=0.065)
                                                            
        def check_checkboxes():
            if Sensor_1_bool.get() and Sensor_2_bool.get():
                my_function()

        Sensor_1_bool.trace("w", lambda *args: check_checkboxes())
        Sensor_2_bool.trace("w", lambda *args: check_checkboxes())      
        
        def extract_values():
            
            """This function will be executed when the user clicks the
            "click here to finish" button in the Select Sensor GUI".
            This will import the variables from the Checkboxes and
            check that one of the checkboxes has been filled in, 
            and not two or none of the checkboxes has been filled in.
            Lastly, the function will extract the variables and terminate the GUI"""
            
            ### The global variable assignment will imports the Sensor_1_bool and Sensor_2_bool 
            ### into the function, and export the Sensor1 and Sensor2 variables out of the function

            global Sensor_selection                 
            
        
            ### This checks whether none of the Sensor type checkboxes have been filled in,
            ### and throws an error if true
            if Sensor_1_bool.get() is False and Sensor_2_bool.get() is False:
                
                tk.messagebox.showerror(title = "Error", message = "No sensor selected, please select one")
                raise Exception("No sensor selected, please select one")
             
            if Sensor_1_bool.get() and Sensor_2_bool.get():
             
                global legend_names
                
             
                legend_name_sensor_1 = Entry_legend_name_sensor_1.get()
                legend_name_sensor_2 = Entry_legend_name_sensor_2.get()
                legend_names = [legend_name_sensor_1, legend_name_sensor_2]


            ### If the conditions are met, the Boolean variables are extracted using the .get() function 
            Sensor1 = Sensor_1_bool.get()
            Sensor2 = Sensor_2_bool.get()
            Sensor_selection = [Sensor1, Sensor2]
            
            ### If this point is reached, i.e. the "Click here to finish" button has been clicked 
            ### and no errors have been raised (all inputted data is correct) the GUI will be
            ### closed (mGui.destroy) and the loop will be broken (mGui.quit()). This
            ### will allow for the code below the nGui.mainloop() to be run.
            mGui.destroy()
            mGui.quit()

        Exit_Button = tk.Button(mGui, text="Click here to finish", command=extract_values)
        Exit_Button.place(relx=0.31, rely=0.92, relwidth=0.36, relheight=0.077)


        mGui.mainloop()

for i, sensor in enumerate(Sensor_selection):
    if not sensor:
        del Sensor_names_no_duplicates[i]


### Empty lists
calcium_dependent_signal_lst = []
calcium_independent_signal_lst = []
Sampling_rate_calcium_dependent_lst = []

for Sensor in Sensor_names_no_duplicates:

    ### Checking to see the sensors 
    calcium_dependent_signal = subject_data.streams[f"_465{Sensor}"].data
    calcium_independent_signal = subject_data.streams[f"_405{Sensor}"].data
    subject_sampling_rate_465 = subject_data.streams[f"_465{Sensor}"].fs
    
    
    calcium_dependent_signal_lst.append(calcium_dependent_signal)
    calcium_independent_signal_lst.append(calcium_independent_signal)
    Sampling_rate_calcium_dependent_lst.append(subject_sampling_rate_465)
    
Timevectors_calcium_dependent_lst = []    
    
### Creating time vectors for calcium dependent signals
for sampling_rate_calcium_dependent, calcium_dependent_signal in zip(Sampling_rate_calcium_dependent_lst, calcium_dependent_signal_lst):   
    
     
    ### The timevector is created by generating, using numpy linspace (https://numpy.org/doc/stable/reference/generated/numpy.linspace.html), an vector with evenly spaced numbers. 
    ### Initially, for each signal (465 or 405) each data point in the signals will have one data point in the timevector, since we´ve set end value the same as the number of time vector datapoints to be generated
    ### For example, for one signal with 6000 data points, the time vector will consist of 6000 datapoints with integers. 
    ### Lastly, the timevector will be divided by the frame rate (i.e. number of signal data points per second for that signal). The frame rate is fixed by a quartz crystal and is therefore reliable. 
    ###Upon doing this, the timevector is converted to seconds, and we will then have a time vector with data points representing the time point of all signal data points.
    
    ### Creating timevectors for 465 wavelength
    Timevector_calcium_dependent = Start + np.linspace(1, len(calcium_dependent_signal), len(calcium_dependent_signal)) / sampling_rate_calcium_dependent
    
    ### Appending Timevector_calcium_dependent
    Timevectors_calcium_dependent_lst.append(Timevector_calcium_dependent)
    
    ### Correcting calcium dependent signal using calcium independent signal 

### In the below code, the calcium-dependent signal is corrected for fluctuations not related to changes in intracellular calcium.
### This is done by fitting the calcium-independent signal to the calcium-dependent.
### THis is done using the numpy.polyfit function (https://numpy.org/doc/stable/reference/generated/numpy.polyfit.html)
### which performs a least-squared polynomial fit. Since we are using the polyfit with the first degree, we are performing
### a least-squared linear regression to fit the calcium-independent to the calcium-dependent. 
### After fitting, we subtract the fitted calcium-independent from the calcium-dependent and
### then get the corrected calcium-dependent signal which we append into the 
### Correct_calcium_dep lst. 
    
### This error is raised due to the fitted calcium independent trace being sensitive to small changes in the data.
### It seems to be raised for all samples, even if the fit is completely acceptable by manual observation.
### Thus, the code below silences this warning since it in our case doesn´t seem to provide any valuable information.
Corrected_calcium_dependent_lst = []

### This error is raised due to the fitted calcium independent trace being sensitive to small changes in the data.
### It seems to be raised for all samples, even if the fit is completely acceptable by manual observation.
### Thus, the code below silences this warning since it in our case doesn´t seem to provide any valuable information.
warnings.simplefilter('ignore', np.RankWarning)

for calcium_independent_signal, calcium_dependent_signal in zip(calcium_independent_signal_lst, calcium_dependent_signal_lst):

    
    fitting_independent_to_dependent = np.polyfit(calcium_independent_signal, calcium_dependent_signal, 1) ### Using polyfit to the first degree.
    fit_line_independent_to_dependent = np.multiply(fitting_independent_to_dependent[0], calcium_independent_signal) + fitting_independent_to_dependent[1]
    Corrected_calcium_dependent = calcium_dependent_signal - fit_line_independent_to_dependent
    
    ### Appending corrected calcium dependent signal to list
    Corrected_calcium_dependent_lst.append(Corrected_calcium_dependent)

### Z-scoring 
Z_score_events_lst = []
Index_for_start_recording = []
Timevectors_for_behavioral_events_lst = []

### In this code, the neural activty surrounding the event will be extracted and converted to Z-score.
### The code will also extract the index for the neural activity which occured at 5 seconds after the first data point in the 
### extracted neural activity. This will be used to plot the starting activity from 0-5 seconds in the first frame.
### I.e., the animation will start with the first 5 seconds initially being plotted.
for i, (timevector_calcium_dependent, Corrected_calcium_dependent) in enumerate(zip(Timevectors_calcium_dependent_lst, Corrected_calcium_dependent_lst)):
    
    ### The activity surrounding each behavioral event will be gathered using numpy.where(https://numpy.org/doc/stable/reference/generated/numpy.where.html). 
    ### where indices fullfilling certain critiries will be extracted. In our case, we select the indices of the timevector where the data points are 
    ### firstly higher than the time point of the behavioral event subtracted with 5 AND lower than the time point of the behavioral event + the duration of the video  
    ### Why the first condition "(timevector_calcium_dependent > (Time_of_event + - 5))" in the np.where function also includes a -5 subtraction is because we want to get 5-seconds before 
    ### the user specified extraction range to plot in starting position in the animation, so the animation starts with data already plotted. 
    index_for_behavioral_event = np.where((timevector_calcium_dependent > Start_time - 5) & ((timevector_calcium_dependent < Start_time + Duration)))
       
    ### These indeces are thereafter used to select the signal data points in the corrected calcium dependent signal.
    ### This works since the timevector and the corrected calcium signal share the same indices.
    ### To explain it a bit further, to find the signal corresponding to a specific time point in the timevector, 
    ### you only need to use the index of that time data point in the signal vector.    
    Neural_activity_for_behavioral_event = Corrected_calcium_dependent[index_for_behavioral_event]
    
    ### Creating a timevector for the behavioral event. 
    ### Yet again, this includes the -5 subtraction for the initial plotted 5-second neural activity in the animation.
    Timevector_for_behavioral_event = - 5 + np.linspace(1, len(Neural_activity_for_behavioral_event), len(Neural_activity_for_behavioral_event))/ Sampling_rate_calcium_dependent_lst[i]
    
    ### Getting the index for the baseline using the np.where function
    ind_baseline = np.where((Timevector_for_behavioral_event > Baseline[0]) & (Timevector_for_behavioral_event < Baseline[1]))
    
    ### Z-scoring by subtracting the neural activity of the event with the mean neural activity of the baseline, 
    ### and lastly dividing the subtraction product by the std of the 
    Z_score_event = (Neural_activity_for_behavioral_event -  Neural_activity_for_behavioral_event[ind_baseline].mean()) /  Neural_activity_for_behavioral_event[ind_baseline].std()
    
    ### Smoothing Z_score_event using whittaker_smoothing
    Z_score_smoothed = whittaker_smooth(Z_score_event, lmbd=10000000, d = 2)
    
    ### Since we want the animation to have already plotted 5 seconds of neural activity
    ### we will also get the index corresponding to 5s. In the animation
    ### we will then start plotting from that timestamp.
    ### This index is found by using one condition (getting all indexes)
    ### where there corresponding values in the time vector are bigger than 
    ### 0. This is because all the data that we want to plot are plotted after 
    ### the zero-second mark. Thereafter, we are getting the min value, which will be the 
    ### index-value that is the closest to the zero-second mark. 
    min_index = np.where(Timevector_for_behavioral_event > 0)[0].min()

    ### Appending data to lists
    Timevectors_for_behavioral_events_lst.append(Timevector_for_behavioral_event)
    Index_for_start_recording.append(min_index)
    Z_score_events_lst.append(Z_score_smoothed)
    
### This processing is done so that if we have neural activty traces 
### from more than one sensor, they will have the same length.  
min_z_score = np.min([len(Z_score) for Z_score in Z_score_events_lst])
Z_score_events_lst = [Z_score[:min_z_score] for Z_score in Z_score_events_lst]

### Creating figure and axes object for figure to be used in the animation
fig, axes = plt.subplots(1, 1, figsize=(10,5))

### Setting colors for traces
colors = ["green", "red"]

### Calculating number of frames that should be plotted in animation. Since we are only plotting each 29th datapoint
### (to limit time taken to generate animation), we are getting the number of frames
### by selecting the datapoints that are either going to be plotted, or lie between datapoints that are going to be plotted
### (i.e. all datapoints after 0 seconds) and take the length of this selection (i.e. the number of datapoints)
### and divide it by 29
Num_frames = int(len(Z_score_events_lst[0][Index_for_start_recording[0]:]) / 29)

### Setting start and end x_val (time) points for the plot.
### These will be updated in the animate function.
Start = -5
End = 5 

### Creating list2D objects for plotting traces
### The reason this is done in a for loop
### is that it is compatible with data 
### from both one and two traces. 
artist_lst = []

for i in range(len(Sensor_names_no_duplicates)):
    
    ### Creating an line object. The line2D 
    ### object returns an tuple but we are
    ### only interested in the first element of the tuple (the trace)
    ### we will unpack the tuple and select the first element,
    ### which is done by setting the comma.
    line, = axes.plot([], [], lw=2, color=colors[i])
     
    ### Appending line object to artist_lst   
    artist_lst.append(line)    

### If there are two selected sensors and both the entry boxes are filled in,
### then we will set them as legend names. 
if (len(Sensor_names_no_duplicates) == 2): 
    if (len(legend_names[0]) > 0) & (len(legend_names[1]) > 0):

        axes.legend(artist_lst, 
                    legend_names,
                    frameon=False, 
                    fontsize=15, 
                    loc="upper right")
     
### Changing settings for matplotlib animation plot.
axes.spines["right"].set_visible(False)
axes.spines["top"].set_visible(False)
axes.spines["bottom"].set_visible(False)
axes.set_ylabel("Z-score", fontsize=20, labelpad=15)
axes.set_xlim(Start, End)


### Getting max and min values for setting y-lim 
max_Z_score = np.max([np.max(Z_score_event) for Z_score_event in Z_score_events_lst])
min_Z_score = np.min([np.min(Z_score_event) for Z_score_event in Z_score_events_lst])
axes.set_ylim(min_Z_score-2, max_Z_score+2)

if len(Title) > 0:
    axes.set_title(Title, fontsize = 20)

### Tick params for x-ticks and y-ticks
axes.tick_params(
    axis="x",
    which="both",      
   bottom=False,      
    top=False,         
   labelbottom=False)

axes.tick_params(
    axis="y",
    which="major",
    labelsize="15")

### Empty lists used for animation
x_values_to_plot_lst = []
y_values_to_plot_lst = []
x_values_for_animation_lst = []
y_values_for_animation_lst = []

### In this for loop the data will be split into two different types
### of lists. The first type, called x/y_values_start_lst,
### contains data from 0-5 seconds and will all be plotted
### in the first frame. The second type, called x/y_values_for_animation_lst
### contain data that will be progessively plotted in each frame.
for i in range(len(Sensor_names_no_duplicates)):
       
    ### Getting the index at 5s (start of animation)
    Index_start = Index_for_start_recording[i]
    
    ### Inserting the five first seconds in the x_value list and y_val list
    ### The list is inserted and then flattened using np.ravel.
    x_val_start = [Timevectors_for_behavioral_events_lst[i][:Index_start]]
    x_val_start_flattened = list(np.ravel(x_val_start))

    y_val_start = [Z_score_events_lst[i][:Index_start]]
    y_val_start_flattened = list(np.ravel(y_val_start))

    ### This selects the x_values and y_values that
    ### occurs after the Start time (0 seconds)
    ### and are thus the values that will be progressively
    ### plotted in the animation. 
    x_values_to_plot = Timevectors_for_behavioral_events_lst[i][Index_start:]
    y_values_to_plot = Z_score_events_lst[i][Index_start:]

    ### Appending data
    x_values_for_animation_lst.append(x_val_start_flattened)
    y_values_for_animation_lst.append(y_val_start_flattened)
    x_values_to_plot_lst.append(x_values_to_plot)
    y_values_to_plot_lst.append(y_values_to_plot)

### This function will be used to plot the base frames and 
### also represents the start frame.
def init():
    
    for i in range(len(Sensor_names_no_duplicates)):  
        ### Setting 0-5 seconds data
        artist_lst[i].set_data(x_values_for_animation_lst[i], y_values_for_animation_lst[i])
        
    return artist_lst
 
### This is the function that will be used to plot each frame 
def animate(i):
    
    global Start
    global End

    ### Firstly, we append new values to the x/y_values_for_animation_lst  and
    ### lists. To limit frames and save time
    ### required to plot the animation, we will only plot
    ### the 29th data points, hence we index the plotting lsts
    ### with i*29
    for j in range(len(Sensor_names_no_duplicates)):
            
        x_values_for_animation_lst[j].append(x_values_to_plot_lst[j][i*29])
        y_values_for_animation_lst[j].append(y_values_to_plot_lst[j][i*29]) 

        artist_lst[j].set_data(x_values_for_animation_lst[j], y_values_for_animation_lst[j])
    
    ### Thereafter, after the first frame, we will update
    ### the start and end variables to be used to set the 
    ### new x-limits. 
    if i > 0:
        
        ### This sets the Time_diff that will be updated.
        ### This time-diff is equal to the difference in time
        ### between the plotted y-value in the current frame
        ### and the plotted y-value in the previous frame.
        Time_diff = x_values_to_plot[i*29] - x_values_to_plot[(i-1)*29]
        Start +=  Time_diff
        End   +=  Time_diff

        ### Setting the x-lim with updated start and end x-limits 
        axes.set_xlim(Start, End)
        
    return artist_lst

### Creating the animation
anim = FuncAnimation(fig, func=animate, frames=int(Num_frames), init_func = init, blit=True)
### Setting parameters for the ffmpeg writer
FFwriter=animation.FFMpegWriter(fps=int(Num_frames/Duration))
### Saving animation
anim.save(Path_for_exporting_video, writer=FFwriter, dpi = 200)