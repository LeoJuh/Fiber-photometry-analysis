import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
import tdt
import re
import math
from sklearn.metrics import auc
import warnings 

def browse_directory():
    
    """This function allows the user to select the path 
    containing all subject tdt files in one experiment. This function
    is executed when the "Click here to import experimental PATH" button is
    pressed."""
    
    global folder_selected
    global path_to_experiment
    folder_selected = filedialog.askdirectory()
    Text_path.insert(0, f"{folder_selected}")
    path_to_experiment = Text_path.get()
    
def AUC_analysis():
    
    """This function enables the user to use AUC analysis, and 
    insert the settings for this type of analysis. This function
    is executed when the "Use Area under Curve?" checkbutton is filled."""
     
    global AUC_pre_1_entry
    global AUC_pre_2_entry
    global AUC_post_1_entry
    global AUC_post_2_entry

    ### Creating AUC time range entry boxes
    AUC_pre_1_entry = tk.Entry(mGui)
    AUC_pre_2_entry = tk.Entry(mGui)
    AUC_post_1_entry = tk.Entry(mGui)
    AUC_post_2_entry = tk.Entry(mGui)

    ### Creating AUC labels
    AUC_to_label_1 = tk.Label(mGui, text="to", font=("Arial", 10))
    AUC_to_label_2 = tk.Label(mGui, text="to", font=("Arial", 10))     

    ### Placing all labels and boxes
    AUC_pre_1_entry.place(relx=0.40, rely=0.54, relwidth=0.05, relheight=0.04)
    AUC_pre_2_entry.place(relx=0.50, rely=0.54, relwidth=0.05, relheight=0.04)
    AUC_post_1_entry.place(relx=0.65, rely=0.54, relwidth=0.05, relheight=0.04)
    AUC_post_2_entry.place(relx=0.75, rely=0.54, relwidth=0.05, relheight=0.04)
    AUC_to_label_1.place(relx=0.46, rely=0.54, relwidth=0.03, relheight=0.04)
    AUC_to_label_2.place(relx=0.71, rely=0.54, relwidth=0.03, relheight=0.04)
    
def Zex_analysis():
    
    """This function enables the user to use z-extreme analysis, and 
    insert the settings for this type of analysis. This function
    is executed when the "Use Z-extreme?" checkbutton is filled."""

    global zex_pre_1_entry
    global zex_pre_2_entry
    global zex_post_1_entry
    global zex_post_2_entry
    global Z_max
    global Z_min
    
    ### Creating Z-extreme time range entry boxes
    zex_pre_1_entry = tk.Entry(mGui)
    zex_pre_2_entry = tk.Entry(mGui)
    zex_post_1_entry = tk.Entry(mGui)
    zex_post_2_entry = tk.Entry(mGui)

    ### Creating labels
    zex_to_label_1 = tk.Label(mGui, text="to", font=("Arial", 10))      
    zex_to_label_2 = tk.Label(mGui, text="to", font=("Arial", 10))
    z_max_or_min_label = tk.Label(mGui, text="Calculate Z-max or Z-min?", font=("Arial", 10), anchor="w")
   


    ### Creating Boolean variables for check boxes.
    Z_max = tk.BooleanVar()
    Z_min = tk.BooleanVar()
    
    ### Creating Z-min checkbox
    Checkbox_Z_min = tk.Checkbutton(mGui, 
                                  text = "Z-min",
                                  variable = Z_min,
                                  onvalue=True,
                                  offvalue=False)
    
    ### Creating Z-max checkbox
    Checkbox_Z_max = tk.Checkbutton(mGui, 
                                  text = "Z-max",
                                  variable = Z_max,
                                  onvalue=True,
                                  offvalue=False)

    ### Placing entry boxes, check boxes and labels
    z_max_or_min_label.place(relx=0.03, rely=0.72, relwidth=0.31, relheight=0.04) 
    zex_pre_1_entry.place(relx=0.40, rely=0.64, relwidth=0.05, relheight=0.04)
    zex_pre_2_entry.place(relx=0.50, rely=0.64, relwidth=0.05, relheight=0.04)
    zex_post_1_entry.place(relx=0.65, rely=0.64, relwidth=0.05, relheight=0.04)
    zex_post_2_entry.place(relx=0.75, rely=0.64, relwidth=0.05, relheight=0.04)
    zex_to_label_2.place(relx=0.71, rely=0.64, relwidth=0.03, relheight=0.04)
    zex_to_label_1.place(relx=0.46, rely=0.64, relwidth=0.03, relheight=0.04)
    Checkbox_Z_min.place(relx=0.365, rely=0.72, relwidth=0.30, relheight=0.06)
    Checkbox_Z_max.place(relx=0.62, rely=0.72, relwidth=0.30, relheight=0.06)
    
def average_z_score():
   
    """This function enables the user to use average Z-score analysis, and 
    insert the settings for this type of analysis. This function
    is executed when the "Use Average Z-score" checkbutton is filled."""             

    global avg_pre_1_entry
    global avg_pre_2_entry
    global avg_post_1_entry
    global avg_post_2_entry

    ### Creating Average Z-score time range entry boxes
    avg_pre_1_entry = tk.Entry(mGui)
    avg_pre_2_entry = tk.Entry(mGui)
    avg_post_1_entry = tk.Entry(mGui)
    avg_post_2_entry = tk.Entry(mGui)
 
    ### Creating labels
    avg_to_label_1 = tk.Label(mGui, text="to", font=("Arial", 10))
    avg_to_label_2 = tk.Label(mGui, text="to", font=("Arial", 10))
        
    ### Placing entry boxes and labels        
    avg_to_label_1.place(relx=0.45, rely=0.81, relwidth=0.05, relheight=0.04)
    avg_post_1_entry.place(relx=0.65, rely=0.81, relwidth=0.05, relheight=0.04)
    avg_post_2_entry.place(relx=0.75, rely=0.81, relwidth=0.05, relheight=0.04)
    avg_to_label_2.place(relx=0.70, rely=0.81, relwidth=0.05, relheight=0.04)    
    avg_pre_1_entry.place(relx=0.40, rely=0.81, relwidth=0.05, relheight=0.04)
    avg_pre_2_entry.place(relx=0.50, rely=0.81, relwidth=0.05, relheight=0.04)    
    
