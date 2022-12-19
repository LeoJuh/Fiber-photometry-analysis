import sys
import tkinter as tk
from tkinter import filedialog
import pathlib
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
import tdt
import re
import math
from sklearn.metrics import auc 
from itertools import zip_longest
import csv

def browse_directory():
    
    """This function allows the user to select the path 
    containing all subject tdt files in one experiment"""
    
    global folder_selected
    global path_to_experiment
    folder_selected = filedialog.askdirectory()
    Text_path.insert(0, f"{folder_selected}")
    path_to_experiment = Text_path.get()
    
def show_parameters_import():
    
    """This function allows the user to import behavioral
    timestamps and perform perievent analysis. Options for statistical
    analysis of perievent neuronal activity will be displayed with the execution
    of this function"""
    
    
    def AUC_analysis():
        
        """This function enables the user to use AUC analysis, and 
        insert the settings for this type of analysis"""
          
        global AUC_pre_1
        global AUC_pre_2
        global AUC_post_1
        global AUC_post_2

        AUC_pre_1 = tk.Entry(mGui)
        AUC_pre_2 = tk.Entry(mGui)
        AUC_pre_1.place(relx=0.40, rely=0.54, relwidth=0.05, relheight=0.04)
        AUC_pre_2.place(relx=0.50, rely=0.54, relwidth=0.05, relheight=0.04)
        AUC_to_label_1 = tk.Label(mGui, text="to", font=("Arial", 10))
        AUC_to_label_1.place(relx=0.46, rely=0.54, relwidth=0.03, relheight=0.04)
        AUC_to_label_2 = tk.Label(mGui, text="to", font=("Arial", 10))
        AUC_to_label_2.place(relx=0.71, rely=0.54, relwidth=0.03, relheight=0.04)
        AUC_post_1 = tk.Entry(mGui)
        AUC_post_2 = tk.Entry(mGui)
        AUC_post_1.place(relx=0.65, rely=0.54, relwidth=0.05, relheight=0.04)
        AUC_post_2.place(relx=0.75, rely=0.54, relwidth=0.05, relheight=0.04)
        
    def Zex_analysis():
        
        """This function enables the user to use z-extreme analysis, and 
        insert the settings for this type of analysis"""

        global zex_pre_1
        global zex_pre_2
        global zex_post_1
        global zex_post_2
        global Z_max
        global Z_min
        
        zex_pre_1 = tk.Entry(mGui)
        zex_pre_2 = tk.Entry(mGui)
        zex_pre_1.place(relx=0.40, rely=0.64, relwidth=0.05, relheight=0.04)
        zex_pre_2.place(relx=0.50, rely=0.64, relwidth=0.05, relheight=0.04)
        zex_to_label_1 = tk.Label(mGui, text="to", font=("Arial", 10))
        zex_to_label_1.place(relx=0.46, rely=0.64, relwidth=0.03, relheight=0.04)
        zex_post_1 = tk.Entry(mGui)
        zex_post_2 = tk.Entry(mGui)
        zex_post_1.place(relx=0.65, rely=0.64, relwidth=0.05, relheight=0.04)
        zex_post_2.place(relx=0.75, rely=0.64, relwidth=0.05, relheight=0.04)
        zex_to_label_2 = tk.Label(mGui, text="to", font=("Arial", 10))
        zex_to_label_2.place(relx=0.71, rely=0.64, relwidth=0.03, relheight=0.04)
        z_max_or_min_label = tk.Label(mGui, text="Calculate Z-max or Z-min?", font=("Arial", 10), anchor="w")
        z_max_or_min_label.place(relx=0.03, rely=0.72, relwidth=0.31, relheight=0.04)    
        Z_max = tk.BooleanVar()
        Z_min = tk.BooleanVar()
        Checkbox_Z_min = tk.Checkbutton(mGui, 
                                      text = "Z-min",
                                      variable = Z_min,
                                      onvalue=True,
                                      offvalue=False)
        Checkbox_Z_min.place(relx=0.365, rely=0.72, relwidth=0.30, relheight=0.06)
        Checkbox_Z_max = tk.Checkbutton(mGui, 
                                      text = "Z-max",
                                      variable = Z_max,
                                      onvalue=True,
                                      offvalue=False)
        Checkbox_Z_max.place(relx=0.62, rely=0.72, relwidth=0.30, relheight=0.06)
        
    def average_z_score():
       
        """This function enables the user to use average Z-score analysis, and 
        insert the settings for this type of analysis"""             

        global avg_pre_1
        global avg_pre_2
        global avg_post_1
        global avg_post_2
    
        avg_pre_1 = tk.Entry(mGui)
        avg_pre_2 = tk.Entry(mGui)
        avg_pre_1.place(relx=0.40, rely=0.81, relwidth=0.05, relheight=0.04)
        avg_pre_2.place(relx=0.50, rely=0.81, relwidth=0.05, relheight=0.04)
        avg_to_label_1 = tk.Label(mGui, text="to", font=("Arial", 10))
        avg_to_label_1.place(relx=0.45, rely=0.81, relwidth=0.05, relheight=0.04)
        avg_post_1 = tk.Entry(mGui)
        avg_post_2 = tk.Entry(mGui)
        avg_post_1.place(relx=0.65, rely=0.81, relwidth=0.05, relheight=0.04)
        avg_post_2.place(relx=0.75, rely=0.81, relwidth=0.05, relheight=0.04)
        avg_to_label_2 = tk.Label(mGui, text="to", font=("Arial", 10))
        avg_to_label_2.place(relx=0.70, rely=0.81, relwidth=0.05, relheight=0.04)    
    

    global AUC_analysis_bool
    global Zex_analysis_bool
    global Average_analysis_bool
    global Range_pre
    global Range_post
    global base_pre
    global base_post
    global Stimuli
     
    Stimuli = tk.Entry(mGui)
    Stimuli.place(relx=0.57, rely=0.12, relwidth=0.28, relheight=0.04)  
    label_Stimuli = tk.Label(mGui, text="Enter stimuli here:", font=("Arial", 10), anchor="e")
    label_Stimuli.place(relx=0.35, rely=0.12, relwidth=0.22, relheight=0.04)
    Range_label = tk.Label(mGui, text="Enter range to extract here:", font=("Arial", 10), anchor="w")   
    Range_label.place(relx=0.35, rely=0.18, relwidth=0.34, relheight=0.04)
    Range_to_label = tk.Label(mGui, text="to", font=("Arial", 10))
    Range_to_label.place(relx=0.76, rely=0.18, relwidth=0.03, relheight=0.04)  
    Range_pre = tk.Entry(mGui)
    Range_post = tk.Entry(mGui)
    Range_pre.place(relx=0.69, rely=0.18, relwidth=0.05, relheight=0.04)
    Range_post.place(relx=0.81, rely=0.18, relwidth=0.05, relheight=0.04)
    base_pre = tk.Entry(mGui)
    base_post = tk.Entry(mGui)
    base_pre.place(relx=0.69, rely=0.24, relwidth=0.05, relheight=0.04)
    base_post.place(relx=0.81, rely=0.24, relwidth=0.05, relheight=0.04)
    base_label = tk.Label(mGui, text="Enter baseline time:",font=("Arial", 10), anchor="w")
    base_label.place(relx=0.35, rely=0.24, relwidth=0.34, relheight=0.04)
    base_to_label = tk.Label(mGui, text="to", font=("Arial", 10))
    base_to_label.place(relx=0.76, rely=0.24, relwidth=0.03, relheight=0.04)
    Pre_label = tk.Label(mGui, text="Pre", font=("Arial", 11))    
    Post_label = tk.Label(mGui, text="Post", font=("Arial", 11))
    Pre_label.place(relx=0.425, rely=0.49, relwidth=0.10, relheight=0.04)
    Post_label.place(relx=0.675, rely=0.49, relwidth=0.10, relheight=0.04)
      
      
    # Statistical analysis title
    Stat_section_title = tk.Label(mGui, text="Parameters for statistical analysis", font=("Arial", 13, "bold"))
    Stat_section_title.place(relx=0.2, rely=0.42, relwidth=0.55, relheight=0.04)
    
    ### Setting Boolean variable for statistical measure checkboxes
    AUC_analysis_bool = tk.BooleanVar()
    Zex_analysis_bool = tk.BooleanVar()
    Average_analysis_bool = tk.BooleanVar()

    ### Checkboxes for statistical measures
    Checkbox_AUC = tk.Checkbutton(mGui, 
                                   text = "Use Area under curve?",
                                   command=AUC_analysis, 
                                   variable=AUC_analysis_bool,
                                   onvalue=True,
                                   offvalue=False)
 
    Checkbox_zex = tk.Checkbutton(mGui,
                                  text = "Use Z-extreme?           ",
                                  command=Zex_analysis,
                                  variable=Zex_analysis_bool,
                                  onvalue=True,
                                  offvalue=False)
                                
    Checkbox_average_z_score = tk.Checkbutton(mGui,  
                                              text = "Use Z-score average? ",
                                              command=average_z_score,
                                              variable=Average_analysis_bool,
                                              onvalue=True,
                                              offvalue=False)
    
    Checkbox_AUC.place(relx=0.05, rely=0.53, relwidth=0.30, relheight=0.06)
    Checkbox_zex.place(relx=0.05, rely=0.63, relwidth=0.30, relheight=0.06)
    Checkbox_average_z_score.place(relx=0.05, rely=0.80, relwidth=0.30, relheight=0.06)
    
    
