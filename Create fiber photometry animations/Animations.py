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
import matplotlib as plt
import time as time1
import matplotlib
import numpy as np
from matplotlib import animation
from matplotlib.animation import FuncAnimation
import tdt
import matplotlib.ticker as plticker
import matplotlib.pyplot as plt

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
    global Extraction_range
    global Baseline
    global Time_of_event
    
    ### Checking that all the inputted conditions are correct. 
    
    ### This checks whether the extraction start time is higher than 0 (i.e., non-negative),
    ### and raises an error if true.
    if float(Extraction_pre_entry.get()) > 0:
        tk.messagebox.showerror(title = "Error", message = "The left field of the extraction time range fields needs to be lower than 0")
        raise Exception("The left field of the extraction time range fields needs to be lower than 0")
    
    ### This checks whether the extraction endtime is lower than 0 (i.e., non-negative),
    ### and raises an error if true.
    if float(Extraction_post_entry.get()) < 0:
        tk.messagebox.showerror(title = "Error", message = "The right field of the extraction time range fields needs to be higher than 0")
        raise Exception("The right field of the extraction time range fields needs to be higher than 0")

    ### This checks whether the baseline start time is lower than the total range extraction start time (i.e., baseline to be used to normalize peri event includes data outside the peri event range),
    ### and raises an error if true.
    if float(Extraction_pre_entry.get()) > float(base_pre_entry.get()):
        tk.messagebox.showerror(title = "Error", message = "The start time point of the baseline is outside of the extraction time range")
        raise Exception("The start time point of the baseline is outside of the extraction time range")
    
    ### This checks whether the baseline end time is higher than the total range extraction end time (i.e., baseline to be used to normalize peri event includes data outside the peri event range),
    ### and raises an error if true. 
    if float(Extraction_post_entry.get()) < float(base_post_entry.get()):
        tk.messagebox.showerror(title = "Error", message = "The end time point of the baseline is outside of the extraction time range")
        raise Exception("The end time point of the baseline is outside of the extraction time range")
    
    ### This checks whether the start time of the baseline is higher than the end time of the baseline, and raises an error if true. 
    if float(base_pre_entry.get()) > float(base_post_entry.get()):
        tk.messagebox.showerror(title = "Error", message = "The end time point of the baseline is lower than the baseline start time point")
        raise Exception("The end time point of the baseline is lower than the baseline start timepoint")
     
    Time_of_event = float(Behavioral_event_entry.get())
    Extraction_range  = (float(Extraction_pre_entry.get()), float(Extraction_post_entry.get()))
    Baseline = (float(base_pre_entry.get()), float(base_post_entry.get()))

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

### Creating entry box for path.
Text_path = tk.Entry(mGui)
Behavioral_event_entry = tk.Entry(mGui)
Extraction_pre_entry = tk.Entry(mGui)
Extraction_post_entry = tk.Entry(mGui)
base_pre_entry = tk.Entry(mGui)
base_post_entry = tk.Entry(mGui)
Title_entry = tk.Entry(mGui)

### Creating labels
Behavioral_event_label = tk.Label(mGui, text="Enter time point of event:",font=("Arial", 10), anchor="w")
Extraction_label = tk.Label(mGui, text="Enter extraction time range:",font=("Arial", 10), anchor="w")
base_label = tk.Label(mGui, text="Enter baseline time range:",font=("Arial", 10), anchor="w")
Extraction_to_label = tk.Label(mGui, text="to", font=("Arial", 10))
base_to_label = tk.Label(mGui, text="to", font=("Arial", 10))
Title_entry_label = tk.Label(mGui, text="Title for video:", font=("Arial", 10))


### Creating browse and exit button
browse_Button = tk.Button(mGui, text="Click here to import subject PATH:", command=browse_directory)
Exit_Button = tk.Button(mGui, text="Click here to finish", command=assign)