def Peri_event_analysis():
    
    """This function allows the user to import behavioral
    timestamps and perform perievent analysis. Options for statistical
    analysis of perievent neuronal activity will also be displayed upon the execution
    of this function. The function is executed when the use timestamps? checkbox is filled in."""
     
    ### This is all the variables that will be exported from this function
    global AUC_analysis_entry
    global Zex_analysis_entry
    global Average_analysis_entry
    global Range_pre_entry
    global Range_post_entry
    global base_pre_entry
    global base_post_entry
    global Stimuli_entry
    global SEM_entry
    global std_entry
     
    ### Generating entry boxes for stimuli, range and baseline time range
    Stimuli_entry = tk.Entry(mGui)
    Stimuli_entry.place(relx=0.57, rely=0.12, relwidth=0.28, relheight=0.04)  
    Range_pre_entry = tk.Entry(mGui)
    Range_post_entry = tk.Entry(mGui)
    base_pre_entry = tk.Entry(mGui)
    base_post_entry = tk.Entry(mGui)
    
    ### Creating labels
    label_Stimuli = tk.Label(mGui, text="Enter stimuli here:", font=("Arial", 10), anchor="e")
    Range_label = tk.Label(mGui, text="Enter range to extract here:", font=("Arial", 10), anchor="w")   
    Range_to_label = tk.Label(mGui, text="to", font=("Arial", 10))
    base_to_label = tk.Label(mGui, text="to", font=("Arial", 10))
    std_or_SEM_label = tk.Label(mGui, text="Display error as std or SEM?",font=("Arial", 10), anchor="w" )
    base_label = tk.Label(mGui, text="Enter baseline time:",font=("Arial", 10), anchor="w")
    Pre_label = tk.Label(mGui, text="Pre", font=("Arial", 11))    
    Post_label = tk.Label(mGui, text="Post", font=("Arial", 11))
    Stat_section_title = tk.Label(mGui, text="Parameters for statistical analysis", font=("Arial", 13, "bold"))
    
    ### Creating BooleanVar for what type of error and statistical measure to calculate
    std_entry = tk.BooleanVar()
    SEM_entry = tk.BooleanVar()
    AUC_analysis_entry = tk.BooleanVar()
    Zex_analysis_entry = tk.BooleanVar()
    Average_analysis_entry = tk.BooleanVar()

    ### Creating checkbox for standard deviation
    Checkbox_std = tk.Checkbutton(mGui,
                                   variable = std_entry,
                                   text="std",
                                   onvalue=True,
                                   offvalue=False)
    
    ### Creating checkbox for standard error of the mean
    Checkbox_SEM = tk.Checkbutton(mGui,
                                   variable = SEM_entry,
                                   text="SEM",
                                   onvalue=True,
                                   offvalue=False)
    
    ### Checkboxes for statistical measures
    ### Filling in one of these checkboxes will activate a function
    ### which will tell the code that we are using this statistical measure and 
    ### also allow us the fill in the time ranges for the pre-event and post-event.
    ### The chosen statistical measures for pre-event and post-event will be calculated from 
    ### these two given time ranges, respectively.
    
    
    Checkbox_AUC = tk.Checkbutton(mGui, 
                                   text = "Use Area under curve?",
                                   command=AUC_analysis, 
                                   variable=AUC_analysis_entry,
                                   onvalue=True,
                                   offvalue=False)
 
    Checkbox_zex = tk.Checkbutton(mGui,
                                  text = "Use Z-extreme?           ",
                                  command=Zex_analysis,
                                  variable=Zex_analysis_entry,
                                  onvalue=True,
                                  offvalue=False)
                                
    Checkbox_average_z_score = tk.Checkbutton(mGui,  
                                              text = "Use Z-score average? ",
                                              command=average_z_score,
                                              variable=Average_analysis_entry,
                                              onvalue=True,
                                              offvalue=False)
    
    ### Placing labels, entry boxes and check boxes
    Checkbox_std = Checkbox_std.place(relx=0.35, rely=0.35, relwidth=0.20, relheight=0.06) 
    Checkbox_SEM = Checkbox_SEM.place(relx=0.50, rely=0.35, relwidth=0.20, relheight=0.06)
    label_Stimuli.place(relx=0.35, rely=0.12, relwidth=0.22, relheight=0.04)
    Range_to_label.place(relx=0.76, rely=0.18, relwidth=0.03, relheight=0.04)  
    Range_label.place(relx=0.35, rely=0.18, relwidth=0.34, relheight=0.04)    
    Range_pre_entry.place(relx=0.69, rely=0.18, relwidth=0.05, relheight=0.04)
    Range_post_entry.place(relx=0.81, rely=0.18, relwidth=0.05, relheight=0.04)
    base_pre_entry.place(relx=0.69, rely=0.24, relwidth=0.05, relheight=0.04)
    base_post_entry.place(relx=0.81, rely=0.24, relwidth=0.05, relheight=0.04)
    base_label.place(relx=0.35, rely=0.24, relwidth=0.34, relheight=0.04)
    base_to_label.place(relx=0.76, rely=0.24, relwidth=0.03, relheight=0.04)
    std_or_SEM_label.place(relx=0.35, rely=0.30, relwidth=0.36, relheight=0.04)
    Pre_label.place(relx=0.425, rely=0.49, relwidth=0.10, relheight=0.04)
    Post_label.place(relx=0.675, rely=0.49, relwidth=0.10, relheight=0.04)
    Stat_section_title.place(relx=0.2, rely=0.42, relwidth=0.55, relheight=0.04)    
    Checkbox_AUC.place(relx=0.05, rely=0.53, relwidth=0.30, relheight=0.06)
    Checkbox_zex.place(relx=0.05, rely=0.63, relwidth=0.30, relheight=0.06)
    Checkbox_average_z_score.place(relx=0.05, rely=0.80, relwidth=0.30, relheight=0.06)
    
