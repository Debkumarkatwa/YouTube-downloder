from ttkbootstrap import *
from tkinter import messagebox
from pytubefix import YouTube, exceptions, Playlist
from tkinter.filedialog import askdirectory


def Lode_Data(url,mode,path=None):
    # Clear the frame before loading new data
    for i in (frame4.winfo_children()): i.destroy()

    # Ask for a directory path if path is True
    selected_path=askdirectory() if path is True else None
    
    try:
        raw_data = YouTube(url)
        print(raw_data.title)
        # urllib.request.urlretrieve(raw_data.thumbnail_url, "thumbnail.jpg")        #---"for downloading thumbnail"
    except exceptions.VideoUnavailable:
        messagebox.showwarning('ERROR','Video is unavailable')
        return
    except exceptions.RegexMatchError:
        messagebox.showwarning('ERROR','Invalid URL')
        return
    except:
        messagebox.showwarning('ERROR','Sorry!! Something went wrong')
        return
    
    global quality,title,video_download,audio_download
    quality = []
    title = raw_data.title

    if mode is True:
        # Get video streams and filter for progressive streams
        video_download = raw_data.streams.filter(type='video',progressive=True)
        recommended=raw_data.streams.get_highest_resolution()
        for i in video_download:
            if i==recommended:
                quality.append(i.resolution + f'        ({(i.filesize)/(1024*1024):.2f}MB)' + '  [recommended]' )
            else:
                quality.append(i.resolution + f'        ({(i.filesize)/(1024*1024):.2f}MB)' )

        select_quality(True,selected_path)
    else:
        # Get audio streams
        audio_download = raw_data.streams.filter(only_audio=True)
        recommended=raw_data.streams.get_audio_only()
        for i in audio_download:
            if i==recommended:
                quality.append(i.abr + f'        ({(i.filesize)/(1024*1024):.2f}MB)' + '  [recommended]' )
            else:
                quality.append(i.abr + f'        ({(i.filesize)/(1024*1024):.2f}MB)' )

        select_quality(False,selected_path)


def select_quality(mode=None,path=None):
    if path is not None:
        # Display selected path
        Label(frame4,text='Selected Path',border=5,relief='solid',background='light blue',foreground='black',font=('Imprint MT Shadow',10), width=13).grid(row=0, column=0, ipadx=5, sticky='e')
        Label(frame4,foreground='white',text=path[-min(len(path),65):],border=5,relief='solid',font=('Imprint MT Shadow',10), width=51).grid(row=0,column=1,columnspan=4,sticky='w')
        
    # Display video title
    Label(frame4,text=f'Video Founded....\n{title[0:min(len(title),72)]}....',border=5,relief='solid',foreground='white',font=('Imprint MT Shadow',10), width=66).grid(row=1,column=0,columnspan=5,ipady=2,sticky='w')

    # Display select quality label
    Label(frame4,text='Select Quality',border=10,relief='solid',background='light blue',foreground='black',font=('Imprint MT Shadow',10), width=13).grid(row=2,column=0)
    
    # Create a combobox to select quality
    selected_quality=Combobox(frame4,values=quality,state='readonly',bootstyle='danger',width=39)
    selected_quality.grid(row=2,column=1,columnspan=3,ipady=1)
    selected_quality.current(0)
    
    # Create a download button
    Button(frame4,text='Download',command=lambda:Download_file(selected_quality.current(),mode,path), width=13).grid(row=2,column=4,sticky='e')


def Download_file(selected_quality,mode,path=None):
    if mode is False:
        # Download selected audio file
        audio_download[selected_quality].download(filename=f"{title}.mp3",output_path=path)
    else:
        # Download selected video file
        video_download[selected_quality].download(filename=f"{title}.mp4",output_path=path)

    messagebox.showinfo('Download','Downloaded Successfully')