def assign():
    
    global Timestamp_import_bool
    Timestamp_import_bool = Timestamp_import.get()
       
    if Timestamp_import_bool:
        
        global Range_pre
        global Range_post
        global base_pre
        global Range
        global base_post
        global Stimuli
        global Baseline
        global AUC_analysis_bool
        global Zex_analysis_bool
        global Average_analysis_bool
        
         
        base_pre = float(base_pre.get())
        base_post = float(base_post.get()) 
        Baseline = (base_pre, base_post)
        
        Stimuli = Stimuli.get()
        Range_pre = float(Range_pre.get())
        Range_post = float(Range_post.get())
        Range = (Range_pre, Range_post)      

        AUC_analysis_bool = AUC_analysis_bool.get()
        Zex_analysis_bool = Zex_analysis_bool.get()
        Average_analysis_bool = Average_analysis_bool.get()
        
        if AUC_analysis_bool:
            
            global AUC_pre_1
            global AUC_pre_2
            global AUC_post_1
            global AUC_post_2  
            
            AUC_pre_1 = float(AUC_pre_1.get())
            AUC_pre_2 = float(AUC_pre_2.get())
            AUC_post_1 = float(AUC_post_1.get())
            AUC_post_2 = float(AUC_post_2.get())
            
        if Zex_analysis_bool:
            
            global zex_pre_1
            global zex_pre_2
            global zex_post_1
            global zex_post_2
            global Z_max_bool
            global Z_min_bool
            
            zex_pre_1 = float(zex_pre_1.get())
            zex_pre_2 = float(zex_pre_2.get())
            zex_post_1 = float(zex_post_1.get())
            zex_post_2 = float(zex_post_2.get())
            Z_max_bool = Z_max.get()
            Z_min_bool = Z_min.get()
            
        if Average_analysis_bool:
            
            global avg_pre_1
            global avg_pre_2
            global avg_post_1
            global avg_post_2
            
            avg_pre_1 = float(avg_pre_1.get())
            avg_pre_2 = float(avg_pre_2.get())
            avg_post_1 = float(avg_post_1.get())
            avg_post_2 = float(avg_post_2.get())
             
            
    mGui.destroy()
    
