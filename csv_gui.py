import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
import tkinter.filedialog

WIDTH = 500
HEIGHT = 600

class Frames(tk.Frame):
    def __init__(self, *args, **kwargs):
        self.parent = parent
        self.parent.iconbitmap("favicon.ico")

        self.get_main_parent(self.parent)
        self.get_main_canvas(self.parent)
        self.get_bg_img(self.parent)
        self.get_file_options(self.parent)
        self.get_x_user_options(self.parent)
        self.get_y_user_options(self.parent)
        self.get_display_options(self.parent)

        self.parent.mainloop()

    def get_main_parent(self, parent):
        #self.parent = tk.Tk()
        self.parent.resizable(False, False)
        self.parent.title("CSV Visualiser")

    def get_main_canvas(self, parent):
        canvas = tk.Canvas(parent, height = HEIGHT, width = WIDTH)
        canvas.pack()

    def get_bg_img(self, parent):
        self.background_image = tk.PhotoImage(file = "background.png")
        self.background_label = tk.Label(parent, image = self.background_image)
        self.background_label.place(relwidth = 1, relheight = 1)

    def get_file_options(self, parent):
        options_frame = tk.Frame(parent, bg = "#80c1ff", bd = 5)
        options_frame.place(relx = 0.5, rely = 0.1, relwidth = 0.75, relheight = 0.1, anchor = 'n')

        self.file_label = tk.Label(options_frame, font = 40, text = "File Name")
        self.file_label.place(relwidth = 0.65, relheight = 1)

        get_button = tk.Button(options_frame, text = "Get File", font = 40, command = self.get_csv)
        get_button.place(relx = 0.7, relheight = 1, relwidth = 0.3)

    def get_x_user_options(self, parent):
        self.loaded_frame = tk.Frame(parent, bg = "#80c1ff", bd = 5)
        self.loaded_frame.place(relx = 0.5, rely = 0.225, relwidth = 0.75, relheight = 0.225, anchor = 'n')

        self.columns_desc = tk.Label(self.loaded_frame, font = 40, text = "Choose a column for the x-axis:")
        self.columns_desc.place(relheight = 0.225, relwidth = 1)

        self.columns_select_button = tk.Button(self.loaded_frame, text = "Select", font = 40, command = lambda: self.get_dataframe(self.columns_listbox))
        self.columns_select_button.place(rely = 0.3, relheight = 0.20, relwidth = 1)

        self.columns_listbox = tk.Listbox(self.loaded_frame)
        self.columns_listbox.place(rely = 0.575, relheight = 0.4, relwidth = 1)

    def get_y_user_options(self, frame):
        self.second_loaded_frame = tk.Frame(parent, bg = "#80c1ff", bd = 5)
        self.second_loaded_frame.place(relx = 0.5, rely = 0.475, relwidth = 0.75, relheight = 0.225, anchor = 'n')

        self.second_columns_desc = tk.Label(self.second_loaded_frame, font = 40, text = "Choose a column for the y-axis:")
        self.second_columns_desc.place(relheight = 0.225, relwidth = 1)

        self.second_columns_select_button = tk.Button(self.second_loaded_frame, text = "Select", font = 40, command = lambda: self.get_dataframe(self.second_columns_listbox))
        self.second_columns_select_button.place(rely = 0.3, relheight = 0.20, relwidth = 1)

        self.second_columns_listbox = tk.Listbox(self.second_loaded_frame)
        self.second_columns_listbox.place(rely = 0.575, relheight = 0.4, relwidth = 1)

    def get_display_options(self, parent):
        self.display_frame = tk.Frame(parent, bg = "#80c1ff", bd = 5)
        self.display_frame.place(relx = 0.5, rely = 0.725, relwidth = 0.75, relheight = 0.225, anchor = 'n')

        self.display_selected_x_header = tk.Label(self.display_frame, font = 40, text = "Selected x-axis:", bg = "#80c1ff", anchor = 'w')
        self.display_selected_x_header.place(relheight = 0.225, relwidth = 0.31)

        self.display_selected_x = tk.Label(self.display_frame, font = 40, text = "None")
        self.display_selected_x.place(relx = 0.375, relheight = 0.225, relwidth = 0.6)

        self.display_selected_y_header = tk.Label(self.display_frame, font = 40, text = "Selected y-axis:", bg = "#80c1ff", anchor = 'w')
        self.display_selected_y_header.place(rely = 0.250, relheight = 0.225, relwidth = 0.31)

        self.display_selected_y = tk.Label(self.display_frame, font = 40, text = "None")
        self.display_selected_y.place(relx = 0.375, rely = 0.250, relheight = 0.225, relwidth = 0.6)

        self.display_frame_graph = tk.Button(self.display_frame, text = "Update", font = 40, command = self.plot_graph)
        self.display_frame_graph.place(rely = 0.60, relheight = 0.20, relwidth = 1)
        
    def get_csv(self):
        self.full_path_to_file = tkinter.filedialog.askopenfilename()

        self.df = pd.read_csv(r"{}".format(self.full_path_to_file))
        print(self.df.head())

        print(self.df.columns.values)

        for i in self.df.columns.values:
            self.columns_listbox.insert(tk.END, i)
            self.second_columns_listbox.insert(tk.END, i)

        self.filename_chosen = self.full_path_to_file.split('/')[-1]

        self.file_label.config(text = f"{self.filename_chosen}")

    def get_dataframe(self, listbox):
        if listbox == self.columns_listbox:
            self.x_selected = listbox.get(tk.ANCHOR)

            self.display_selected_x.config(text = f"{self.x_selected}")

        if listbox == self.second_columns_listbox:
            self.y_selected = listbox.get(tk.ANCHOR)

            self.display_selected_y.config(text = f"{self.y_selected}")

    def plot_graph(self):
        self.plot_window = tk.Tk()
        self.plot_window.resizable(False, False)
        self.plot_window.title("Data Vis.")

        figure = plt.Figure(figsize = (10, 10), dpi = 100)

        ax = figure.add_subplot(111)

        line = FigureCanvasTkAgg(figure, self.plot_window)
        line.get_tk_widget().pack(side = tk.LEFT, fill = tk.BOTH)

        df_agg = self.df[[self.x_selected, self.y_selected]]

        x_list = [df_agg[df_agg.columns[0]][i] for i in range(len(df_agg))]
        y_list = [df_agg[df_agg.columns[1]][i] for i in range(len(df_agg))]

        ax.set_title(f"{self.filename_chosen} - {self.x_selected} vs {self.y_selected}")

        ax.set_xlabel(f"{self.x_selected}")
        ax.set_ylabel(f"{self.y_selected}")

        ax.plot(x_list, y_list)

        self.plot_window.mainloop()
        

    
parent = tk.Tk()

f = Frames(parent)






