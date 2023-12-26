# ------- IMPORTS --------- #
from ideation_ec_automation import ideation_ec_automation as auto
from os import listdir
from os.path import isfile, join
import PySimpleGUI as sg
from ast import literal_eval
# ------- IMPORTS END --------- #

# ------- SCRIPT --------- #


# Selecting the theme of the UI
sg.theme('Black')

# the layout of the UI (with inputs)
layout_format_data = [[sg.Text('Extracting Information from EC Data')],
          [sg.Text('User Folder'),sg.Input(key='path'),
           sg.FolderBrowse(target='path')],
          [sg.Text('Headers'), sg.InputText(key='header')],
          [sg.Text('Seperator')],
          [sg.Listbox(values=list(['Comma', 'Tab']), size=(10, 5), key='seperator')],
          [sg.Text('Blank Lines'), sg.InputText(key='blank')],
          [sg.Text('List Columns'), sg.InputText(key='column')],
          [sg.Text('Smooth Value'), sg.InputText(key='smooth')],
          [sg.Checkbox('Entire Bound', default=True, key='entire_bound')],
          [sg.Text('Lower Bound'), sg.InputText(key='lower_bound')],
          [sg.Text('Upper Bound'), sg.InputText(key='upper_bound')],
          [sg.Button('Ok'), sg.Button('Cancel')]]

# Create the Window
window = sg.Window('Format_data', layout_format_data )

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
# check to see if the person wants entire range or not
if values['entire_bound'] is True:
    bound = None
else:
    bound = [float(values["lower_bound"]), float(values("upper_bound"))]


# repeat for all the files we have
for file in files:
    for column_i in literal_eval(values['column']):
        test = auto(path, file)

        # change the seperator
        if values['seperator'] == ['Tab']:
            test.convert_deliminator(sep='\t')

        # remove metadata
        test.format_file_to_csv(blank_line=int(values['blank']),
                                head=values['header'])
        # convert the txt file to csv
        test.convert_csv()

# -------- SCRIPT END ------------- #
