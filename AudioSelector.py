from email.mime import audio
import tkinter as tk
from tkinter import END, W, filedialog, ttk
import os
from pyparsing import col
import audio_to_text

class AudioSelector:
    def __init__(self, root):
        
        self.AudioToText = audio_to_text.AudioToText()

        #Set config window base.
        self.root = root
        self.root.title("Selector de Audio")
        #self.root.geometry("800x600")

        #Set config label base.
        frame_master = tk.LabelFrame(root,text="Convertirdor de archivos")
        frame_master.grid(row = 0, column= 0,columnspan=3,padx=15,pady=15)

        #Set label input foldel
        #self.label = tk.Label(frame, text="Seleccionar carpeta").grid(row=1,column=0,padx=5,pady=5)

        #Set entry folder selected
        self.folder_path = tk.StringVar()
        self.folder_entry = tk.Entry(frame_master, textvariable=self.folder_path, width=50).grid(row=1,column=0,padx=5,pady=5,columnspan=2,sticky='ew')
        
        #Set button open folder selected
        self.browse_button = tk.Button(frame_master, text="Seleccionar carpeta audios", command=self.browse_folder).grid(row=1,column=3,padx=5,pady=5,sticky='ew')

        #Set list frame
        #self.audio_list_frame = tk.Frame(frame)

        #Set audio listbox 
        self.audio_listbox = tk.Listbox(frame_master,selectmode=tk.SINGLE,width=30)
        self.audio_listbox.grid(row=2,column=0,padx=5,pady=5)
        self.audio_listbox.bind('<<ListboxSelect>>', self.event_listbox)


        #Set frame
        self.frame_buttons_add_and_remove = tk.Label(frame_master)
        self.frame_buttons_add_and_remove.grid(row = 2, column = 1,sticky='nsew')
        self.frame_buttons_add_and_remove.grid_columnconfigure(0, weight=1)
        self.frame_buttons_add_and_remove.grid_rowconfigure(0, weight=1)

        #Set button add audio.
        self.add_audio_button = tk.Button(self.frame_buttons_add_and_remove,text="=>",command=self.event_add_audio)
        self.add_audio_button.grid(row=0,column=0,padx=5,pady=5,sticky='n')

        #Set button remove audio.
        self.remove_audio_button = tk.Button(self.frame_buttons_add_and_remove,text="<=",command=self.event_remove_audio)
        self.remove_audio_button.grid(row=1,column=0,padx=5,pady=5,sticky='s')


        #Set listbox selected
        self.audio_listbox_selected = tk.Listbox(frame_master,selectmode=tk.SINGLE,width=30)
        self.audio_listbox_selected.grid(row=2,column=3 ,padx=5,pady=5)
        self.audio_listbox_selected.bind('<<ListboxSelect>>', self.event_listbox_selected)

        #Set config button run program
        self.converter_button = tk.Button(frame_master,text="Generar Texto",command=self.run_converter)
        self.converter_button.grid(row=3,column=0,padx=5,pady=5,sticky='we')

        #Set progress bar
        self.progress = ttk.Progressbar(frame_master, orient='horizontal', length=200, mode='determinate')
        self.progress.grid(row=3, column=1, padx=5, pady=5,sticky='nsew')

        #Create variables 
        self.path_folder_audios = ""
        self.selected_files = []
        self.index_list_box_input = None
        self.index_list_box_output = None
        self.select_audio_item = None
        self.transcriptions_texts_raw = []


    def browse_folder(self):
        self.path_folder_audios = filedialog.askdirectory()
        if self.path_folder_audios:
            self.folder_path.set(self.path_folder_audios)
            self.load_audio_files(self.path_folder_audios)

    def load_audio_files(self, folder):
        self.audio_listbox.delete(0, tk.END)
        audio_files = [f for f in os.listdir(folder) if f.endswith('.mp3') or f.endswith('.wav') or f.endswith('.m4a')]
        for audio_file in audio_files:
            self.audio_listbox.insert(tk.END, audio_file)

    def event_listbox(self, event):
        widget = event.widget
        self.index_list_box_input  = widget.curselection()
        if(self.index_list_box_input):
            self.select_audio_item = str(widget.get(self.index_list_box_input))  
       
    
    def event_listbox_selected(self,event):
        widget = event.widget
        self.index_list_box_output = widget.curselection()
        if(self.index_list_box_output):
            self.select_audio_item = str(widget.get(self.index_list_box_output))
             
    def event_add_audio(self):
        if self.index_list_box_input  and self.select_audio_item:
            self.audio_listbox.delete(self.index_list_box_input[0])
            self.audio_listbox_selected.insert(tk.END,self.select_audio_item)
            self.index_list_box_input = None
            self.select_audio_item = None
        
    def event_remove_audio(self):
        print("remove audio")
        if self.index_list_box_output  and self.select_audio_item:
            self.audio_listbox_selected.delete(self.index_list_box_output[0])
            self.audio_listbox.insert(tk.END, self.select_audio_item)
            self.index_list_box_output = None
            self.select_audio_item = None

        print("listbox iz")
        for item in self.audio_listbox.get(0,END):
            print(item)
        print("listbox de")
        for item2 in self.audio_listbox_selected.get(0,END):
            print(item2)

        
    def get_path_complete(self,item):
        return os.path.normpath(os.path.join(self.path_folder_audios,item))

    def update_files_to_process(self):
        self.selected_files = []
        for audio in self.audio_listbox_selected.get(0,END):
            self.selected_files.append(self.get_path_complete(audio))
    
    def configurar_progress_bar(self,max_duration):
        self.progress.

    def run_converter(self):
        self.update_files_to_process()
        duration_total =  self.AudioToText.calculate_total_duration_in_seconds(self.selected_files)
        print(duration_total)
        print(self.selected_files)

        """if self.selected_files:
            print("Arrancando transcripcion")
            self.transcriptions_texts_raw = audio_to_text.transcribe_audio_list_by_segments(self.selected_files)
            print("Transcripciones terminadas")
            print(self.transcriptions_texts_raw)
        else:
            print("no run program")
        pass"""


if __name__ == "__main__":
    root = tk.Tk()
    app = AudioSelector(root)
    root.mainloop()