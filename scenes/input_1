# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 08:52:54 2025

@author: regne
"""

import tkinter as tk
from tkinter import *

def create_widget(parent, widget_type, **options):
    return widget_type(parent, **options)

root = Tk()
# create the window w/ title at the top
root.title('Calcium Oxalate Kidney Stone Simulation')
root.geometry('1200x400')
# General Entries
calcium_entry = Spinbox(root, from_=0, to=100, width=10, repeatdelay=500, repeatinterval=100,
                     font=("Arial", 12), bg="white")
oxalate_entry = Spinbox(root, from_=0, to=100, width=10, repeatdelay=500, repeatinterval=100,
                     font=("Arial", 12), bg="white")
# citrate_entry = Spinbox(root, from_=0, to=100, width=10, repeatdelay=500, repeatinterval=100,
#                      font=("Arial", 12), bg="white")
water_entry = Spinbox(root, from_=0, to=100, width=10, repeatdelay=500, repeatinterval=100,
                     font=("Arial", 12), bg="white")

calcium_label = Label(root, text='Enter your calcium level')
oxalate_label = Label(root, text='Enter your oxalate level')
# citrate_label = Label(root, text='Enter your citrate level')
water_label = Label(root, text='Enter your urine specific gravity level')

                      
calcium_label.grid(row=0, column=0)
oxalate_label.grid(row=1, column=0)
# citrate_label.grid(row=2, column=0)
water_label.grid(row=2, column=0)

# Placing the Spinbox in the window
calcium_entry.grid(row=0, column=1)
oxalate_entry.grid(row=1, column=1)
# citrate_entry.grid(row=2, column=1)
water_entry.grid(row=2, column=1)

calcium_units = Label(root, text='mg/dL')
oxalate_units = Label(root, text='mg/dL')
# citrate_units = Label(root, text='mg/dL')
water_units = Label(root, text='USG')


calcium_units.grid(row=0, column=2)
oxalate_units.grid(row=1, column=2)
# citrate_units.grid(row=2, column=2)
water_units.grid(row=2, column=2)

## If they haven't gone to the doctor to get urinanlysis results done, some reference metrics:
place_holder= Label(root, text='   ')
place_holder.grid(row=0, column = 5)
place_holder.grid(row=1, column = 5)
place_holder.grid(row=2, column = 5)
place_holder.grid(row=3, column = 5)
calcium_ref_label = Label(root, text='A normal diet of calcium consists of about 100-300 mg, if you have little to no calcium in your diet enter a value below 100 mg. ')
oxalate_ref_label = Label(root, text='A normal diet of oxalate consists of about 25 mg, if your diet consists of a lot of nuts, beets, spinach, or kale enter a higher number (not to exceed 100 mg). ')
# citrate_ref_label = Label(root, text='A normal diet of citrate consists of about 640 mg, adjust accordingly if your diet contains high or low citrate foods. ')
water_ref_label = Label(root, text='Being relatively hydrated has a value of 1.01, with dehyrdation having a value around 1.02')
calcium_ref_label.grid(row=0, column=6)
oxalate_ref_label.grid(row=1, column=6)
# citrate_ref_label.grid(row=2, column=6)
water_ref_label.grid(row=2, column=6)
# Check Boxes

# other_conditions = Label(root, text ='Please check what, if any, apply to you', font = "50") 
# other_conditions.grid(row =0, column = 5) 

# Checkbutton1 = IntVar() 
# Checkbutton2 = IntVar() 
# Checkbutton3 = IntVar() 

# Button1 = Checkbutton(root, text = "Family history of kidney stones", 
#                     variable = Checkbutton1, 
#                     onvalue = 1, 
#                     offvalue = 0, 
#                     height = 2, 
#                     width = 10) 

# Button2 = Checkbutton(root, text = "Gastro bypass surgery", 
#                     variable = Checkbutton2, 
#                     onvalue = 1, 
#                     offvalue = 0, 
#                     height = 2, 
#                     width = 10) 

# Button3 = Checkbutton(root, text = "Have had a kidney stone before", 
#                     variable = Checkbutton3, 
#                     onvalue = 1, 
#                     offvalue = 0, 
#                     height = 2, 
#                     width = 10) 
    
# Button1.grid(row = 1, column = 5) 
# Button2.grid(row = 2, column = 5) 
# Button3.grid(row = 3, column = 5)  





# Checklist Phase

#Radiobutton(root, text='Prefer not to disclose', variable=v, value=2).pack(anchor=W)
mainloop()
root.mainloop()