mGui = tk.Tk()

global Timestamp_import ### Make the variable upon clicking or not clicking checkbox global

### Objects shown before clicking any checkbox
mGui.geometry("500x500+500+300")
mGui.title("Choosing parameters for FIP analysis")
Text_path = tk.Entry(mGui)
Text_path.place(relx=0.47, rely=0.01, relwidth=0.4, relheight=0.05)
browse_Button = tk.Button(
    mGui, 
    text="Click here to import experiment PATH:", 
    command=browse_directory)


browse_Button.place(relx=0.0, rely=0.01, relwidth=0.45, relheight=0.05)
Exit_Button = tk.Button(mGui, text="Click here to finish", command=assign)
Exit_Button.place(relx=0.35, rely=0.95, relwidth=0.3, relheight=0.05)

Timestamp_import = tk.BooleanVar()

Checkbox_timestamps = tk.Checkbutton(mGui, 
                                     text = "Use timestamps?",
                                     command=show_parameters_import,
                                     variable=Timestamp_import,
                                     onvalue=True,
                                     offvalue=False)

Checkbox_timestamps.place(relx=0.05, rely=0.11, relwidth=0.25, relheight=0.06)


mGui.mainloop()

### Conditions to check
if Timestamp_import_bool:
    
    ### This checks it so that the time range of the range extraction is correct.
    if Range_pre > 0:
        raise Exception("The start point time point of the range extraction time range needs to be less than 0.")
        
    if Range_post < 0:
        raise Exception("The end point time point of the range extraction time range needs to be higher than 0.")
    
    ### This checks that the baseline is within the range
    if Range_pre > base_pre:
        raise Exception("The start time point of the baseline is outside of the extraction time range")
    
    if Range_post < base_post:
        raise Exception("The end time point of the baseline is outside of the extraction time range")
    
    if base_pre > base_post:
        raise Exception("The end time point of the baseline is lower than the baseline start timepoint")
    
    ### This checks that the AUC time ranges are correct
    if AUC_analysis_bool:
             
        if AUC_pre_1 > AUC_pre_2:
            raise Exception("The start time point of the AUC pre time range is higher than the pre AUC end timepoint")
        
        if AUC_post_1 > AUC_post_2:
            raise Exception("The start time point of the AUC post time range is lower than the post AUC end timepoint")
        
        if AUC_post_2 < AUC_pre_1:
            raise Exception("The start timepoint of the AUC pre time range is higher than the post AUC end timepoint")
        
        if AUC_pre_1 < Range_pre:
            raise Exception("The start time point of the AUC pre time range is lower than the pre extraction start timepoint")
         
        if AUC_post_2 > Range_post:
            raise Exception("The end time point of the AUC post time range is higher than the extraction end timepoint")
    
    ### This checks that the Zex time ranges are correct
    if Zex_analysis_bool:
        
        if zex_pre_1 > zex_pre_2:
            raise Exception("The start time point of the Z-extreme pre time range is higher than the pre Z-extreme end timepoint")
        
        if zex_post_1 > zex_post_2:
            raise Exception("The start time point of the Z-extreme post time range is lower than the post Z-extreme end timepoint")
        
        if zex_post_2 < zex_pre_1:
            raise Exception("The start timepoint of the Z-extreme pre time range is higher than the post Z-extreme end timepoint")
        
        if zex_pre_1 < Range_pre:
            raise Exception("The start time point of the Z-extreme pre time range is lower than the extraction start timepoint")
         
        if zex_post_2 > Range_post:
            raise Exception("The end time point of the Z-extreme post time range is higher than extraction end timepoint")    
          
    ### This checks that the Average Z-score time ranges are correct        
    if Average_analysis_bool:
        
        if avg_pre_1 > avg_pre_2:
            raise Exception("The start time point of the Average Z-score pre time range is higher than the pre Z-extreme end timepoint")
        
        if avg_post_1 > avg_post_2:
            raise Exception("The start time point of the Average Z-score post time range is lower than the post Z-extreme end timepoint")
        
        if avg_post_2 < avg_pre_1:
            raise Exception("The start timepoint of the Average Z-score pre time range is higher than the post Z-extreme end timepoint")
        
        if avg_pre_1 < Range_pre:
            rgaise Exception("The start time point of the Average Z-score pre time range is lower than the extraction start timepoint")
         
        if avg_post_2 > Range_post:
            raise Exception("The end time point of the Average Z-score post time range is higher than extraction end timepoint")    
           