def assign():
    
    ### This checks whether the experiment path hasn´t been filled in, 
    ### and raises an error if true. 
    if len(path_to_experiment) == 0:
            tk.messagebox.showerror(title = "Error", message = "No experiment path have been chosen, please press the browse experiment path button and choose one")
            raise Exception("No experiment path have been chosen, please press the browse experiment path button and choose one")
    
    ### This extracts the Timestamp_import_bool value, i.e., gets the boolean value
    ### that checks if peri event analysis should be done or not. It imports it into
    ### the Timestamp_import bool variable which is set as global and can thus
    ### be used outside of the function.
    global Timestamp_import_bool
    Timestamp_import_bool = Timestamp_import.get()
       
    if Timestamp_import_bool:
        
        ### These variables will be exported from this function and used in the code after mainloop, i.e., after the gui has been terminated. 
        global Range
        global Stimuli
        global Baseline
        global AUC_analysis_bool
        global Zex_analysis_bool
        global Average_analysis_bool
        global std_bool
        global SEM_bool    
        
        ### These initial if conditions will check that the extraction range, baseline range, error boxes and statistical measure boxes
        ### have been filled in correctly.
        
        ### This checks whether stimuli entry box is empty and raises an error if true. 
        if len(Stimuli_entry.get()) == 0:       
            tk.messagebox.showerror(title = "Error", message = "The stimuli box was left empty, please fill it in")
            raise Exception("The stimuli box was left empty, please fill it in")
        
        ### This checks whether there is atleast one entry box in the range extraction and baseline time range that is empty, 
        ### and raises an error if true.  
        if len(Range_pre_entry.get()) == 0 or len(Range_post_entry.get()) == 0 or len(base_pre_entry.get()) == 0 or len(base_post_entry.get()) == 0:           
            tk.messagebox.showerror(title = "Error", message = "One of the boxes in the range extraction limit or baseline limit were not filled in, fill in all boxes")
            raise Exception("One of the boxes in the range extraction limit or baseline limit were not filled in, fill in all boxes")
        
        
        ### This checks if both error type check boxes are filled in, and raises an error if true. 
        if std_entry.get() and SEM_entry.get():
            tk.messagebox.showerror(title = "Error", message = "both std and SEM chosen, only choose one")
            raise Exception("both std and SEM chosen, only choose one")
        
        ### This checks if both error type checkboxes are left empty, and raises an error if true.
        if std_entry.get() is False and SEM_entry.get() is False:
            tk.messagebox.showerror(title = "Error", message = "Neither std and SEM chosen, choose one")
            raise Exception("Neither std and SEM chosen,choose one")
        
        ### This checks if all checkboxes for the statistical measure types are left empty, and raises an error if true.
        if AUC_analysis_entry.get() is False and Zex_analysis_entry.get() is False and Average_analysis_entry.get() is False:
            tk.messagebox.showerror(title = "Error", message = "No statistical measure option were chosen, chose atleast one.")
            raise Exception("No statistical measure option were chosen, choose atleast one.")
        
        ### This checks if the start time of the total range extraction range is higher than 0 (i.e., extraction time range start after the behavioral event) and raises an error if true.
        if float(Range_pre_entry.get()) > 0:
            tk.messagebox.showerror(title = "Error", message = "The start point time point of the range extraction time range needs to be less than 0.")
            raise Exception("The start point time point of the range extraction time range needs to be less than 0.")    
        
        ### This checks if the end time of the total range extraction range is lower than 0 (i.e., extraction time range end before the behavioral event) and raises an error if true.    
        if float(Range_post_entry.get()) < 0:
            tk.messagebox.showerror(title = "Error", message = "The end point time point of the range extraction time range needs to be higher than 0.")
            raise Exception("The end point time point of the range extraction time range needs to be higher than 0.")
            
        ### This checks whether the baseline start time is lower than the total range extraction start time (i.e., baseline to be used to normalize peri event includes data outside the peri event range),
        ### and raises an error if true.
        if float(Range_pre_entry.get()) > float(base_pre_entry.get()):
            tk.messagebox.showerror(title = "Error", message = "The start time point of the baseline is outside of the extraction time range")
            raise Exception("The start time point of the baseline is outside of the extraction time range")
        
        ### This checks whether the baseline end time is higher than the total range extraction end time (i.e., baseline to be used to normalize peri event includes data outside the peri event range),
        ### and raises an error if true. 
        if float(Range_post_entry.get()) < float(base_post_entry.get()):
            tk.messagebox.showerror(title = "Error", message = "The end time point of the baseline is outside of the extraction time range")
            raise Exception("The end time point of the baseline is outside of the extraction time range")
        
        ### This checks whether the start time of the baseline is higher than the end time of the baseline, and raises an error if true. 
        if float(base_pre_entry.get()) > float(base_post_entry.get()):
            tk.messagebox.showerror(title = "Error", message = "The end time point of the baseline is lower than the baseline start time point")
            raise Exception("The end time point of the baseline is lower than the baseline start timepoint")
                  
        ### If all the conditions for the range extraction time limit, baseline time limit, error type and statistical measure type inputs are
        ### met, the code below will extract the values using .get()
        
        base_pre = float(base_pre_entry.get())
        base_post = float(base_post_entry.get()) 
        Baseline = (base_pre, base_post)       
        Stimuli = Stimuli_entry.get()
        Range_pre = float(Range_pre_entry.get())
        Range_post = float(Range_post_entry.get())
        Range = (Range_pre, Range_post)      
        AUC_analysis_bool = AUC_analysis_entry.get()
        Zex_analysis_bool = Zex_analysis_entry.get()
        Average_analysis_bool = Average_analysis_entry.get()
        std_bool = std_entry.get()
        SEM_bool = SEM_entry.get()
        
        ### The following code will deal with processing and extracting the inputs to the statistical measures which includes: Checking if an statistical measure is selected, 
        ### checking if the input for the statistical analysis is acceptable, and 
        ### lastly extracting the values using .get(). Since the code is modular and 
        ### repeated for each statistical measure type,the structure of the code will 
        ### be explained in the below segment. 
        
        ### 1. Checking if the statistical measure type is selected. This is done by checking if the boolean variable connected to the 
        ### specific statistical measure checkbox (e.g., AUC_analysis_bool) is True or False. If true, then the code within the if statement
        ### will be run. 
        
        ### 2. The variables that will be extracted from this section of the function are assigned as global, since they will be used outside
        ###    of the function. 
        
        ### 3. Conditions are applied that checks whether the input into the statistical measure entry boxes are correct. 
        ### For each statistical measure, five conditions are applied. 
            ### 3.1 if any entry box is empty, an error is raised. 
            ### 3.2 If the start time of the pre time range is higher than the end time of the pre time range, an error is raised.
            ### 3.3 If the start time of the post time range is higher than the end time of the post time range an error is raised.
            ### 3.4 If the end time of the post time range is lower than the start time of the pre time range, an error is raised.
            ### 3.5 If the start time of the pre time range is lower than the start time of the start total extraction range, an error is raised.
            ### 3.6 If the end time of the post time range is higher than the end time of the end total extraction range, an error is raised.
        
        ### 4. If the conditions are met, the values are extracted using .get()
        
        if AUC_analysis_bool:
            
            global AUC_pre_1
            global AUC_pre_2
            global AUC_post_1
            global AUC_post_2  
            
            if len(AUC_pre_1_entry.get()) == 0 or len(AUC_pre_2_entry.get()) == 0 or len(AUC_post_1_entry.get()) == 0 or len(AUC_post_2_entry.get()) == 0:
                tk.messagebox.showerror(title = "Error", message = "Atleast one of the boxes in the AUC time range is empty, please fill in all boxes.")
                raise Exception("Atleast one of the boxes in the AUC time range is empty, please fill in all boxes.")
            
            if float(AUC_pre_1_entry.get()) > float(AUC_pre_2_entry.get()):
                tk.messagebox.showerror(title = "Error", message = "The start time point of the AUC pre time range is higher than the pre AUC end time point")
                raise Exception("The start time point of the AUC pre time range is higher than the pre AUC end time point")
            
            if float(AUC_post_1_entry.get()) > float(AUC_post_2_entry.get()):
                tk.messagebox.showerror(title = "Error", message = "The start time point of the AUC post time range is lower than the post AUC end time point")
                raise Exception("The start time point of the AUC post time range is higher than the post AUC end time point")
            
            if float(AUC_post_2_entry.get()) < float(AUC_pre_1_entry.get()):
                tk.messagebox.showerror(title = "Error", message = "The start timepoint of the AUC pre time range is higher than the post AUC end time point")
                raise Exception("The start timepoint of the AUC pre time range is higher than the post AUC end time point")
            
            if float(AUC_pre_1_entry.get()) < Range_pre:
                tk.messagebox.showerror(title = "Error", message = "The start time point of the AUC pre time range is lower than the pre extraction start time point")
                raise Exception("The start time point of the AUC pre time range is lower than the pre extraction start time point")
             
            if float(AUC_post_2_entry.get()) > Range_post:
                tk.messagebox.showerror(title = "Error", message = "The end time point of the AUC post time range is higher than the extraction end time point")
                raise Exception("The end time point of the AUC post time range is higher than the extraction end time point")
            
            AUC_pre_1 = float(AUC_pre_1_entry.get())
            AUC_pre_2 = float(AUC_pre_2_entry.get())
            AUC_post_1 = float(AUC_post_1_entry.get())
            AUC_post_2 = float(AUC_post_2_entry.get())
            
        if Zex_analysis_bool:
            
            global zex_pre_1
            global zex_pre_2
            global zex_post_1
            global zex_post_2
            global Z_max_bool
            global Z_min_bool
            
            if len(zex_pre_1_entry.get()) == 0 or len(zex_pre_2_entry.get()) == 0 or len(zex_post_1_entry.get()) == 0 or len(zex_post_2_entry.get()) == 0:
                tk.messagebox.showerror(title = "Error", message = "Atleast one of the boxes in the Z-extreme time range is empty, please fill in all boxes.")
                raise Exception("Atleast one of the boxes in the AUC time range is empty, please fill in all boxes.")
            
            if float(zex_pre_1_entry.get()) > float(zex_pre_2_entry.get()):
                tk.messagebox.showerror(title = "Error", message = "The start time point of the Z-extreme pre time range is higher than the pre Z-extreme end timepoint")
                raise Exception("The start time point of the Z-extreme pre time range is higher than the pre Z-extreme end timepoint")    
            
            if float(zex_post_1_entry.get()) > float(zex_post_2_entry.get()):
                tk.messagebox.showerror(title = "Error", message = "The start time point of the Z-extreme post time range is higher than the post Z-extreme end timepoint")
                raise Exception("The start time point of the Z-extreme post time range is lower than the post Z-extreme end time point")
            
            if float(zex_post_2_entry.get()) < float(zex_pre_1_entry.get()):
                tk.messagebox.showerror(title = "Error", message = "The start timepoint of the Z-extreme pre time range is higher than the post Z-extreme end timepoint")
                raise Exception("The start timepoint of the Z-extreme pre time range is higher than the post Z-extreme end timepoint")          
            
            if float(zex_pre_1_entry.get()) < Range_pre:
                tk.messagebox.showerror(title = "Error", message = "The start time point of the Z-extreme pre time range is lower than the extraction start timepoint")
                raise Exception("The start time point of the Z-extreme pre time range is lower than the extraction start time point")
            
            if float(zex_post_2_entry.get()) > Range_post:
                tk.messagebox.showerror(title = "Error", message = "The end time point of the Z-extreme post time range is higher than extraction end timepoint")
                raise Exception("The end time point of the Z-extreme post time range is higher than extraction end time point")    
               
            if Z_max.get() and Z_min.get():
                tk.messagebox.showerror(title = "Error", message = "both Z-max and Z-min chosen, only choose one")
                raise Exception("both Z-max and Z-min chosen, only chose one")
            
            if Z_max.get() is False and Z_min.get() is False:
                tk.messagebox.showerror(title = "Error", message = "Neither Z-max and Z-min options chosen, choose one")
                raise Exception("Neither Z-max and Z-min options were chosen, choose one")
            
            zex_pre_1 = float(zex_pre_1_entry.get())
            zex_pre_2 = float(zex_pre_2_entry.get())
            zex_post_1 = float(zex_post_1_entry.get())
            zex_post_2 = float(zex_post_2_entry.get())
            Z_max_bool = Z_max.get()
            Z_min_bool = Z_min.get()
            
        if Average_analysis_bool:
                       
            global avg_pre_1
            global avg_pre_2
            global avg_post_1
            global avg_post_2
            
            if len(avg_pre_1_entry.get()) == 0 or len(avg_pre_2_entry.get()) == 0 or len(avg_post_1_entry.get()) == 0 or len(avg_post_2_entry.get()) == 0:
                tk.messagebox.showerror(title = "Error", message = "Atleast one of the boxes in the Average Z-score time range is empty, please fill in all boxes.")
                raise Exception("Atleast one of the boxes in the AUC time range is empty, please fill in all boxes.")
                
            if float(avg_pre_1_entry.get()) > float(avg_pre_2_entry.get()):
                tk.messagebox.showerror(title = "Error", message = "The start time point of the Average Z-score pre time range is higher than the Average Z-score end timepoint")
                raise Exception("The start time point of the Average Z-score pre time range is higher than the pre Average Z-score end timepoint")
            
            if float(avg_post_1_entry.get()) > float(avg_post_2_entry.get()):
                tk.messagebox.showerror(title = "Error", message = "The start time point of the Average Z-score post time range is lower than the post Z-extreme end timepoint")
                raise Exception("The start time point of the Average Z-score post time range is lower than the post Average Z-score end timepoint")
            
            if float(avg_post_2_entry.get()) < float(avg_pre_1_entry.get()):
                tk.messagebox.showerror(title = "Error", message = "The start timepoint of the Average Z-score pre time range is higher than the post Average Z-score end timepoint")
                raise Exception("The start timepoint of the Average Z-score pre time range is higher than the post Average Z-score end timepoint")
            
            if float(avg_pre_1_entry.get()) < Range_pre:
                tk.messagebox.showerror(title = "Error", message = "The start time point of the Average Z-score pre time range is lower than the extraction start timepoint")
                raise Exception("The start time point of the Average Z-score pre time range is lower than the extraction start timepoint")
            
            if float(avg_post_2_entry.get()) > Range_post:
                tk.messagebox.showerror(title = "Error", message = "The end time point of the Average Z-score post time range is higher than extraction end timepoint")
                raise Exception("The end time point of the Average Z-score post time range is higher than extraction end timepoint")    
            
            avg_pre_1 = float(avg_pre_1_entry.get())
            avg_pre_2 = float(avg_pre_2_entry.get())
            avg_post_1 = float(avg_post_1_entry.get())
            avg_post_2 = float(avg_post_2_entry.get())
    
    ### If this point is reached, i.e. the "Click here to finish" button has been clicked 
    ### and no errors have been raised (all inputted data is correct) the GUI will be
    ### closed (mGui.destroy) and the loop will be broken (mGui.quit()). This
    ### will allow for the code below the mGui.mainloop() to be run.
    mGui.destroy()       
    mGui.quit()
    
