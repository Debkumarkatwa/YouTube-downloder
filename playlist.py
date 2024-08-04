from ttkbootstrap import *
from tkinter import messagebox, Listbox
from pytubefix import Playlist, exceptions, YouTube
from tkinter.filedialog import askdirectory


def Lode_Data(url, mode, path=None):  # Function to load the playlist data
    # Destroy all existing widgets in frame4
    for i in (frame4.winfo_children()): i.destroy()
    # Ask for a directory path if path is True
    selected_path = askdirectory() if path is True else None
    # Create BooleanVar objects for checkboxes
    all, specific = BooleanVar(frame4, 1), BooleanVar(frame4)

    global raw_data
    try:
        # Get the playlist data
        raw_data = Playlist(url)
        print(raw_data.title)
        # urllib.request.urlretrieve(raw_data.thumbnail_url, "thumbnail.jpg")        #---"for downloading thumbnail"
    except exceptions.VideoUnavailable:
        messagebox.showwarning('ERROR', 'Video is unavailable')
        return
    except exceptions.RegexMatchError:
        messagebox.showwarning('ERROR', 'Invalid URL')
        return
    except:
        messagebox.showwarning('ERROR', 'Sorry!! Something went wrong')
        return

    # Create a label to show the playlist title
    Label(frame4, text=f'"{raw_data.title[0:min(len(raw_data.title),68)]}..."', border=10, relief='solid', foreground='white', font=('Imprint MT Shadow', 10)).grid(row=0, column=0, columnspan=5, sticky='w')

    # Create a label to show the number of videos in the playlist
    Label(frame4, text=f'Contains {len(raw_data.videos)} Videos. Want to Download ---', border=10, relief='solid', foreground='white', font=('Imprint MT Shadow', 10)).grid(row=1, column=0, columnspan=2, sticky='w')

    # Create checkboxes for selecting all videos or specific videos
    Checkbutton(frame4, text='All Videos  ', bootstyle='info-round-toggle', variable=all, command=lambda: specific.set(value=not(all.get()))).grid(row=1, column=2)
    Checkbutton(frame4, text='Specific Videos ', bootstyle='info-round-toggle', variable=specific, command=lambda: all.set(value=not(specific.get()))).grid(row=1, column=3)

    # Show the selected path if available
    if selected_path is not None:
        Label(frame4, text='Selected Path', border=10, relief='solid', background='light blue', foreground='black', font=('Imprint MT Shadow', 10)).grid(row=2, column=0, sticky='e')
        Label(frame4, text=selected_path[-min(len(selected_path),38):], border=10, relief='solid', foreground='white', font=('Imprint MT Shadow', 10), width=35).grid(row=2, column=1, columnspan=2, sticky='w', ipady=1)

    # Create a button to start the download
    Button(frame4, text='Download', command=lambda: Download_file(all.get(), mode, selected_path), bootstyle='warning').grid(row=2, column=3, ipady=3)


def Download_file(all, mode, path):
    def Download_specific(video:tuple, mode, path):  # function for specific videos it run when submit button is pressed
        if mode is False:
            print('Downloading specific Audio')
            for i in video:
                audio_download = raw_data.videos[i].streams.get_audio_only()
                audio_download.download(filename=f"{raw_data.videos[i].title}.mp3", output_path=path)
        else:
            print('Downloading specific video')
            for i in video:
                video_download = raw_data.videos[i].streams.get_highest_resolution()
                video_download.download(filename=f"{raw_data.videos[i].title}.mp4", output_path=path)
        messagebox.showinfo('Download', 'Downloaded Successfully')
        Window.destroy()

    if all is False:  # check if all videos are selected or specific videos
        Window=Toplevel(win, position=(450,150), resizable=(0,0))
        Window.title('YT Video Downloder')
        Window.geometry('400x250')

        Label(Window, text = "Select Videos........... ", font = ("Times New Roman", 18)).pack(padx = 5, pady = 5) 
        fra1=Frame(Window, bootstyle='success', border=8, relief='sunken')
        fra1.pack()

        yscrollbar = Scrollbar(fra1,bootstyle='info round') ; xscrollbar = Scrollbar(fra1, orient = HORIZONTAL,bootstyle='info round')
        yscrollbar.pack(side = RIGHT, fill = Y) ; xscrollbar.pack(side = BOTTOM, fill = X)
        list = Listbox(fra1, selectmode = "multiple", yscrollcommand = yscrollbar.set, xscrollcommand = xscrollbar.set, height = 8, width = 50)  
        list.pack(padx = 5, pady = 5, expand = YES, fill = "both") 

        for i in (raw_data.videos): 
            list.insert(END, i.title) 
            list.itemconfig(END, bg = "white", fg = "black", selectbackground = "blue", selectforeground = "white") 

        # Attach listbox to vertical scrollbar 
        yscrollbar.config(command = list.yview) ; xscrollbar.config(command = list.xview)

        Button(Window,text='Download',command=lambda:Download_specific(list.curselection(), mode, path),bootstyle='outline-warning').pack()
        Window.mainloop()
        return 

    if mode is False:
        for i in raw_data.videos:
            audio_download = i.streams.get_audio_only()
            audio_download.download(filename=f"{i.title}.mp3", output_path=path)
    else:
        for i in raw_data.videos:
            video_download = i.streams.get_highest_resolution()
            video_download.download(filename=f"{i.title}.mp4", output_path=path)
    messagebox.showinfo('Download', 'Downloaded Successfully')

 
