import PySimpleGUI as sg
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import matplotlib
from netspeedmonitor.lib import load_db, to_dataframe, record_func
from functools import partial
from threading import Thread

matplotlib.use("TkAgg")


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


db = load_db()
df = to_dataframe(db)


fig = plt.figure()
ax = fig.add_subplot(111)
df.plot(ax=ax, alpha=0.5)

layout = [
    # [sg.Text("Hello from PySimpleGUI")], [sg.Button("OK")]
    [sg.Text("Internet Speed Monitor", font=("Comic Sans", 18))],
    [
        sg.Button("Launch Monitor"),
        sg.Button("Measure Speed"),
        sg.Button("Refresh Plot"),
    ],
    [sg.Canvas(key="-CANVAS-")],
]

# Create the window
window = sg.Window("Demo", layout, finalize=True)
draw_figure(window["-CANVAS-"].TKCanvas, fig)
running_processes = []
# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED:
        break

    if event == "Refresh Plot":
        print("hey!")
        db = load_db()
        df = to_dataframe(db)
        plt.cla()
        df.plot(ax=ax, alpha=0.5)

    if event == "Launch Monitor":
        if len(running_processes) == 0:
            func = partial(record_func, min_interval=1, max_interval=2)
            process = Thread(target=func, daemon=True)
            process.start()
            running_processes.append(process)
        else:
            print("hey!")

window.close()