# Parameters for analysis
Start = 5
Step_size_plot = 4

# Empty lists and dictionaries
Name_of_subjects_lst = []
Calcium_dependent_signal_lst = []
Calcium_independent_signal_lst = []
Calcium_dependent_frame_rate_lst = []
Calcium_independent_frame_rate_lst = []
Timevector_calcium_independent_lst = []
Timevector_calcium_dependent_lst = []
Behavioral_event_lst = []
Settings_for_analysis = {} # Dictionary where results will be appended to

Paths_to_experiment_files = Path(path_to_experiment).glob("*") # Getting paths to each individual animal

for path in Paths_to_experiment_files:
  
    path_str = str(path)   # path is converted to string  
    Subject_name = re.search("([^\/|^\\\]+$)", path_str).group(0)          # Extracting subject name using regex, where subject name is the subject´s folder name  
             
    try:     
        
        subject_data = tdt.read_block(path_str, t1= Start)                      # Reading data from 5s to end of recording
        Calcium_dependent_signal = subject_data.streams["_465A"].data          # Extracting caldium dependent signal from tdt data file
        Calcium_dependent_signal_lst.append(Calcium_dependent_signal)          # Appending calcium dependent data
        Calcium_independent_signal = subject_data.streams["_405A"].data        # Extracting caldium independent signal from tdt data file
        Calcium_independent_signal_lst.append(Calcium_independent_signal)      # Appending calcium independent data       
        Calcium_dependent_frame_rate = subject_data.streams["_465A"].fs        # Extracting frame rate of calcium dependent signal
        Calcium_dependent_frame_rate_lst.append(Calcium_dependent_frame_rate)  # Appending calcium dependent frame rate     
        Calcium_independent_frame_rate = subject_data.streams["_405A"].fs       # Extracting frame rate of calcium independent signal  
        Calcium_independent_frame_rate_lst.append(Calcium_independent_frame_rate) # Appending calcium independent frame rate 
        Name_of_subjects_lst.append(Subject_name)                                 # Appending subject name

    except:    
            print(f"The {Subject_name} folder was not able to be read by the tdt package.")
            pass 
                            
    if Timestamp_import_bool:                                                   # If stimuli is not false, import it.   
                                                           
        try:
            Behavioral_event_animal = pd.read_csv(f"{path_str}\\Timestamps_{Stimuli}.csv")
            Behavioral_event_lst.append(Behavioral_event_animal)
        except:
            print(f"The timestamp file for the {Subject_name} was not found")                                      

### Generating path to main folder.
path_to_experiment_windows_path = Path(path_to_experiment)
Main_folder = Path.joinpath(path_to_experiment_windows_path, f"Results {path_to_experiment_windows_path.parts[-1]}")

### If the default main folder path already exists, i.e., code has been run before, this 
### code will generate a unique folder name consisting of default name + an integer. 
### Thus, there is an unlimited amount of time in which the code can be run.