### Initializing GUI.
mGui = tk.Tk()
mGui.geometry("500x500+500+300")
mGui.title("Choosing parameters for FIP analysis")

### Creating entry box for path.
Text_path = tk.Entry(mGui)
Text_path.place(relx=0.47, rely=0.01, relwidth=0.4, relheight=0.05)

### Creating browse and exit button
browse_Button = tk.Button(mGui, text="Click here to import experiment PATH:", command=browse_directory)
Exit_Button = tk.Button(mGui, text="Click here to finish", command=assign)

### Creating Boolean variable for whether we should perform peri event analysis or not
Timestamp_import = tk.BooleanVar()

### Creating checkbox for timestamp importation
Checkbox_timestamps = tk.Checkbutton(mGui, 
                                     text = "Use timestamps?",
                                     command=Peri_event_analysis,
                                     variable=Timestamp_import,
                                     onvalue=True,
                                     offvalue=False)

### Placing buttons and checkboxes
browse_Button.place(relx=0.0, rely=0.01, relwidth=0.45, relheight=0.05)
Exit_Button.place(relx=0.35, rely=0.94, relwidth=0.3, relheight=0.05)
Checkbox_timestamps.place(relx=0.05, rely=0.11, relwidth=0.25, relheight=0.06)

### Blocking code after .mainloop until mGui has been destroyed and quitted
mGui.mainloop()

### Parameters for analysis

### Setting error type 
if Timestamp_import_bool:
    if SEM_bool:
        Error_type = "SEM"
    if std_bool:
        Error_type = "Std"

### Setting start time for importing tdt recordings. 
Start = 5

### Setting the step size for plotting matplotlib subplots
Step_size_plot = 4

### Empty lists and dictionaries
Name_of_subjects_lst = []
Calcium_dependent_signal_lst = []
Calcium_independent_signal_lst = []
Calcium_dependent_frame_rate_lst = []
Calcium_independent_frame_rate_lst = []
Timevector_calcium_independent_lst = []
Timevector_calcium_dependent_lst = []
Behavioral_event_lst = []
Settings_for_analysis = {} # Dictionary where results will be appended to
Timestamps_for_camera_frames_lst = []

### Getting paths to each individual subject by using the Path
### function from Pathlib.
Paths_to_experiment_files = Path(path_to_experiment).glob("*") 