def playlist():  
    def playlist_download(url,mode,path=None):
        Label(frame_,text='Downloading....',border=10,relief='solid',background='red',foreground='white',font=('Imprint MT Shadow',15),width=20).grid(row=1,column=1)
        
        try:        url=Playlist(url)
        except:     messagebox.showerror('ERROR', 'SORRY!! Something Went Wrong') ; return
        
        path = askdirectory() if path is True else None
        if mode is False:
            # Download audio file
            for i in url.videos:
                i.streams.get_audio_only.download(filename=f"{url.title}.mp3",output_path=path)
        else:
            # Download video file
            for i in url.videos:
                i.streams.get_highest_resolution.download(filename=f"{url.title}.mp4",output_path=path)

        messagebox.showinfo('Download','Downloaded Successfully')
        Window.destroy()
      
    Window=Toplevel(win, position=(480,150), resizable=(0,0))
    Window.title('YT Video Downloder')
    Window.geometry('400x180')
    Window.grid_anchor('center')
    
    Label(Window,text='Download Playlist',font = ("Times New Roman", 18)).grid(row=0,column=0)
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
    Button(bframe,text='Submit',command=lambda:playlist_download(url.get(),mode.get(),path.get()),bootstyle='warning').grid(row=0,column=4,ipady=5,ipadx=5)

    
    Window.mainloop()


# main()-----------------------------------------------------------------------------------
win=Window('YouTube Downloader(mp3/mp4)','solar',position=(100,100))
win.geometry('500x500')
win.resizable(0,0)


if __name__ == '__main__':
    # Label Frame
    frame0=Labelframe(win,bootstyle='success',border=8,relief='sunken')
    frame0.grid(row=0,column=0,columnspan=2)

    Label(frame0,text='Welcome to The Application ',border=10,relief='solid',foreground='white',font=('Imprint MT Shadow',18,'bold')).pack()
    Label(frame0,text='Paste a Valid URL to Download Video or Audio',border=10,relief='sunken',foreground='white',font=('Imprint MT Shadow',15,'bold')).pack()

    # option Frame
    frame1=Labelframe(win,bootstyle='success',border=8,relief='sunken')
    frame1.grid(row=1,column=0,ipadx=10,columnspan=2)

    Label(frame1,text='Want to Downlode Whole Playlist--?',border=10,relief='solid',foreground='white',font=('Imprint MT Shadow',12,'bold')).grid(row=0,column=1,ipadx=12)
    Button(frame1,text='Downlode Playlist', command=lambda:playlist(), bootstyle='warning-outline').grid(row=0,column=3,ipady=3)


# Entry Frame
frame2=Labelframe(win,bootstyle='success',border=8,relief='sunken')
frame2.grid(row=2,column=0)

Label(frame2,text='Paste Url',border=10,relief='solid',background='light blue',foreground='black',font=('Imprint MT Shadow',10)).grid(row=0,column=0)
url=Entry(frame2,foreground='white',width=45,bootstyle='warning')
url.grid(row=0,column=1,columnspan=3,ipady=2)

mode=BooleanVar()
path=BooleanVar()
Checkbutton(frame2,text='Covert to Mp4',bootstyle='info-round-toggle',variable=mode).grid(row=1,column=3)
Checkbutton(frame2,text='Select Castom Path',bootstyle='info-round-toggle',variable=path).grid(row=1,column=1)

# Button Frame
frame3=Labelframe(win,bootstyle='success',border=8,relief='sunken')
frame3.grid(row=2,column=1)

submit=Button(frame3,text='Submit',command=lambda:Lode_Data(url.get(),mode.get(),path.get()),bootstyle='warning')
submit.grid(row=0,column=0,ipady=5,ipadx=5)

# Download Frame
frame4=Labelframe(win,bootstyle='success',border=8,relief='sunken')
frame4.grid(row=3,column=0,columnspan=2)

win.mainloop()


# -----test-link-----------------------  https://youtu.be/HGfc06RZyjQ?si=ITkUFe0jViqcB6Pu