if Main_folder.is_dir():
    i = 2
    while Path.joinpath(path_to_experiment_windows_path,f"Results {path_to_experiment_windows_path.parts[-1]} ({i})").is_dir():
        i += 1
    Main_folder = Path.joinpath(path_to_experiment_windows_path, f"Results {path_to_experiment_windows_path.parts[-1]} ({i})")

Main_folder.mkdir(parents=True)
Figures_path = Path.joinpath(Main_folder, "Figures of entire recordings")
Figures_path.mkdir(parents=True) 

if Timestamp_import_bool:
    Data_path = Path.joinpath(Main_folder, f"Output perievent {Stimuli} analysis")
    Data_path.mkdir(parents=True)
    Figures_perievent = Path.joinpath(Data_path, "Figures")
    Figures_perievent.mkdir(parents=True)    
    Data_perievent = Path.joinpath(Data_path, "Data")  
    Data_perievent.mkdir(parents=True)

# Creating time vectors for calcium independent and calcium dependent signals

for calcium_dependent_signal, calcium_independent_signal, calcium_dependent_frame_rate, calcium_independent_frame_rate  in zip(Calcium_dependent_signal_lst, Calcium_independent_signal_lst, Calcium_dependent_frame_rate_lst, Calcium_independent_frame_rate_lst):
    
    calcium_dependent_time_vector = Start + np.linspace(1, len(calcium_dependent_signal), len(calcium_dependent_signal))/calcium_dependent_frame_rate          # Creating timevector for calcium dependent signal
    Timevector_calcium_dependent_lst.append(calcium_dependent_time_vector)                                                                                     # Appending calcium dependent time vector 
    calcium_independent_time_vector = Start + np.linspace(1, len(calcium_independent_signal), len(calcium_independent_signal))/calcium_independent_frame_rate  # Creating timevector for calcium_independent signal
    Timevector_calcium_independent_lst.append(calcium_independent_time_vector)                                                                                 # Appending calcium independent time vector
    
# Plotting raw signals
Jump_ind = 0

for i in range(math.ceil(len(Name_of_subjects_lst)/4)):  

    fig_raw_signal, axs_raw_signal = plt.subplots(4,1, figsize=(16,16)) ### Generating figure object with subplots
    
    for j, ax in enumerate(axs_raw_signal):
        
        if j + Jump_ind + 1 > len(Name_of_subjects_lst):
            break
        else:
            calcium_dependent_signal_plot = Calcium_dependent_signal_lst[j+Jump_ind] - Calcium_dependent_signal_lst[j+Jump_ind].mean(axis=0)       # Subtracting the signal with its mean to overlay it with the calcium independent for plotting
            calcium_independent_signal_plot = Calcium_independent_signal_lst[j+Jump_ind] - Calcium_independent_signal_lst[j+Jump_ind].mean(axis=0) # Subtracting the signal with its mean to overlay it with the calcium dependent for plotting
            ax.plot(Timevector_calcium_dependent_lst[j+Jump_ind], calcium_dependent_signal_plot, color="green", label="Calcium dependent")        # Plotting calcium dependent signal
            ax.plot(Timevector_calcium_independent_lst[j+Jump_ind], calcium_independent_signal_plot, color="purple", label="Calcium independent") # Plotting calcium independent signal
            ax.set_title(f"{Name_of_subjects_lst[j+Jump_ind]} raw signals", fontsize=30)
            ax.set_ylabel("mV", fontsize=25)
            ax.set_xlabel("Time (s)", fontsize=25)
            ax.tick_params(axis="both", which="major", labelsize=17)
            ax.legend(fontsize=20, loc="upper right")
        
    fig_raw_signal.tight_layout()
    Path_to_export_figures = Path.joinpath(Figures_path, f"Raw_signal subjects {Jump_ind} - {Jump_ind+4} .tiff")
    fig_raw_signal.savefig(Path_to_export_figures)
    
    Jump_ind += 4   

# Correcting calcium dependent with calcium independent signal.

Correct_calcium_dep_lst = []
Calcium_independent_fitted_lst = []

for calcium_independent_signal, calcium_dependent_signal in zip(Calcium_independent_signal_lst, Calcium_dependent_signal_lst): 
    fitting_independent_to_dependent = np.polyfit(calcium_independent_signal, calcium_dependent_signal, 1) ### Using polyfit to the second degree
    fit_line_independent_to_dependent = np.multiply(fitting_independent_to_dependent[0], calcium_independent_signal) + fitting_independent_to_dependent[1]
    Corrected_calcium_dependent = calcium_dependent_signal - fit_line_independent_to_dependent
    Calcium_independent_fitted_lst.append(fit_line_independent_to_dependent)
    Correct_calcium_dep_lst.append(Corrected_calcium_dependent)