def single_video():  # Function to download a single video
    def download_File(url,mode,path=None):  # it run when submit button is pressed
        Label(frame_,text='Downloading....',border=10,relief='solid',background='red',foreground='white',font=('Imprint MT Shadow',15),width=20).grid(row=1,column=1)
        
        try:        url=YouTube(url)
        except:     messagebox.showerror('ERROR', 'SORRY!! Something Went Wrong') ; return
        
        path = askdirectory() if path is True else None
        if mode is False:
            # Download audio file
            url.streams.get_audio_only.download(filename=f"{url.title}.mp3",output_path=path)
        else:
            # Download video file
            url.streams.get_highest_resolution.download(filename=f"{url.title}.mp4",output_path=path)

        messagebox.showinfo('Download','Downloaded Successfully')
        Window.destroy()
    
    Window=Toplevel(win, position=(480,150), resizable=(0,0))
    Window.title('YT Video Downloder')
    Window.geometry('400x180')
    Window.grid_anchor('center')
    
    Label(Window,text='Download Single Video',font = ("Times New Roman", 18)).grid(row=0,column=0)
    # Entry Frame
    frame_=Labelframe(Window,bootstyle='success',border=8,relief='sunken')
    frame_.grid(row=1,column=0)

    Label(frame_,text='Paste Url',border=10,relief='solid',background='light blue',foreground='black',font=('Imprint MT Shadow',10)).grid(row=0,column=0)
    url=Entry(frame_,foreground='white',width=45,bootstyle='warning')
    url.grid(row=0,column=1,columnspan=3,ipady=2)
    
    # Button Frame
    bframe=Labelframe(frame_,bootstyle='success',border=8,relief='sunken')
    bframe.grid(row=1,column=0,columnspan=4)
    mode,path = BooleanVar(), BooleanVar()
    
    Checkbutton(bframe,text='Covert to Mp4 \t ',bootstyle='info-round-toggle',variable=mode).grid(row=0,column=2)
    Checkbutton(bframe,text='Castom Path \t ',bootstyle='info-round-toggle',variable=path).grid(row=0,column=0)
    Button(bframe,text='Submit',command=lambda:download_File(url.get(),mode.get(),path.get()),bootstyle='warning').grid(row=0,column=3,ipady=3)

    
    Window.mainloop()


# main()-----------------------------------------------------------------------------------
win = Window('YouTube Downloader(mp3/mp4)', 'solar', position=(100, 100))
win.geometry('500x480')
win.resizable(0, 0)

if __name__ == '__main__':
    # Label Frame
    frame0 = Labelframe(win, bootstyle='success', border=8, relief='sunken')
    frame0.grid(row=0, column=0, columnspan=2, ipadx=5)

    Label(frame0, text='Welcome to The Application ', border=10, relief='raised', foreground='white', font=('Imprint MT Shadow', 18, 'bold')).pack()
    Label(frame0, text='Paste a Valid URL to Download Video or Audio', border=10, relief='sunken', foreground='white', font=('Imprint MT Shadow', 15, 'bold')).pack()

    # option Frame
    frame1 = Frame(win, bootstyle='darkly', border=8, relief='sunken')
    frame1.grid(row=1, column=0, ipadx=10, columnspan=2)

    Label(frame1, text='Want to Downlode Single Video--?', border=10, relief='sunken', foreground='white', font=('Imprint MT Shadow', 12, 'bold')).grid(row=0, column=1, ipadx=12, ipady=5)
    Button(frame1, text='Downlode Video', command=lambda: single_video(), bootstyle='warning-outline').grid(row=0, column=3, ipady=3)

# Entry Frame
frame2 = Labelframe(win, bootstyle='success', border=8, relief='sunken')
frame2.grid(row=2, column=0)

Label(frame2, text='Paste Url', border=10, relief='solid', background='light blue', foreground='black', font=('Imprint MT Shadow', 10)).grid(row=0, column=0)
url = Entry(frame2, foreground='white', width=45, bootstyle='warning')
url.grid(row=0, column=1, columnspan=3, ipady=2)

mode = BooleanVar()
path = BooleanVar()
Checkbutton(frame2, text='Covert to Mp4', bootstyle='info-round-toggle', variable=mode).grid(row=1, column=3)
Checkbutton(frame2, text='Select Custom Path', bootstyle='info-round-toggle', variable=path).grid(row=1, column=1)

# Button Frame
frame3 = Frame(win, bootstyle='darkly', border=8, relief='sunken')
frame3.grid(row=2, column=1)

submit = Button(frame3, text='Submit', command=lambda: Lode_Data(url.get(), mode.get(), path.get()), bootstyle='warning')
submit.grid(row=0, column=0, ipady=5, ipadx=5)

# Download Frame
frame4 = Labelframe(win, bootstyle='success', border=8, relief='sunken')
frame4.grid(row=3, column=0, columnspan=2)

win.mainloop()

# -----test-link-----------------------  https://youtube.com/playlist?list=PLzMcBGfZo4-kmY7Nh4kI9kPPnxJ5JMRPj&si=ISKOBKCujO99NQ0P