### for looping through subject paths
for i, path in enumerate(Paths_to_experiment_files):
  
    path_str = str(path) 
    ### Extracting subject name using regex, where subject name is the subject´s folder name
    Subject_name = re.search("([^\/|^\\\]+$)", path_str).group(0)            
      
    ### First importing data for entire recording, which will be used even if the user didn´t check the "use timestamps?" checkbox. 
    ### This is done inside an try-except block, so if the folder can´t be read by the tdt python package,
    ### we will pass and try with the next folder.       
     
    try:
        
        ### When the tdt.read_block() function encounters an file without tdt files, it will raise an warning.
        ### However, this code contains an custom specific warning for this phenomenon which is more informative
        ### and clear. Thus, the tdt generated warning will be suppressed.
        warnings.filterwarnings('ignore', message= "no tsq file found, attempting to read sev files")
        
        ### Reading in data
        subject_data = tdt.read_block(path, t1 = Start)                    ### Reading data from 5s to end of recording. The reason we´re skipping the first 5 seconds is because
                                                                           ### there is usually a big jump in the beginning of recordings that might mess a bit with our analysis and is therefore omitted.
        
        subject_data_frames = tdt.read_block(path)                         ### Reading data from 0s to end of recording. These data will strictly be used to get the timestamps of the camera frames.
                                                                           ### To do this we need the timestamps camera frames and we can´t therefore use the 
                                                                           ### the tdt object stored in the subject_data variable, since this tdt.object
                                                                           ### doesn´t contain timestamps for the frames before 5s (or whatever the Start variable is set to.)
          
        if subject_data is None:
            
            mGui = tk.Tk()              # Initializing GUI    
            mGui.withdraw()             # Withdrawing main window, to only display the error message
            tk.messagebox.showerror(title = "Error", message = f"The {Subject_name} folder could not be read by the tdt package and will be skipped")      
            pass
        
        else:
    
            ### For the first animals, we will check what sensors have been used. 
            ### The code down here will specifict, either automatically or by user input
            ### which sensor will be used for the rest of subjects during the analysis.
            if i == 0:
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
                    mGui = tk.Tk()              # Initializing GUI    
                    mGui.withdraw()             # Withdrawing main window, to only display the error message
                    tk.messagebox.showerror(title = "Error", message = "No fiber photometry signals seems to be present in this recording")
                    raise Exception("No fiber photometry signals seems to be present in this recording")
            
                ### If there is one sensor, this means that we only recorded using one fiber.
                ### The sensor name will then be set to the only sensor name available in the list
                if len(Sensor_names_no_duplicates) == 1:
                    Sensor = Sensor_names_no_duplicates[0]
                
                ### If there are two sensor names, it means the recording was done with two
                ### fibers. In that case, a GUI created by tkinter will 
                ### pop up, which enables the user to select what sensor to use for  
                ### all the subjects. 
                if len(Sensor_names_no_duplicates) == 2:
                    
                    ### Main window is created
                    mGui = tk.Tk()
                    mGui.geometry("300x350+500+300")
                    mGui.title("Select sensor")
                    
                    
                    ### Text asking (Which sensor do you want to use for analysis?)
                    Sensor_question = tk.Label(mGui, text="Which sensor do you want to use for analysis?", font=("Arial", 9, "bold"))
                    
                    ### Boolean variables for the sensors. 
                    Sensor_1_bool = tk.BooleanVar()
                    Sensor_2_bool = tk.BooleanVar()   
                    
                    ### The checkboxes below are connected to the Sensor_1_bool and Sensor_2_bool variables above.
                    ### Upon clicking the checkboxes, they will switch to True. Thus, when the checkboxes
                    ### are empty, they will be set as False 
                    
                    ### First checkbox which will contain the sensor name of the sensor in 
                    ### the first position in the sensor name list. Upon clicking this checkbox
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
                    
                    ### Checkboxes are placed
                    checkbox_sensor_1.place(relx=0.2, rely=0.45)
                    checkbox_sensor_2.place(relx=0.6, rely=0.45)   
                    Sensor_question.place(relx=0.05, rely=0.35)
                                   
                    def extract_values():
                        
                        """This function will be executed when the user clicks the
                        "click here to finish" button in the Select Sensor GUI".
                        This will import the variables from the Checkboxes and
                        check that one of the checkboxes has been filled in, 
                        and not two or none of the checkboxes has been filled in.
                        Lastly, the function will extract the variables and terminate the GUI"""
                        
                        ### The global variable assignment will imports the Sensor_1_bool and Sensor_2_bool 
                        ### into the function, and export the Sensor1 and Sensor2 variables out of the function

                        global Sensor1
                        global Sensor2                 
                        
                        ### This checks whether both of the Sensor type checkboxes have been filled in,
                        ### and raises an error if true
                        if Sensor_1_bool.get() is True and Sensor_2_bool.get() is True:
                            
                            tk.messagebox.showerror(title = "Error", message = "Both sensors selected, only select one")
                            raise Exception("Both sensors selected, only select one")
                        
                        ### This checks whether none of the Sensor type checkboxes have been filled in,
                        ### and throws an error if true
                        if Sensor_1_bool.get() is False and Sensor_2_bool.get() is False:
                            
                            tk.messagebox.showerror(title = "Error", message = "No sensor selected, please select one")
                            raise Exception("No sensor selected, please select one")
                                             
                        ### If the conditions are met, the Boolean variables are extracted using the .get() function 
                        Sensor1 = Sensor_1_bool.get()
                        Sensor2 = Sensor_2_bool.get()
                        
                        ### If this point is reached, i.e. the "Click here to finish" button has been clicked 
                        ### and no errors have been raised (all inputted data is correct) the GUI will be
                        ### closed (mGui.destroy) and the loop will be broken (mGui.quit()). This
                        ### will allow for the code below the nGui.mainloop() to be run.
                        mGui.destroy()
                        mGui.quit()
                         
                    # This button will trigger the extract_values function when clicked
                    Exit_button_sensor = tk.Button(mGui, text="Click here to finish", command=extract_values)
                    Exit_button_sensor.place(relx=0.30, rely=0.91, relwidth=0.40, relheight=0.08)
                               
                    mGui.mainloop()
                
                    if Sensor1 == True:
                        Sensor = Sensor_names_no_duplicates[0]
                        
                    elif Sensor2 == True:
                        Sensor = Sensor_names_no_duplicates[1]
                    
            ### The code below will extract data from the tdt streams object. Since it is nested, this section will be skipped
            ### if the above try-except (outer) block (in which the tdt file is imported using tdt.read())
            ### throws an error. This try-except block will raise an exception if 
            ### the data can´t be extracted, and will then skip importing anything from this subject. 
            try:

                ### Extracting data
                Calcium_dependent_signal = subject_data.streams[f"_465{Sensor}"].data          # Extracting caldium dependent signal from tdt data file
                Calcium_independent_signal = subject_data.streams[f"_405{Sensor}"].data        # Extracting caldium independent signal from tdt data file
                Calcium_dependent_frame_rate = subject_data.streams[f"_465{Sensor}"].fs        # Extracting frame rate of calcium dependent signal
                Calcium_independent_frame_rate = subject_data.streams[f"_405{Sensor}"].fs      # Extracting frame rate of calcium independent signal
                 
                ### Appending data
                Calcium_dependent_signal_lst.append(Calcium_dependent_signal)              # Appending calcium dependent data
                Calcium_independent_signal_lst.append(Calcium_independent_signal)          # Appending calcium independent data       
                Calcium_dependent_frame_rate_lst.append(Calcium_dependent_frame_rate)      # Appending calcium dependent frame rate     
                Calcium_independent_frame_rate_lst.append(Calcium_independent_frame_rate)  # Appending calcium independent frame rate
                Name_of_subjects_lst.append(Subject_name)                                  # Appending subject names
    
                ### If the "use timestamps?" checkbox was checked, the below code will be executed to import timestamps of behavioral event and also timestamps of camera frames                        
                if Timestamp_import_bool:                            
                    
                    ### In the below code the behavioral event and timestamp for camera frames will be imported inside an 2D nested try-except block.
                    ### Since it is 2D nested, it is dependent on the above (outer) try-blocks to complete without errors.
                    ### If this try-block doesn´t work, it will delete all of the appended data, which was appeneded in the above (outer) try-block.
                    ### Essentially, it will delete all data from the subject from which the timestamp file or timestamp of camera frames could not
                    ### be imported.                         
                    try:
                        ### Reading in data
                        Behavioral_event_animal = pd.read_csv(f"{path_str}\\Timestamps_{Stimuli}.csv").squeeze("columns") # Reading and squeezing behavioral event lst
                        Timestamps_for_camera_frames = pd.DataFrame(subject_data_frames.epocs.Cam1.onset, columns=["Seconds"]).squeeze("columns") # This creates an pandas dataframe which 
                                                                                                                                                  # contain the time onset of each frame captured by the camera.
                                                                                                                                                  # This file will be used if we have behavioral timestamps expressed in frame number
                                                                                                                                                 # we need to convert frame number to seconds.
                        
                        ### Appending data
                        Behavioral_event_lst.append(Behavioral_event_animal)
                        Timestamps_for_camera_frames_lst.append(Timestamps_for_camera_frames)                    # Importing timestamp of frames
                    
                    ### If either the behavioral event timestamps or the timestamps of camera frames were not able to be imported, 
                    ### then the data corresponding to this subject (calcium recordings, subject name etc) will be deleted
                    except:
                        
                        ### Showing an error that tells us the subject was removed from analysis 
                        mGui = tk.Tk()              # Initializing GUI    
                        mGui.withdraw()             # Withdrawing main window, to only display the error message
                        tk.messagebox.showerror(title = "Warning", message = f"The timestamp file for {Subject_name} could not be found and the subject is removed from analysis.")
                        
                        ### Deleting appended subject data
                        del Name_of_subjects_lst[-1]
                        del Calcium_dependent_signal_lst[-1]
                        del Calcium_independent_signal_lst[-1]
                        del Calcium_dependent_frame_rate_lst[-1]
                        del Calcium_independent_frame_rate_lst[-1]                                                    
            
            ### If the tdt data file doesn´t contain recordings from the specified sensor 
            ### it will tell us that the sensor data could not be found and this subject
            ### is removed from the analysis.
            except:
                ### Showing an error that tells us the subject was removed from analysis
                mGui = tk.Tk()         # Initializing GUI    
                mGui.withdraw()        # Withdrawing main window, to only display the error message
                tk.messagebox.showerror(title = "Warning", message = f"The data from the sensor {Sensor}, could not be read for {Subject_name} and the subject is removed from analysis.")
                
                
    ### If a file that is not a directory is encountered, the for loop will skip this iteration.
    except NotADirectoryError:
        pass
        
### Generating path to create the  main results folder in which all data will be put in.
path_to_experiment_windows_path = Path(path_to_experiment)

### If the tdt recordings had two different sensors(i.e., the Sensor_names_no_duplicates == 2), the sensor name will be displayed in the main results folder. 
### otherwise, the sensor type will not be displayed in the main folder name. 

### For both of the different main folder name creations, the code will check if the main folder already exists. 
### If it does, it will enter a while loop and add a number enclosed in paranthesis into the folder name. 
### Thus if you already have a results folder called for example "Results EPM VTA", the code will create 
### a new folder called "Results EPM VTA (2)". 
### However, it will, before doing this, also check if "Results EPM VTA (2)" also exists as a main results folder.
### If it does so it will increase the number enclosed in the paranthesis by 1 and check if this
### main folder name exists. It will do this until it reaches a number where the original name
### plus the number enclosed in paranthesis doesn´t exist as a folder name. It will then output
### the results into that folder name.   

if len(Sensor_names_no_duplicates) == 2:
    Main_folder = Path.joinpath(path_to_experiment_windows_path, f"Results {path_to_experiment_windows_path.parts[-1]}, sensor {Sensor}")
    if Main_folder.is_dir():
        i = 2
        while Path.joinpath(path_to_experiment_windows_path,f"Results {path_to_experiment_windows_path.parts[-1]}, sensor {Sensor} ({i})").is_dir():
            i += 1
        Main_folder = Path.joinpath(path_to_experiment_windows_path, f"Results {path_to_experiment_windows_path.parts[-1]}, sensor {Sensor} ({i})")
else:
    Main_folder = Path.joinpath(path_to_experiment_windows_path, f"Results {path_to_experiment_windows_path.parts[-1]}")
    
    if Main_folder.is_dir():
        i = 2
        while Path.joinpath(path_to_experiment_windows_path,f"Results {path_to_experiment_windows_path.parts[-1]} ({i})").is_dir():
            i += 1
        Main_folder = Path.joinpath(path_to_experiment_windows_path, f"Results {path_to_experiment_windows_path.parts[-1]} ({i})")