### Placing buttons and checkboxes
Text_path.place(relx=0.52, rely=0.01, relwidth=0.42, relheight=0.09)
browse_Button.place(relx=0.005, rely=0.01, relwidth=0.5, relheight=0.09)
Exit_Button.place(relx=0.31, rely=0.89, relwidth=0.3, relheight=0.10)
Behavioral_event_label.place(relx=0.02, rely=0.19, relwidth=0.37, relheight=0.08) 
Behavioral_event_entry.place(relx=0.47, rely=0.19, relwidth=0.2, relheight=0.09)   
Extraction_to_label.place(relx=0.555, rely=0.37, relwidth=0.03, relheight=0.04)
Extraction_label.place(relx=0.02, rely=0.36, relwidth=0.41, relheight=0.07)  
Extraction_pre_entry.place(relx=0.47, rely=0.36, relwidth=0.07, relheight=0.07)
Extraction_post_entry.place(relx=0.61, rely=0.36, relwidth=0.07, relheight=0.08)
base_label.place(relx=0.02, rely=0.48, relwidth=0.39, relheight=0.08)
base_pre_entry.place(relx=0.47, rely=0.48, relwidth=0.07, relheight=0.07)
base_post_entry.place(relx=0.61, rely=0.48, relwidth=0.07, relheight=0.07)
base_to_label.place(relx=0.555, rely=0.49, relwidth=0.03, relheight=0.04)
Title_entry.place(relx=0.47, rely=0.60, relwidth=0.21, relheight=0.07)
Title_entry_label.place(relx=0.20, rely=0.61, relwidth=0.20, relheight=0.04)

### Blocking code after .mainloop until mGui has been destroyed and quitted
mGui.mainloop()

### Variables for analysis
Start = 5

### Getting paths using pathlibs Path function
path_to_experiment = Path(path_to_experiment)
path_str = str(path_to_experiment)

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
            
            Entry_legend_name_sensor_1_label.place(relx=0.05, rely=0.59, relwidth=0.37, relheight=0.12)
            Entry_legend_name_sensor_2_label.place(relx=0.05, rely=0.78, relwidth=0.37, relheight=0.12)
            Entry_legend_name_sensor_1.place(relx=0.53, rely=0.62, relwidth=0.25, relheight=0.065)
            Entry_legend_name_sensor_2.place(relx=0.53, rely=0.81, relwidth=0.25, relheight=0.065)
                                                            
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
        Exit_Button.place(relx=0.31, rely=0.89, relwidth=0.3, relheight=0.10)


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
    Timevectors_calcium_dependent_lst.append(Timevectors_calcium_dependent)
    
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
Corrected_calcium_dependent_lst.append()

for calcium_independent, calcium_dependent in zip(calcium_independent_signal_lst, calcium_dependent_signal_lst):

    
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
    ### firstly higher than the time point of the behavioral event - the start time of the total extraction range AND lower than the time point of the behavioral event + the end time of the total extraction range.  
    ### Why the first condition "(timevector_calcium_dependent > (Time_of_event + Extraction_range[0] - 5))" in the np.where function also includes a - 5 subtraction is because we want to get 5-seconds before 
    ### the user specified extraction range to plot as the starting position in the animation. 
    
    index_for_behavioral_event = np.where((timevector_calcium_dependent > (Time_of_event + Extraction_range[0] - 5)) & ((timevector_calcium_dependent < Time_of_event + Extraction_range[1])))
    
    ### These indeces are thereafter used to select the signal data points in the corrected calcium dependent signal.
    ### This works since the timevector and the corrected calcium signal share the same indices.
    ### To explain it a bit further, to find the signal corresponding to a specific time point in the timevector, 
    ### you only need to use the index of that time data point in the signal vector.    
    Neural_activity_for_behavioral_event = Corrected_calcium_dependent[index_for_behavioral_event]
    
    ### Creating a timevector for the behavioral event. 
    ### Yet again, this includes the -5 subtraction for the initial plotted 5-second neural activity in the animation.
    Timevector_for_behavioral_event = Extraction_range[0] - 5 + np.linspace(1, len(Neural_activity_for_behavioral_event), len(Neural_activity_for_behavioral_event))/ Sampling_rate_calcium_dependent[i]
    
    

    
    ind_baseline = np.where((Timevector_beh_event > Baseline[0]) & (Timevector_beh_event < Baseline[1]))
    Z_score_event = (Neural_activity_event - Neural_activity_event[ind_baseline].mean()) / Neural_activity_event[ind_baseline].std()
    
    min_index = np.where(Timevector_beh_event > Extraction_range[0])[0].min()
    
    
    
    ### Appending to lists
    Timevectors_for_behavioral_events_lst.append(Timevector_for_behavioral_event)
    Index_for_start_recording.append(min_index)
    Z_score_events_lst.append(Z_score_event)
    
