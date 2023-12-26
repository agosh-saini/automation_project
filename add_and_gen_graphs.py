'''
In this document, we will generate graphs and upload the data automatically to SQLite relation_db
'''

import relation_db as db
import graph_gen_and_saving as graph
import PySimpleGUI as sg
import pandas as pd

''' This section deals with creating databases if they do not exist '''

hub = db.relation_db("gas_sensing.db")
db_path, db_name = hub.create_db()
hub.create_index_table()

''' get information about data being added'''

# Define the layout of the window
layout_add_data = [
    [sg.Text('Sensor ID'), sg.InputText(key='Sensor ID')],
    [sg.Text('Metadata'), sg.InputText(key='Metadata')],
    [sg.Text('Analyte'), sg.InputText(key='Analyte')],
    [sg.Text('Material'), sg.InputText(key='Material')],
    [sg.Text('Test ID'), sg.InputText(key='Test ID')],
    [sg.Text('Date'), sg.InputText(key='Date')],
    [sg.Text('Select File'), sg.InputText(key='File'), sg.FileBrowse()],
    [sg.Checkbox('Normalization', default=True, key='norm')],
    [sg.Button('Submit'), sg.Button('Cancel')]
]

# Create the window
window = sg.Window('Sensor Data Input', layout_add_data)

# Event loop
while True:
    event, values = window.read()

    # End program if user closes window or presses the 'Cancel' button
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

    if event == 'Submit':
        print('Data Submitted:', values)
        break

window.close()

''' create graph from data '''

processor = graph.graph_gen_and_saving()
normalized_data = processor.process_all_files(norm=values['norm'])
processor.plot_and_save_graphs(normalized_data)

''' Add data to database '''
path = f"{db_path}\\{db_name}"

hub.add_to_index(values['Sensor ID'], values['Metadata'], values['Analyte'], values['Material'], values['Test ID'], values['Date'])

values['Test ID'] = 'T'+ values['Test ID']

df = pd.read_csv(values['File'])
df.insert(4 , "gas", values['Analyte'])
df.insert(0 , "sensor_id", values['Sensor ID'])
hub.add_to_table(values['Test ID'], df=df)