Jump_ind = 0

# Plotting fitted calcium independent signal

for i in range(math.ceil(len(Name_of_subjects_lst)/4)):  

    fig_raw_signal, axs_raw_signal = plt.subplots(4,1, figsize=(16,16)) ### Generating figure object with subplots
    
    for j, ax in enumerate(axs_raw_signal):
        
        if j + Jump_ind + 1 > len(Name_of_subjects_lst):
            break
        else:
            
            ax.plot(Timevector_calcium_dependent_lst[j+Jump_ind], Calcium_dependent_signal_lst[j+Jump_ind], color="green", label="Calcium dependent")        # Plotting calcium dependent signal
            ax.plot(Timevector_calcium_independent_lst[j+Jump_ind], Calcium_independent_fitted_lst[j+Jump_ind], color="Blue", label="Fitted calcium independent") # Plotting calcium independent signal
            ax.set_title(f"{Name_of_subjects_lst[j+Jump_ind]} raw signals", fontsize=30)
            ax.set_ylabel("mV", fontsize=25)
            ax.set_xlabel("Time (s)", fontsize=25)
            ax.tick_params(axis="both", which="major", labelsize=17)
            ax.legend(fontsize=20, loc="upper right")
        
    fig_raw_signal.tight_layout()
    Path_to_export_figures = Path.joinpath(Figures_path, f"Fitted calcium independent signal, subjects {Jump_ind} - {Jump_ind+4} .tiff")
    fig_raw_signal.savefig(Path_to_export_figures)
    Jump_ind += 4   