min_z_score = np.min([len(Z_score) for Z_score in Z_score_events_lst])
Z_score_events_lst = [Z_score[:min_z_score] for Z_score in Z_score_events_lst]


start_time = time1.time()

plt.plot(Timevector_beh_event ,Z_score_event)

matplotlib.rcParams['animation.ffmpeg_path'] = r"C:\Users\aboo_\Desktop\ffmpeg.exe"

### initiate figure
fig, axes = plt.subplots(nrows = 1, ncols = 1, figsize = (10,8))
axes.set_ylim(-2, 4.0)

Num_frames = int(len(Z_score_events_lst[0][Index_for_start_recording[0]:]) / 50)
#axes.yaxis.set_major_locator(loc)
#axes.xaxis.set_major_locator(loc)
axes.spines["right"].set_visible(False)
axes.spines["top"].set_visible(False)
#axes.spines["bottom"].set_visible(False)
axes.set_ylabel("Z-score", fontsize=25, labelpad=15)

axes.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False)

axes.tick_params(
    axis="y",
    which="major",
    labelsize="20")

time = [Timevectors_beh_events_lst[0][:Index_for_start_recording[0]]]
time = list(np.ravel(time))

z_score_y_value = [Z_score_events_lst[0][:Index_for_start_recording[0]]]
z_score_y_value = list(np.ravel(z_score_y_value))

Start = Extraction_range[0] -5
End = Extraction_range[0] -5 + 10
axes.set_xlim(Start, End)


line, = axes.plot([Timevectors_beh_events_lst[0][:Index_for_start_recording[0]]], [Z_score_events_lst[0][:Index_for_start_recording[0]]]], lw=2)

def animate(i):
    
    global Start
    global End
    global Time_video



    lien = 
    z_score_y_value.append((Z_score_events_lst[0][Index_for_start_recording[0] + (i*50)]))
    time.append(Timevectors_beh_events_lst[0][Index_for_start_recording[0] + (i*50)])

    Start += Timevectors_beh_events_lst[0][Index_for_start_recording[0] + (i*50)] - Timevectors_beh_events_lst[0][Index_for_start_recording[0] + ((i-1)*50)]
    End += Timevectors_beh_events_lst[0][Index_for_start_recording[0] + (i*50)] - Timevectors_beh_events_lst[0][Index_for_start_recording[0] + ((i-1)*50)]
    axes.set_xlim(Start, End)

    #axes.yaxis.set_major_locator(loc)
    axes.plot(time, z_score_y_value, color="green", linewidth=3)

anim = FuncAnimation(fig, func=animate, frames=int(Num_frames), interval=20, blit=True)
FFwriter=animation.FFMpegWriter(fps=int(Num_frames/abs(Extraction_range[1]-(Extraction_range[0]))), bitrate=2000)
anim.save(r'C:/Users/aboo_/Desktop/basic_animation.mp4', writer=FFwriter, dpi = 500)

end_time = time1.time()

elapsed_time = end_time - start_time
print("Time taken: ", elapsed_time)    
    
    
    
    