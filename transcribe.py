from tkinter import *
from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
import os
import tempfile
from tkinter import ttk
from tkinter.messagebox import showinfo

class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.max_progress = 1000


        self.start_button  = Button(self,text ="start transcribing",command=self.translate)

        self.mp3_file =None 
        file_name = Label(self,text = "mp3 file path").grid(row = 0, column = 0,pady=20) 

        self.mp3_file_path = Label(self,text = "None")
        self.mp3_file_path.grid(row = 0, column = 1,pady=20)

        self.mp3_size_lb = Label(self,text = "None")
        
        #select_file  = Label(self,text = "click on button",width=20).grid(row = 1, column = 0,pady=20) 
        Button(self, text = "click here to set input file location",command=self.open_file_mp3).grid(row = 1, column = 1,pady=20)  


        self.output_file_path =None 
        Label(self,text = "output file path").grid(row =2, column = 0,pady=20) 
         
        self.output_file_path_lb = Label(self,text = "None")
        self.output_file_path_lb.grid(row = 2, column = 1,pady=20)  
        
        #Label(self,text = "click on button",width=20).grid(row = 3, column = 0,pady=20) 
        Button(self, text = "click here to set output file location",command=self.open_file_text).grid(row = 3, column = 1,pady=20)    

        self.start_button.grid(row = 4, column = 0,pady=20,columnspan= 2)  


        self.value= 0

        self.value_label = ttk.Label(self, text=" do not worry if progress is not increasing,mp3 file is loading\n"+self.update_progress_label())
 
        self.value_label.grid(column=0, row=5, columnspan=2)
        

    def update_progress_label(self):
        x = self.value *100 / self.max_progress
        return f"Current Progress: {x}% , {self.value }/{self.max_progress} done"
    
    def progress(self):
        if self.value < self.max_progress:
            self.value += 1
            self.value_label.config(text = " do not worry if progress is not increasing,mp3 file is loading\n"+ self.update_progress_label())
            self.value_label.update()
        else:
            showinfo(message='The progress completed!')

    def open_file_mp3(self):
        file = filedialog.askopenfile(mode='r', filetypes=[('Text Files', '*.mp3')])
        if file:
            filepath = os.path.abspath(file.name)
            self.mp3_file = file.name
            self.mp3_file_path.config(text = file.name)
    
    def open_file_text(self):
        file = filedialog.askopenfile(mode='r', filetypes=[('Text Files', '*.txt')])
        if file:
            filepath = os.path.abspath(file.name)
            self.output_file_path = file.name
            self.output_file_path_lb.config(text = file.name)

            
    def translate(self):
        #reading from audio mp3 file
        if self.mp3_file is None:
            return
        
        if self.output_file_path is None :
            self.output_file_path = "output.txt" 

        # check if folder bad exists 
        path = "bad/"
        if not os.path.exists(path):
            showinfo(message='create a folder a name bad in your folder ')
            return
        
        sound = AudioSegment.from_mp3(self.mp3_file)
        
        # spliting audio files
        audio_chunks = split_on_silence(sound, min_silence_len=1000, silence_thresh=-40,keep_silence=150 )


        r = sr.Recognizer()
        #loop is used to iterate over the output list
        self.max_progress = len(audio_chunks)
        tempWavFile = tempfile.mktemp('.wav')

        with open(self.output_file_path,"a") as file :
            for i, chunk in enumerate(audio_chunks):
                if len(chunk) < 1000:
                    continue
                chunk.export(tempWavFile, format="wav")

                with sr.AudioFile(tempWavFile) as source:
                    audio = r.record(source)              
                    try :
                        x = r.recognize_google(audio , language="ta-IN")
                        file.write(f"{x} \n")
                    except :
                        print("bad source",len(chunk))
                        chunk.export(f"bad/bad_source{i}.wav",format ="wav")
                self.progress()
        self.progress()



if __name__ == "__main__":
    # initialize tkinter
    root = Tk()
    root.geometry("500x400")
    root.resizable(False,False)
    app = Window(root)
    app.place(x=0,y=0)
    # set window title
    root.wm_title("Tkinter window")
    root.title("transcribe")
    # show window
    root.mainloop()