if Timestamp_import_bool: ### This will perform the perievent analysis, but only if you clicked the "Use timestamps?" checkbox.
    
    
    ### Extracting the neural activity surrounding each behavioral event
    Z_score_of_neural_activity_surrounding_events = [[] for animal in Correct_calcium_dep_lst] # Creating 2D list with sublist for each animal in Correct_calcium_dep_lst
    
    for i, (signal_animal, timestamps_animal, timevector_animal) in enumerate(zip(Correct_calcium_dep_lst, Behavioral_event_lst, Timevector_calcium_dependent_lst)):
      
      for j, behavioral_event in timestamps_animal.iterrows():
        ### Checking if event timestamps are not too close to the begininning or end of the video
        if ((behavioral_event.values[0]-Range[0]) > Start) & ((behavioral_event.values[0]+Range[1]) < timevector_animal[-1]): 
    
          ### select indices around event. The range around event is determined by extract.
          index_for_event = np.where((timevector_animal > (behavioral_event.values[0]+Range[0])) & (timevector_animal < (behavioral_event.values[0]+Range[1])))[0] ### Selecting the indices which correspond to the time surrounding the behavioral event
          Neural_activity_for_behavioral_event = signal_animal[index_for_event]
     
          # Z-scoring the neural activity 
          
          index_for_baseline = np.where((timevector_animal > (behavioral_event.values[0]+Baseline[0])) & ((behavioral_event.values[0]+Baseline[1]) < timevector_animal))
          Neural_activity_of_baseline = signal_animal[index_for_baseline]
          Z_score = (Neural_activity_for_behavioral_event - Neural_activity_of_baseline.mean()) / Neural_activity_of_baseline.std()                                
          Z_score_of_neural_activity_surrounding_events[i].append(Z_score)

    ### Making sure all the perievents have same length and makign a final timevector to use
    ### for all perievents. 

    ### This collects the minimum trial length for each animal
    min_perievent_length_animal = []

    for animal_peri_event_signals in Z_score_of_neural_activity_surrounding_events:
        min_peri_event_length = np.min([np.size(peri_event) for peri_event in animal_peri_event_signals])
        min_perievent_length_animal.append(min_peri_event_length)

    ### This collects the minimum trial length of all animals
    total_min_peri_event = np.min(min_perievent_length_animal)

    ### This trims down the lengths of all trials to the shortest trial length
    ### ofall animals
    for i, animal_peri_event_signals in enumerate(Z_score_of_neural_activity_surrounding_events):
        animal_peri_event_signals = [peri_event[:total_min_peri_event] for peri_event in animal_peri_event_signals]
        Z_score_of_neural_activity_surrounding_events[i] = animal_peri_event_signals

    ### This creates a timevector based on the trimmed trials
    ### This has the same length as all trials  
    Timevec_peri_event_final = Range[0] + np.linspace(1, len(Z_score_of_neural_activity_surrounding_events[0][0]), len(Z_score_of_neural_activity_surrounding_events[0][0]))/Calcium_dependent_frame_rate_lst[0]

    Z_score_averaged_neural_activity = []
    
    ### All the values extracted for statistical analysis will be appended
    ### to this dictionary
    Statistical_analysis = {"Subjects":Name_of_subjects_lst, 
                            "AUC-pre": [], 
                            "AUC-post":[], 
                            "Z-min pre":[],
                            "Z-min post": [],
                            "Z-max pre":[],
                            "Z-max post":[],
                            "Average-pre":[],
                            "Average-post":[],
                            }
    
    for i, z_score_animal_all_trials in enumerate(Z_score_of_neural_activity_surrounding_events):
        
        z_score_animal_avg = np.mean(z_score_animal_all_trials, axis=0) ### Avearing all trials within each animal
        Z_score_averaged_neural_activity.append(z_score_animal_avg)
        
        if AUC_analysis_bool:
            
            index_pre_AUC = np.where((Timevec_peri_event_final > AUC_pre_1) & (AUC_pre_2 < Timevec_peri_event_final))
            index_post_AUC = np.where((Timevec_peri_event_final > AUC_post_1) & (AUC_post_2 < Timevec_peri_event_final)) 
            AUC_pre  = auc(Timevec_peri_event_final[index_pre_AUC], z_score_animal_avg[index_pre_AUC])
            AUC_post = auc(Timevec_peri_event_final[index_post_AUC], z_score_animal_avg[index_post_AUC])
            Statistical_analysis["AUC-pre"].append(AUC_pre)
            Statistical_analysis["AUC-post"].append(AUC_post)
            Settings_for_analysis["AUC time range (s)"] = [f"Pre: {AUC_pre_1} to {AUC_pre_2}", f"Post: {AUC_post_1} to {AUC_post_2}"]
            
        if Zex_analysis_bool:
            
            index_pre_zex = np.where((Timevec_peri_event_final > zex_pre_1) & (zex_pre_2 < Timevec_peri_event_final))
            index_post_zex = np.where((Timevec_peri_event_final > zex_post_1) & (zex_post_2 < Timevec_peri_event_final))
            
            ### Getting the minimum or the maximum of the Z-score within the specified time ranged,
            ### dependent on whether the z-min or z-max checkbox was checked.
            
            if Z_min_bool:
                
                Z_min_pre = z_score_animal_avg[index_pre_zex].min()
                Z_min_post = z_score_animal_avg[index_post_zex].min()
                
                Statistical_analysis["Z-min pre"].append(Z_min_pre)
                Statistical_analysis["Z-min post"].append(Z_min_post)
                Settings_for_analysis["Z-min time range(s)"] = [f"Pre: {zex_pre_1} to {zex_pre_2}", f"Post: {zex_post_1} to {zex_post_2}"]
                
            if Z_max_bool:
                
                Z_max_pre = z_score_animal_avg[index_pre_zex].max()
                Z_max_post = z_score_animal_avg[index_pre_zex].max()
                
                Statistical_analysis["Z-max pre"].append(Z_max_pre)
                Statistical_analysis["Z-max post"].append(Z_max_post)
                Settings_for_analysis["Z-max time range(s)"] = [f"Pre: {zex_pre_1} to {zex_pre_2}", f"Post: {zex_post_1} to {zex_post_2}"]
            
                
        if Average_analysis_bool:
            
            index_pre_avg = np.where((Timevec_peri_event_final > avg_pre_1) & (avg_pre_2 < Timevec_peri_event_final))
            index_post_avg = np.where((Timevec_peri_event_final > avg_post_1) & (avg_post_2 < Timevec_peri_event_final))
            
            Z_score_avg_pre = z_score_animal_avg[index_pre_avg].mean()
            Z_score_avg_post = z_score_animal_avg[index_post_avg].mean()
            
            Statistical_analysis["Average-pre"].append(Z_score_avg_pre)
            Statistical_analysis["Average-post"].append(Z_score_avg_post)
            
            Settings_for_analysis["Average Z-score time range (s)"] = [f"Pre: {avg_pre_1} to {avg_pre_2}", f"Post: {avg_post_1} to {avg_post_2}"]
            
    Jump_ind = 0
    
    for i in range(math.ceil(len(Name_of_subjects_lst)/4)):  

        fig_peri_event_signal, axs_peri_event_signal = plt.subplots(4,1, figsize=(16,16)) ### Generating figure object with subplots
        
        for j, ax in enumerate(axs_peri_event_signal):
            
            if j + Jump_ind + 1 > len(Name_of_subjects_lst):
                break
            else:
                
                ax.plot(Timevec_peri_event_final, Z_score_averaged_neural_activity[j+Jump_ind], color="green")        # Plotting calcium dependent signal
                ax.set_title(f"{Name_of_subjects_lst[j+Jump_ind]}", fontsize=30)
                ax.set_ylabel(f"Z-score", fontsize=25)
                ax.set_xlabel("Time (s)", fontsize=25)
                ax.tick_params(axis="both", which="major", labelsize=17)
            
        fig_peri_event_signal.tight_layout()
        Path_for_exporting_peri_event_signals_all_subjects = Path.joinpath(Figures_perievent, f"Perievent signal subjects {Jump_ind} - {Jump_ind+4} .tiff")  
        fig_peri_event_signal.savefig(Path_for_exporting_peri_event_signals_all_subjects)
        Jump_ind += 4   

    ### Averaging all animals together and plotting the averaged activity.
    Z_score_averaged_completely = np.mean(Z_score_averaged_neural_activity, axis=0)
    fig_all_averaged = plt.figure(figsize=(15,8))     
    ax_fig_all_averaged = plt.subplot(111)

    ax_fig_all_averaged.plot(Timevec_peri_event_final, Z_score_averaged_completely, color="green")
    ax_fig_all_averaged.set_title(f"Single trace", fontsize=30)
    ax_fig_all_averaged.set_ylabel(f"Z-score", fontsize=25)
    ax_fig_all_averaged.set_xlabel("Time (s)", fontsize=25)
    ax_fig_all_averaged.spines.right.set_visible(False)
    ax_fig_all_averaged.spines.top.set_visible(False)
    ax_fig_all_averaged.tick_params(axis="both", which="major", labelsize=17)
    Path_for_exporting_sinle_averaged_trace = Path.joinpath(Figures_perievent, "Perievent single trace.tiff")
    plt.savefig(Path_for_exporting_sinle_averaged_trace, dpi=200)
         
    

    ### Appending settings to dictionary
    Settings_for_analysis["Baseline time range (s)"] = [f"{Baseline[0]} to {Baseline[1]}"]
    Settings_for_analysis["Extraction time range (s)"] = [f"{Range[0]} to {Range[1]}"]
    Settings_for_analysis["Number of animals"] = [len(Name_of_subjects_lst)]
    Settings_for_analysis["Trials per subject"] = [f"{subject}:{len(Peri_event_animal)} trials" for subject, Peri_event_animal in zip(Name_of_subjects_lst, Z_score_of_neural_activity_surrounding_events)]
    Settings_for_analysis["Stimuli"] = [Stimuli]
    
    ### Making values in dictionary same length so the dict can be exported to csvs using Pandas Dataframe
    
    Settings_for_analysis_max_length = max([len(v) for v in Settings_for_analysis.values()]) # Finding column with the highest length

    for key, values in Settings_for_analysis.items():
        if len(values) < Settings_for_analysis_max_length: # If a column has lower number of values then max length, then this code will fill with NaNs until it has the same length.
            while len(values) < Settings_for_analysis_max_length:
                Settings_for_analysis[key].append(np.nan)
    
    Settings_for_analysis_pd = pd.DataFrame(Settings_for_analysis)
    Path_to_export_settings_for_analysis = Path.joinpath(Data_perievent, f"Settings for peri event analysis.csv")
    Settings_for_analysis_pd.to_csv(Path_to_export_settings_for_analysis, index=False)
    
    # Exporting statistical analysis
    Statistical_analysis_filtered = {k:v for k, v in Statistical_analysis.items() if len(v) > 0}
    Statistical_analysis_pd = pd.DataFrame(Statistical_analysis_filtered)
    Path_to_export_statistical_analysis = Path.joinpath(Data_perievent, "Statistical_analysis.csv")  
    Statistical_analysis_pd.to_csv(Path_to_export_statistical_analysis, index=False)
        
    # Exporting perievents for individual animals
    Perievent_individual_animals_dict = {Subject:Perievent for Subject, Perievent in zip(Name_of_subjects_lst, Z_score_averaged_neural_activity)}
    Perievent_individial_animals_pd = pd.DataFrame(Perievent_individual_animals_dict)
    Perievent_individial_animals_pd.insert(0, "Seconds", Timevec_peri_event_final)
    Path_to_export_perievents_for_individual_animals = Path.joinpath(Data_perievent, "Perievent_individual_animals.csv")  
    Perievent_individial_animals_pd.to_csv(Path_to_export_perievents_for_individual_animals, index=False)
    
    ### Exporting perievents averaged across all animals
    Perievent_averaged_across_animals_dict = {Subject:Perievent for Subject, Perievent in zip(Name_of_subjects_lst, Z_score_averaged_neural_activity)}
    Perievent_averaged_across_animals_pd = pd.DataFrame(Perievent_averaged_across_animals_dict)
    Perievent_averaged_across_animals_pd.insert(0, "Seconds", Timevec_peri_event_final)
    Path_to_export_averaged_peri_event_trace = Path.joinpath(Data_perievent, f"Perievent averaged trace.csv")
    Perievent_averaged_across_animals_pd.to_csv(Path_to_export_averaged_peri_event_trace, index=False)

 
    