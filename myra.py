# Myra
A simple and easy to use music player.


from tkinter import *
from tkinter import ttk, messagebox, filedialog
import os ,time,threading
from mutagen.mp3 import MP3
from pygame import mixer
from ttkthemes import themed_tk as tk


main_app = tk.ThemedTk()
main_app.get_themes()
main_app.set_theme("radiance")


### Create Menu

menu_bar=Menu(main_app)
main_app.config(menu=menu_bar)

submenu =Menu(menu_bar,tearoff=0)
menu_bar.add_cascade(menu=submenu,label="File")

status_bar_label=ttk.Label(main_app,text="Welcom To Myra",relief=SUNKEN)
status_bar_label.pack(side=BOTTOM,fill=X)

left_frame=ttk.Frame(main_app)
left_frame.pack(side=LEFT,anchor=N,padx=50,pady=70)



right_frame=ttk.Frame(main_app)
right_frame.pack(pady=30)

top_frame=ttk.Frame(right_frame)
top_frame.pack(pady=10)

playlist = []

def chose_file():
    global url
    url = filedialog.askopenfilename(initialdir=os.getcwd(), title= "Select File",filetypes=(('Mp3 File','*.mp3'),('All Files','*.*')))
    add_toplaylist(url)

def add_toplaylist(filename):
    filename = os.path.basename(url)
    index = 0
    playlist_box.insert(index,filename)
    playlist.insert(index,url)
    index +=1
    


def del_musicfile():
    selected_song=playlist_box.curselection()
    selected_song=int(selected_song[0])
    playlist_box.delete(selected_song)
    playlist.pop(selected_song)

playlist_box = Listbox(left_frame)
playlist_box.pack()

add_btn = ttk.Button(left_frame,text="+ Add",command=chose_file)
add_btn.pack(side =LEFT)

del_btn = ttk.Button(left_frame,text="- Del",command=del_musicfile)
del_btn.pack(side=LEFT)

lengthlabel=ttk.Label(top_frame,text="Total Length -  --:--")
lengthlabel.pack(pady=10)

currenttime_label=ttk.Label(top_frame,text="Current Time -  --:-- ",relief=GROOVE)
currenttime_label.pack()




def show_details(play_song):

    file_type= os.path.splitext(play_song)

    if file_type[1]=='.mp3':
        audio=MP3(play_song)
        total_length=audio.info.length
    else:
        a=mixer.Sound(play_song)
        total_length=a.get_length()
    
    mins, secs=divmod(total_length,60)
    mins=round(mins)
    secs=round(secs)

    timeformat="{:02d}:{:02d}".format(mins,secs)
    lengthlabel['text']="Total Length - " + timeformat

    thread = threading.Thread(target=start_count,args=(total_length,))
    thread.start()
    

def start_count(t):
    global paused
    x=0
    while x<=t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs=divmod(x,60)
            mins=round(mins)
            secs=round(secs)    
            timeformat="{:02d}:{:02d}".format(mins,secs)
            currenttime_label['text']="Current Time - " + timeformat
            time.sleep(1)
            x +=1


### PLAY MUSIC 

playing_music=BooleanVar()
playing_music=FALSE

def play_music():
    global playing_music
    playing_music=TRUE
    global paused
    if paused:
        mixer.music.unpause()   
        status_bar_label['text']="Music Resume"
        paused=FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlist_box.curselection()
            selected_song = int(selected_song[0])
            playit = playlist[selected_song]
            mixer.music.load(playit)
            mixer.music.play()
            status_bar_label['text']="Playing "+ os.path.basename(playit)
            show_details(playit)
        except:
             messagebox.showerror("File Not Found",'Myra couldnt find any file to play')
          

def exit_func():
    if playing_music:
        mbox = messagebox.askyesno("Exit","Are You Sure You Want To Exit ?")
        if mbox is True:
            stop_music()
            main_app.destroy()

    else:
        main_app.destroy()


submenu.add_command(label="Choose File",command=chose_file)
submenu.add_command(label="Exit",command=exit_func)

### About Myra Function To show message box

def about_myra():
    messagebox.showinfo("About Us","Myra Music Player : To Play Your Own Music")

submenu =Menu(menu_bar,tearoff=0)
menu_bar.add_cascade(menu=submenu,label="Help")
submenu.add_command(label="About Myra",command=about_myra)


mixer.init()  # initializing the mixer

main_app.title("Myra")
main_app.geometry('780x400')
main_app.resizable(0,0)
main_app.iconbitmap(r'New folder\movie.ico')



### IMAGE ICONS

play_img = PhotoImage(file=r"New folder\myra_icons\play.png")
stop_img = PhotoImage(file=r'New folder\myra_icons\stop (1).png')
pause_img = PhotoImage(file=r"New folder\myra_icons\pause.png")
mute_img = PhotoImage(file=r"New folder\myra_icons\001-mute-1.png")
sound_img = PhotoImage(file=r"New folder\myra_icons\004-speaker.png")



### STOP MUSIC 

def stop_music():
    playing_music=FALSE
    mixer.music.stop() 
    status_bar_label['text']="music stopped" 

### Frames
middle_frame=ttk.Frame(right_frame)
middle_frame.pack(pady=10)

bottom_frame=ttk.Frame(right_frame)
bottom_frame.pack(pady=10)

### PLAY BUTTON

play_btn = ttk.Button(middle_frame,image=play_img,command=play_music)
play_btn.grid(row=0,column=0,padx=10)

#### STOP BUTTON

stop_btn = ttk.Button(middle_frame,image=stop_img,command=stop_music)
stop_btn.grid(row=0,column=1,padx=10)

paused = FALSE
def pause_music():
    global paused
    paused=TRUE
    mixer.music.pause()
    status_bar_label['text']="music paused" 

## pause_btn

pause_btn=ttk.Button(middle_frame,image=pause_img,command=pause_music)
pause_btn.grid(row=0,column=3,padx=10)




def set_vol(val):
   volume = float(val) / 100
   mixer.music.set_volume(volume)
   

mixer.music.set_volume(.4)
scale = ttk.Scale(bottom_frame,from_ = 0,to=100,length=150,orient=HORIZONTAL,command=set_vol)
scale.set(40)
scale.grid(row=0,column=1,padx=15)

### Staus Bar





muted = FALSE


def mute_music():
    global muted
    if muted:
        sound_btn.configure(image=sound_img)
        mixer.music.set_volume(.4)
        scale.set(40)
        muted=FALSE
    else:
        sound_btn.configure(image=mute_img)
        mixer.music.set_volume(0)
        scale.set(0)
        muted=TRUE


### sound button
sound_btn=ttk.Button(bottom_frame,image=sound_img,command=mute_music)
sound_btn.grid(row=0,column=0,padx=5)

def on_closing():
    if playing_music:
        mbox = messagebox.askyesno("Exit","Are You Sure You Want To Exit ?")
        if mbox is True:
            stop_music()
            main_app.destroy()

    else:
        main_app.destroy()

main_app.protocol("WM_DELETE_WINDOW",on_closing)
 
main_app.mainloop()