### If the default main folder path already exists, i.e., code has been run before, this 
### code will generate a unique folder name consisting of default name + an integer. 
### Thus, there is an unlimited amount of time in which the code can be run.

### Creating folders for exporting figures showing the entire recording
Main_folder.mkdir(parents=True)
Figures_path = Path.joinpath(Main_folder, "Figures of entire recordings")
Figures_path.mkdir(parents=True) 

### Creating directories to export data and figures relevant to perievent analysis, if the
### "use timestamps?" checkbox was checked in.
if Timestamp_import_bool:
    Data_path = Path.joinpath(Main_folder, f"Output perievent {Stimuli} analysis")
    Data_path.mkdir(parents=True)
    Figures_perievent = Path.joinpath(Data_path, "Figures")
    Figures_perievent.mkdir(parents=True)    
    Data_perievent = Path.joinpath(Data_path, "Data")  
    Data_perievent.mkdir(parents=True)

### Converting behavioral timestamp files which contain frame numbers to seconds.
if Timestamp_import_bool:
    for i, (timestamps_of_camera_frames, timestamps_of_animal) in enumerate(zip(Timestamps_for_camera_frames_lst, Behavioral_event_lst)):
        
        if re.search("[fF][rR][aA][mM][eE]", timestamps_of_animal.name): ### Checking if panda series name contains the column frame (case insensitive)
     
            timestamps_of_animal_converted = timestamps_of_camera_frames[timestamps_of_animal.astype(int)].reset_index(drop=True)
            Behavioral_event_lst[i] = timestamps_of_animal_converted
        
### Creating time vectors for calcium independent and calcium dependent signals
for calcium_dependent_signal, calcium_independent_signal, calcium_dependent_frame_rate, calcium_independent_frame_rate  in zip(Calcium_dependent_signal_lst, Calcium_independent_signal_lst, Calcium_dependent_frame_rate_lst, Calcium_independent_frame_rate_lst):
    
    ### The timevector is created by generating, using numpy linspace (https://numpy.org/doc/stable/reference/generated/numpy.linspace.html), an vector with evenly spaced numbers. 
    ### Initially, for each signal (465 or 405) each data point in the signals will have one data point in the timevector, since we´ve set end value the same as the number of time vector datapoints to be generated
    ### For example, for one signal with 6000 data points, the time vector will consist of 6000 datapoints with integers. 
    ### Lastly, the timevector will be divided by the frame rate (i.e. number of signal data points per second for that signal). The frame rate is fixed by a quartz crystal and is therefore reliable. 
    ###Upon doing this, the timevector is converted to seconds, and we will then have a time vector with data points representing the time point of all signal data points.
   
    calcium_dependent_time_vector = Start + np.linspace(1, len(calcium_dependent_signal), len(calcium_dependent_signal))/calcium_dependent_frame_rate          # Creating timevector for calcium dependent signal
    Timevector_calcium_dependent_lst.append(calcium_dependent_time_vector)                                                                                     # Appending calcium dependent time vector 
    calcium_independent_time_vector = Start + np.linspace(1, len(calcium_independent_signal), len(calcium_independent_signal))/calcium_independent_frame_rate  # Creating timevector for calcium_independent signal
    Timevector_calcium_independent_lst.append(calcium_independent_time_vector)                                                                                 # Appending calcium independent time vector

### Correcting calcium dependent with calcium independent signal.
Correct_calcium_dep_lst = []
Calcium_independent_fitted_lst = []

### In the below code, the calcium-dependent signal is corrected for fluctuations not related to changes in intracellular calcium.
### This is done by fitting the calcium-independent signal to the calcium-dependent.
### This is done using the numpy.polyfit function (https://numpy.org/doc/stable/reference/generated/numpy.polyfit.html)
### which performs a least-squared polynomial fit. Since we are using the polyfit with the first degree, we are performing
### a least-squared linear regression to fit the calcium-independent to the calcium-dependent. 
### After fitting, we subtract the fitted calcium-independent from the calcium-dependent and
### then get the corrected calcium-dependent signal which we append into the 
### Correct_calcium_dep lst. 
    

### This error is raised due to the fitted calcium independent trace being sensitive to small changes in the data.
### It seems to be raised for all samples, even if the fit is completely acceptable by manual observation.
### Thus, the code below silences this warning since it in our case doesn´t seem to provide any valuable information.
warnings.simplefilter('ignore', np.RankWarning)

for calcium_independent_signal, calcium_dependent_signal in zip(Calcium_independent_signal_lst, Calcium_dependent_signal_lst): 
    
    fitting_independent_to_dependent = np.polyfit(calcium_independent_signal, calcium_dependent_signal, 1) ### Using polyfit to the first degree.
    fit_line_independent_to_dependent = np.multiply(fitting_independent_to_dependent[0], calcium_independent_signal) + fitting_independent_to_dependent[1]
    Corrected_calcium_dependent = calcium_dependent_signal - fit_line_independent_to_dependent
    Calcium_independent_fitted_lst.append(fit_line_independent_to_dependent)
    Correct_calcium_dep_lst.append(Corrected_calcium_dependent)

### Plotting raw signals

### The general approach for plotting these signal is that when there are
### multiple plots to generate, each figure will contain 4 plots.
### This is to make sure that the sizes of the plots remain consistent. 

### This will only be explained here, but the approach is same
### in all for loops including the "jump_ind" variable

Jump_ind = 0

for i in range(math.ceil(len(Name_of_subjects_lst)/4)):  ### This will jump 4 steps, i.e., each loop in this for loop will generate one figure with 4 plots. 

    fig_raw_signal, axs_raw_signal = plt.subplots(4,1, figsize=(16,16)) ### Generating figure object with 4 subplots
    
    for j, ax in enumerate(axs_raw_signal): ### This will iterate through the axes in the figure object with 4 subplots.
        
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
    
    Jump_ind += 4 ### After exporting the figure, jump_ind will increase with 4, to sample the next 4 iteration subject data  

### Plotting fitted calcium independent signal
Jump_ind = 0

for i in range(math.ceil(len(Name_of_subjects_lst)/4)):  

    fig_raw_fitted_signal, axs_raw_fitted_signal = plt.subplots(4,1, figsize=(16,16)) ### Generating figure object with subplots
    
    for j, ax in enumerate(axs_raw_fitted_signal):
        
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
        
    fig_raw_fitted_signal.tight_layout()
    Path_to_export_figures = Path.joinpath(Figures_path, f"Fitted calcium independent signal, subjects {Jump_ind} - {Jump_ind+4} .tiff")
    fig_raw_fitted_signal.savefig(Path_to_export_figures)
    Jump_ind += 4   
    
### Plotting corrected calcium independent signal
Jump_ind = 0

for i in range(math.ceil(len(Name_of_subjects_lst)/4)):  

    fig_corrected_signal, axs_corrected_signal = plt.subplots(4,1, figsize=(16,16)) ### Generating figure object with subplots
    
    for j, ax in enumerate(axs_corrected_signal):
        
        if j + Jump_ind + 1 > len(Name_of_subjects_lst):
            break
        else:
            ax.plot(Timevector_calcium_dependent_lst[j+Jump_ind], Correct_calcium_dep_lst[j+Jump_ind], color="green", label="Calcium dependent")        # Plotting corrected calcium dependent signal
            ax.set_title(f"{Name_of_subjects_lst[j+Jump_ind]} raw signals", fontsize=30)
            ax.set_ylabel("dF", fontsize=25)
            ax.set_xlabel("Time (s)", fontsize=25)
            ax.tick_params(axis="both", which="major", labelsize=17)
            ax.legend(fontsize=20, loc="upper right")
        
    fig_corrected_signal.tight_layout()
    Path_to_export_figures = Path.joinpath(Figures_path, f"Correctec calcium dependent signal, subjects {Jump_ind} - {Jump_ind+4} .tiff")
    fig_corrected_signal.savefig(Path_to_export_figures)
    Jump_ind += 4  

