from concurrent.futures import thread
from email.mime import audio
import tkinter as tk
from tkinter import END, W, filedialog, ttk
import os
from colorama import init
from pyparsing import col
from sympy import true
from BuilderWordDocx import BuilderWordDocx
import audio_to_text
import threading

class AudioSelector(threading.Thread):
    def __init__(self, root):
        
        self.thread_whisper = False
        threading.Thread.__init__(self,name="thread_whisper",target=self.run_thread_whisper)
        #Run thread Whisper.
        self.start()
        self.AudioToText = audio_to_text.AudioToText()
        self.builderWordDocx = BuilderWordDocx()

        #Set config window base.
        self.root = root
        self.root.title("Selector de Audio")
        #self.root.geometry("800x600")

        #Set config label base.
        frame_master = tk.LabelFrame(root,text="Convertirdor de archivos")
        frame_master.grid(row = 0, column= 0,columnspan=3,padx=15,pady=15)

        #Set label input foldel
        self.label = tk.Label(frame_master, text="Seleccionar carpeta").grid(row=1,column=0,padx=5,pady=5)

        #Set entry folder selected
        self.folder_path = tk.StringVar()
        self.folder_entry = tk.Entry(frame_master, textvariable=self.folder_path, width=50).grid(row=1,column=0,padx=5,pady=5,columnspan=2,sticky='ew')
        
        #Set button open folder selected
        self.browse_button = tk.Button(frame_master, text="Seleccionar carpeta audios", command=self.browse_folder).grid(row=1,column=3,padx=5,pady=5,sticky='ew')

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
        self.progressbar = ttk.Progressbar(frame_master, orient='horizontal', mode='determinate')
        self.progressbar.grid(row=3, column=1, padx=5,columnspan=2, pady=5,sticky='nsew')

        #Set label text progress bar 
        self.label_progressbar = ttk.Label(frame_master,text=self.init_text_progessbar())
        self.label_progressbar.grid(row=4,column=1, sticky='nsew')

        #Set label_name_file
        self.label_name_file = ttk.Label(frame_master,text="Nombre del archivo word")
        self.label_name_file.grid(row=5,column=0, sticky='nsew',pady=5) 

        self.entry_name_file = tk.Entry (frame_master)
        self.entry_name_file.grid(row=5,column=1, sticky='nsew',pady=5)

        #Create variables 
        self.path_folder_audios = ""
        self.selected_files = []
        self.index_list_box_input = None
        self.index_list_box_output = None
        self.select_audio_item = None
        self.transcriptions_texts_raw = []
        self.total_segment = 0
        self.current_step = 0


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
        if self.index_list_box_output  and self.select_audio_item:
            self.audio_listbox_selected.delete(self.index_list_box_output[0])
            self.audio_listbox.insert(tk.END, self.select_audio_item)
            self.index_list_box_output = None
            self.select_audio_item = None
        
    def get_path_complete(self,item):
        return os.path.normpath(os.path.join(self.path_folder_audios,item))

    def update_files_to_process(self):
        self.selected_files = []
        for audio in self.audio_listbox_selected.get(0,END):
            self.selected_files.append(self.get_path_complete(audio))   
    
    def callback_update_progressbar(self):
        self.current_step += 1   
        self.progressbar['value'] = self.current_step
        self.label_progressbar['text'] = self.messageProcess(self.current_step)
    
    def messageProcess(self,current_step) -> str:
        porcentege = int((100*current_step)/self.total_segment)
        if porcentege != 100:
            return  f"Procesado actual: {porcentege}%"
        else:
            return f"Termianado"

    def reset_progressbar(self,total_segment):
        self.label_progressbar['text'] =  f"Procesado actual: {0.00}%"
        self.progressbar.configure(maximum=total_segment)
        self.current_step = 0
        self.progressbar['value'] = self.current_step
        

    def init_text_progessbar(self):
        return f"Procesado actual: {self.progressbar['value']}%"
        
    def run_converter(self):
        self.thread_whisper = True
  
    def run_thread_whisper(self):
        while True:
            if self.thread_whisper:

                self.update_files_to_process()
                self.builderWordDocx.configure_path_save_document(self.path_folder_audios)
                self.total_segment = self.AudioToText.calculate_total_duration_total_segment(self.selected_files)
                self.reset_progressbar(self.total_segment)

                if self.selected_files:
                    self.transcriptions_texts_raw = self.AudioToText.transcribe_audio_list_by_segments(self.selected_files,self.callback_update_progressbar)
                    self.builderWordDocx.create_docx(self.entry_name_file.get(),self.transcriptions_texts_raw)
                else:
                    print("no run program")
                self.thread_whisper = False

            
if __name__ == "__main__":
    root = tk.Tk()
    app = AudioSelector(root)
    root.mainloop()