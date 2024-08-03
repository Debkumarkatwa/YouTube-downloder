from ttkbootstrap import *
from tkinter import messagebox
from pytubefix import Playlist, exceptions
from tkinter.filedialog import askdirectory

def Lode_Data(url, mode, path=None):

    # Destroy all existing widgets in frame4
    for i in (frame4.winfo_children()): i.destroy()

    # Ask for a directory path if path is True
    selected_path = askdirectory() if path is True else None

    # Create a label to show "Please Wait..."
    lable = Label(frame4, text='Please Wait...', border=10, relief='solid', foreground='white', font=('Imprint MT Shadow', 10))
    lable.grid(row=0, column=0, ipadx=10, sticky='w')

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
        lable.destroy()
        return
    except exceptions.RegexMatchError:
        messagebox.showwarning('ERROR', 'Invalid URL')
        lable.destroy()
        return
    except:
        messagebox.showwarning('ERROR', 'Sorry!! Something went wrong')
        lable.destroy()
        return

    # Destroy the "Please Wait..." label
    lable.destroy()

    # Create a label to show the playlist title
    Label(frame4, text=f'"{raw_data.title[0:min(len(raw_data.title),68)]}..."', border=10, relief='solid', foreground='white', font=('Imprint MT Shadow', 10)).grid(row=0, column=0, columnspan=5, sticky='w')

    # Create a label to show the number of videos in the playlist
    Label(frame4, text=f'Contains {len(raw_data.videos)} Videos. Want to Download ---', border=10, relief='solid', foreground='white', font=('Imprint MT Shadow', 10)).grid(row=1, column=0, columnspan=2, sticky='w')

    # Create checkboxes for selecting all videos or specific videos
    Checkbutton(frame4, text='All Video  ', bootstyle='info-round-toggle', variable=all, command=lambda: specific.set(value=0)).grid(row=1, column=2)
    Checkbutton(frame4, text='Specific Video', bootstyle='info-round-toggle', variable=specific, command=lambda: all.set(value=0)).grid(row=1, column=3)

    # Show the selected path if available
    if selected_path is not None:
        Label(frame4, text='Selected Path', border=10, relief='solid', background='light blue', foreground='black', font=('Imprint MT Shadow', 10)).grid(row=2, column=0, sticky='e')
        Label(frame4, text=selected_path, border=10, relief='solid', foreground='white', font=('Imprint MT Shadow', 10)).grid(row=2, column=1, sticky='w', ipady=1)

    # Create a button to start the download
    Button(frame4, text='Download', command=lambda: Download_file(all.get(), mode, selected_path), bootstyle='warning').grid(row=2, column=3, ipady=3)


def Download_file(all, mode, path):
    def Download_specific(video, mode, path):
        if mode is False:
            print('Downloading specific Audio')
            for i in raw_data.videos:
                audio_download = i.streams.get_audio_only()
                audio_download.download(filename=f"{i.title}.mp3", output_path=path)
        else:
            print('Downloading specific video')
            for i in raw_data.videos:
                video_download = i.streams.get_highest_resolution()
                video_download.download(filename=f"{i.title}.mp4", output_path=path)
    
    if all is True:
        if mode is False:
            for i in raw_data.videos:
                audio_download = i.streams.get_audio_only()
                audio_download.download(filename=f"{i.title}.mp3", output_path=path)
        else:
            for i in raw_data.videos:
                video_download = i.streams.get_highest_resolution()
                video_download.download(filename=f"{i.title}.mp4", output_path=path)

    else:
        window=Toplevel(win)
        window.geometry('200x100')
        window.resizable(0,0)
        Label(window,text='Select Videos',border=10,relief='solid',background='light blue',foreground='white',font=('Imprint MT Shadow',10)).grid(row=0,column=0,sticky='w')
        select=Combobox(window,values=[i.title for i in raw_data.videos],bootstyle='primary')
        select.grid(row=0,column=1,ipady=3)
        Button(window,text='Download',command=lambda:Download_specific(raw_data.videos[select.current()],mode,path),bootstyle='outline-warning').grid(row=1,column=1,ipady=3)

    messagebox.showinfo('Download', 'Downloaded Successfully')
    


# main()-----------------------------------------------------------------------------------
win = Window('YouTube Downloader(mp3/mp4)', 'solar', position=(100, 100))
win.geometry('500x500')
win.resizable(0, 0)

if __name__ == '__main__':
    # Label Frame
    frame0 = Labelframe(win, bootstyle='success', border=8, relief='sunken')
    frame0.grid(row=0, column=0, columnspan=2)

    Label(frame0, text='Welcome to The Application ', border=10, relief='solid', foreground='white', font=('Imprint MT Shadow', 18, 'bold')).pack()
    Label(frame0, text='Paste a Valid URL to Download Video or Audio', border=10, relief='sunken', foreground='white', font=('Imprint MT Shadow', 15, 'bold')).pack()

    # option Frame
    frame1 = Frame(win, bootstyle='darkly', border=8, relief='ridge')
    frame1.grid(row=1, column=0, ipadx=10, columnspan=2)

    Label(frame1, text='Want to Downlode Single Video--?', border=10, relief='solid', foreground='white', font=('Imprint MT Shadow', 12, 'bold')).grid(row=0, column=1, ipadx=12)
    Button(frame1, text='Downlode Video', command=lambda: print('Yes'), bootstyle='warning-outline').grid(row=0, column=3, ipady=3)

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

# Progressbar(win).pack()