if Timestamp_import_bool: ### This will perform the perievent analysis, but only if you clicked the "Use timestamps?" checkbox.
    
    ### This code section will remove timestamps that are too close to the start of recordings or too close too end.
    ### If they are so close so that we can´t extract the time range of neural activity 
    
    ### This lst will contain the indexes of the behavioral event files in the Behavioral_event_lst 
    ### that are either initially or after filtering, empty. These indexes will thereafter be used to 
    ### delete the files.
    Indexes_for_empty_behavioral_event_lst_to_be_removed = []
    
    for i, animal_timestamps in enumerate(Behavioral_event_lst):
        
        animal_timestamps_filtered = animal_timestamps[((animal_timestamps+Range[0]) > Start) &  ((animal_timestamps + Range[1]) < Timevector_calcium_dependent_lst[i][-1])].reset_index(drop=True)
        Behavioral_event_lst[i] = animal_timestamps_filtered  
        
        if animal_timestamps_filtered.size == 0:
            Indexes_for_empty_behavioral_event_lst_to_be_removed.append(i)
    
    ### Using list comprehension to remove the files of the subjects which behavioral event files had a size of zero. 
    ### If the index of that subject is in the Indexes_for_empty_behavioral_event_lst_to_be_removed, it will be removed using the below code. 
    Behavioral_event_lst = [Behavioral_file_animal for i, Behavioral_file_animal in enumerate(Behavioral_event_lst) if i not in Indexes_for_empty_behavioral_event_lst_to_be_removed]
    Correct_calcium_dep_lst = [Correct_calcium_dep_animal for i, Correct_calcium_dep_animal in enumerate(Correct_calcium_dep_lst) if i not in Indexes_for_empty_behavioral_event_lst_to_be_removed]
    Name_of_subjects_lst = [subject for i, subject in enumerate(Name_of_subjects_lst) if i not in Indexes_for_empty_behavioral_event_lst_to_be_removed]
    Timevector_calcium_dependent_lst = [Timevector_calcium_dependent_animal for i, Timevector_calcium_dependent_animal in enumerate(Timevector_calcium_dependent_lst) if i not in Indexes_for_empty_behavioral_event_lst_to_be_removed]
    

    if len(Behavioral_event_lst) == 0:
        tk.messagebox.showerror(title = "Error", message = "After filtering, all timestamps were removed and no subject recordings thus remains")
        raise Exception("After filtering, all timestamps were removed and no subject recordings thus remains")
      
    ### Extracting the neural activity surrounding each behavioral event
    Z_score_of_neural_activity_surrounding_events = [[] for animal in Correct_calcium_dep_lst] # Creating 2D list with sublist for each animal in Correct_calcium_dep_lst
    
    for i, (signal_animal, timestamps_animal, timevector_animal) in enumerate(zip(Correct_calcium_dep_lst, Behavioral_event_lst, Timevector_calcium_dependent_lst)):
      
      for behavioral_event in timestamps_animal:

          ### The activity surrounding each behavioral event will be gathered using numpy.where(https://numpy.org/doc/stable/reference/generated/numpy.where.html). 
          ### where indices fullfilling certain critiries will be extracted. In our case, we select the indices of the timevector where the data points are 
          ### firstly higher than the time point of the behavioral event - the start time of the total extraction range AND lower than the time point of the behavioral event + the end time of the total extraction range.
          index_for_event = np.where((timevector_animal > (behavioral_event+Range[0])) & (timevector_animal < (behavioral_event+Range[1])))[0]
          
          ### These indeces are thereafter used to select the signal data points in the corrected calcium dependent signal.
          ### This works since the timevector and the corrected calcium signal share the same indices.
          ### To explain it a bit further, to find the signal corresponding to a specific time point in the timevector, 
          ### you only need to use the index of that time data point in the signalvector. 
          Neural_activity_for_behavioral_event = signal_animal[index_for_event]
     
          # Z-scoring the neural activity using the same np.where function but with the baseline time ranges instead.      
          index_for_baseline = np.where((timevector_animal > (behavioral_event+Baseline[0])) & (timevector_animal < (behavioral_event+Baseline[1])))
          Neural_activity_of_baseline = signal_animal[index_for_baseline]
          Z_score = (Neural_activity_for_behavioral_event - Neural_activity_of_baseline.mean()) / Neural_activity_of_baseline.std()   ## Z-scoring by subtracting the mean of the baseline and dividing by the standard deviation.                             
          Z_score_of_neural_activity_surrounding_events[i].append(Z_score)


    ### Making sure all the perievents have same length and making a final timevector to use
    ### for all perievents. 

    ### This collects the minimum trial length for each animal
    min_perievent_length_animal = []

    for animal_peri_event_signals in Z_score_of_neural_activity_surrounding_events:
        min_peri_event_length = np.min([np.size(peri_event) for peri_event in animal_peri_event_signals])
        min_perievent_length_animal.append(min_peri_event_length)

    ### This collects the minimum trial length of all animals
    total_min_peri_event = np.min(min_perievent_length_animal)

    ### This trims down the lengths of all trials to the shortest trial length
    ### of all animals
    for i, animal_peri_event_signals in enumerate(Z_score_of_neural_activity_surrounding_events):
        animal_peri_event_signals = [peri_event[:total_min_peri_event] for peri_event in animal_peri_event_signals]
        Z_score_of_neural_activity_surrounding_events[i] = animal_peri_event_signals

    ### This creates a timevector based on the trimmed trials
    ### This has the same length as all trials  
    Timevec_peri_event_final = Range[0] + np.linspace(1, len(Z_score_of_neural_activity_surrounding_events[0][0]), len(Z_score_of_neural_activity_surrounding_events[0][0]))/Calcium_dependent_frame_rate_lst[0]
    Z_score_averaged_neural_activity = []
    Z_score_error_per_animal = []
    
    ### All the values extracted for statistical analysis will be appended
    ### to this dictionary
    Statistical_analysis = {"Subjects":Name_of_subjects_lst, 
                            "AUC pre": [], 
                            "AUC post":[], 
                            "Z-min pre":[],
                            "Z-min post": [],
                            "Z-max pre":[],
                            "Z-max post":[],
                            "Average Z-score pre":[],
                            "Average Z-score post":[],
                            }
    
    ### Extracting the measures for the statistical analysis. This will be done
    ### for each subject.
    for i, z_score_animal_all_trials in enumerate(Z_score_of_neural_activity_surrounding_events):
        
        z_score_animal_avg = np.mean(z_score_animal_all_trials, axis=0) ### Averaging all trials within each animal
        Z_score_averaged_neural_activity.append(z_score_animal_avg)
        
        ### This will calculated the standard deviation for each subject if it was chosen as the error type in the user interface. 
        if std_bool:
            
            Z_score_std_per_animal = np.std(z_score_animal_all_trials, axis=0)
            Z_score_error_per_animal.append(Z_score_std_per_animal)
        
        ### This will calculated the standard error of the mean for each subject if it was chosen as the error type in the user interface.
        if SEM_bool:
            
            Z_score_SEM_per_animal = np.std(z_score_animal_all_trials, axis=0) / np.sqrt(len(z_score_animal_all_trials))
            Z_score_error_per_animal.append(Z_score_SEM_per_animal)
        
        ### If the "Use Area under curve?" checkbox is filled, this will calculate the AUC. 
        if AUC_analysis_bool:
            
            index_pre_AUC = np.where((Timevec_peri_event_final > AUC_pre_1) & (Timevec_peri_event_final < AUC_pre_2))
            index_post_AUC = np.where((Timevec_peri_event_final > AUC_post_1) & (Timevec_peri_event_final < AUC_post_2)) 
            
            ### Area under curve is calculated by using sk.learn metrics AUC function, which 
            ### calcualtes the AUC using the trapezoidal rule.
            AUC_pre  = auc(Timevec_peri_event_final[index_pre_AUC], z_score_animal_avg[index_pre_AUC])
            AUC_post = auc(Timevec_peri_event_final[index_post_AUC], z_score_animal_avg[index_post_AUC])
            Statistical_analysis["AUC pre"].append(AUC_pre)
            Statistical_analysis["AUC post"].append(AUC_post)
            Settings_for_analysis["AUC time range (s)"] = [f"Pre: {AUC_pre_1} to {AUC_pre_2}", f"Post: {AUC_post_1} to {AUC_post_2}"]
        
        ### If the "Use Z-extreme?" checkbox is filled, this will calculate the Z-extreme (Z-max or Z-min) will be calculated.
        if Zex_analysis_bool:
            
            index_pre_zex = np.where((Timevec_peri_event_final > zex_pre_1) & (Timevec_peri_event_final < zex_pre_2))
            index_post_zex = np.where((Timevec_peri_event_final > zex_post_1) & (Timevec_peri_event_final < zex_post_2))
            
            ### The below code will extract either the Z-score minimum or maximum within the specified time ranged,
            ### dependent on whether the z-min or z-max checkbox was checked.    
            
            ### If Z-min_bool is True, the Z-min will be calculated
            if Z_min_bool:
                
                Z_min_pre = z_score_animal_avg[index_pre_zex].min()
                Z_min_post = z_score_animal_avg[index_post_zex].min()     
                Statistical_analysis["Z-min pre"].append(Z_min_pre)
                Statistical_analysis["Z-min post"].append(Z_min_post)
                Settings_for_analysis["Z-min time range(s)"] = [f"Pre: {zex_pre_1} to {zex_pre_2}", f"Post: {zex_post_1} to {zex_post_2}"]
            
            ### If Z-max_bool is True, the Z-max will be calculated
            if Z_max_bool:
                
                Z_max_pre = z_score_animal_avg[index_pre_zex].max()
                Z_max_post = z_score_animal_avg[index_post_zex].max()  
                Statistical_analysis["Z-max pre"].append(Z_max_pre)
                Statistical_analysis["Z-max post"].append(Z_max_post)
                Settings_for_analysis["Z-max time range(s)"] = [f"Pre: {zex_pre_1} to {zex_pre_2}", f"Post: {zex_post_1} to {zex_post_2}"]
        
        ### If the "Use Z-score average?" checkbox is filled, this will calculate the average z-score will be calculated.
        if Average_analysis_bool:
            
            index_pre_avg = np.where((Timevec_peri_event_final > avg_pre_1) & (Timevec_peri_event_final < avg_pre_2))
            index_post_avg = np.where((Timevec_peri_event_final > avg_post_1) & (Timevec_peri_event_final < avg_post_2))
            Z_score_avg_pre = z_score_animal_avg[index_pre_avg].mean()
            Z_score_avg_post = z_score_animal_avg[index_post_avg].mean()
            Statistical_analysis["Average Z-score pre"].append(Z_score_avg_pre)
            Statistical_analysis["Average Z-score post"].append(Z_score_avg_post)
            Settings_for_analysis["Average Z-score time range (s)"] = [f"Pre: {avg_pre_1} to {avg_pre_2}", f"Post: {avg_post_1} to {avg_post_2}"]
    
    ### Plotting peri event traces for the individual subjects
    Jump_ind = 0
    
    for i in range(math.ceil(len(Name_of_subjects_lst)/4)):  

        fig_peri_event_signal, axs_peri_event_signal = plt.subplots(4,1, figsize=(16,16)) ### Generating figure object with subplots
        for j, ax in enumerate(axs_peri_event_signal):
            
            if j + Jump_ind + 1 > len(Name_of_subjects_lst):
                break
            else:            
                ax.plot(Timevec_peri_event_final, Z_score_averaged_neural_activity[j+Jump_ind], color="green")        # Plotting calcium dependent signal
                ax.fill_between(Timevec_peri_event_final, Z_score_averaged_neural_activity[j+Jump_ind]+Z_score_error_per_animal[j+Jump_ind], Z_score_averaged_neural_activity[j+Jump_ind]-Z_score_error_per_animal[j+Jump_ind], color="green", alpha=0.3)
                ax.set_title(f"{Name_of_subjects_lst[j+Jump_ind]}", fontsize=30)
                ax.set_ylabel("Z-score", fontsize=25)
                ax.set_xlabel("Time (s)", fontsize=25)
                ax.tick_params(axis="both", which="major", labelsize=17)
            
        fig_peri_event_signal.tight_layout()
        Path_for_exporting_peri_event_signals_all_subjects = Path.joinpath(Figures_perievent, f"Perievent signal subjects {Jump_ind} - {Jump_ind+4} .tiff")  
        fig_peri_event_signal.savefig(Path_for_exporting_peri_event_signals_all_subjects)
        Jump_ind += 4   

    ### Averaging all animals together and plotting the averaged activity.
    Z_score_averaged_completely = np.mean(Z_score_averaged_neural_activity, axis=0)

    if std_bool:
        Z_score_error_total = np.std(Z_score_averaged_neural_activity, axis=0)
    
    if SEM_bool:    
        Z_score_error_total = np.std(Z_score_averaged_neural_activity, axis=0) / np.sqrt(len(Name_of_subjects_lst))
        
    ### Plotting the averaged across all subjects peri event trace  
    fig_all_averaged = plt.figure(figsize=(15,8))     
    ax_fig_all_averaged = plt.subplot(111)
    ax_fig_all_averaged.plot(Timevec_peri_event_final, Z_score_averaged_completely, color="green")
    ax_fig_all_averaged.fill_between(Timevec_peri_event_final, Z_score_averaged_completely-Z_score_error_total, Z_score_averaged_completely+Z_score_error_total,color="green", alpha = 0.3)
    ax_fig_all_averaged.set_title("Single trace", fontsize=30)
    ax_fig_all_averaged.set_ylabel("Z-score", fontsize=25)
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
    Settings_for_analysis["Error type"] = [Error_type]
    Settings_for_analysis["Stimuli"] = [Stimuli]
    
    ### The code below will make the values in settings dictionary same length so the dict can be exported to csvs using Pandas to_csv function
    Settings_for_analysis_max_length = max([len(v) for v in Settings_for_analysis.values()]) # Finding column with the highest length

    for key, values in Settings_for_analysis.items():
        if len(values) < Settings_for_analysis_max_length: # If a column has lower number of values then max length, then this code will fill with NaNs until it has the same length.
            while len(values) < Settings_for_analysis_max_length: # While len(values) is lower then max, np.nan will be appended.
                Settings_for_analysis[key].append(np.nan)
    
    ### Exporting settings for the peri event analysis
    Settings_for_analysis_pd = pd.DataFrame(Settings_for_analysis)
    Path_to_export_settings_for_analysis = Path.joinpath(Data_perievent, "Settings for peri event analysis.csv") ### This creates the path for exporting the csv
    Settings_for_analysis_pd.to_csv(Path_to_export_settings_for_analysis, index=False)
    
    ### Exporting statistical analysis
    Statistical_analysis_filtered = {k:v for k, v in Statistical_analysis.items() if len(v) > 0} ### Some of the values for the items in statistical analysys                                                                                               ### dictionary will be empty (e.g., Z-min values will be empty if we chose Z-max in the Gui.)                                                                                               ### This dictiory comprehension will remove empty key-value pairs.
    Statistical_analysis_pd = pd.DataFrame(Statistical_analysis_filtered)
    Path_to_export_statistical_analysis = Path.joinpath(Data_perievent, "Statistical_analysis.csv")  ### This creates the path for exporting the csv 
    Statistical_analysis_pd.to_csv(Path_to_export_statistical_analysis, index=False)
        
    # Exporting perievents for individual animals
    # Using for loop to create dictionary for exporting traces of individual animals
    Perievent_individual_animals_dict = {}
    for i, subject in enumerate(Name_of_subjects_lst):
        
        Perievent_individual_animals_dict[f"{subject} signal"] = Z_score_averaged_neural_activity[i]
        Perievent_individual_animals_dict[f"{subject} {Error_type}"] = Z_score_error_per_animal[i]
    
    ### After the signals and errors have been appended to the dictionary, it is converted to a pandas dataframe
    Perievent_individial_animals_pd = pd.DataFrame(Perievent_individual_animals_dict)
    Perievent_individial_animals_pd.insert(0, "Seconds", Timevec_peri_event_final)                                         ### The time vector for the peri event traces is inserted as the first column
    Path_to_export_perievents_for_individual_animals = Path.joinpath(Data_perievent, "Perievent individual animals.csv")   ### This creates the path for exporting the csv
    Perievent_individial_animals_pd.to_csv(Path_to_export_perievents_for_individual_animals, index=False)
    
    ### Exporting perievents averaged across all subjects (single trace representing total average of all subjects)
    ### The dictionary is created with peri event timevector, peri event signals and the error
    Perievent_averaged_across_animals_dict = {"Seconds" : Timevec_peri_event_final, "Perievent signal" : Z_score_averaged_completely, f"Perievent {Error_type}" : Z_score_error_total}
    Perievent_averaged_across_animals_pd = pd.DataFrame(Perievent_averaged_across_animals_dict)
    Path_to_export_averaged_peri_event_trace = Path.joinpath(Data_perievent, "Perievent averaged trace.csv") ### This creates the path for exporting the csv
    Perievent_averaged_across_animals_pd.to_csv(Path_to_export_averaged_peri_event_trace, index=False)
