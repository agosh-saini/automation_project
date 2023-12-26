# ------- IMPORTS --------- #
from ideation_ec_automation import ideation_ec_automation
from os import listdir
from os.path import isfile, join
import PySimpleGUI as sg
from ast import literal_eval
# ------- IMPORTS END --------- #

# ------- SCRIPT --------- #
# Selecting the theme of the UI
sg.theme('Black')

    # the layout of the UI (with inputs)
layout_mark_peaks = [[sg.Text('Extracting Information from EC Data')],
          [sg.Text('User Folder'), sg.Input(key='path'),
           sg.FolderBrowse(target='path')],
          [sg.Checkbox('Get Graphs', default=True, key='graph')],
          [sg.Text('Threshold'), sg.InputText(key='thres')],
          [sg.Text('Min Height'), sg.InputText(key='height')],
          [sg.Checkbox('Check for Peak, Uncheck for Valley', default=False, key='peak')],
          [sg.Button('Ok'), sg.Button('Cancel')]]

# Create the Window
window = sg.Window('IDEATION LAB', layout_mark_peaks)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    # if user closes window or clicks cancel or clicks ok -> exit
    if event == sg.WIN_CLOSED or event == 'Cancel' or event == "Ok":
        break
# close the window
window.close()

# get the path of the folder
path = values['path']

# get all the files in the directory
files = [f for f in listdir(path) if isfile(join(path, f))]

# determines if peaks or valleys are desired
if values['peak'] is False:
    direction = -1
else:
    direction = 1

# repeat for all the files we have
for file in files:
    for column_i in literal_eval(values['column']):
        test = ideation_ec_automation(path, file)

        # create the pandas dataframe
        df = test.create_df()

        # look for peaks and get the graphs
        test.plot_res(column=[column_i],
                      smooth=float(values['smooth']), graph=values['graph'],
                      threshold=float(values['thres']),
                      min_height=float(values['height']),
                      direction=direction)

# -------- SCRIPT END ------------- #
