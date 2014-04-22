from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
from socket import gethostbyname,gaierror
from PIL import ImageGrab
import io, random
import mimetypes, ntpath

class MyFrame(Frame):
    
    @classmethod
    def main(cls):
        tkinter.NoDefaultRoot()
        root = tkinter.Tk()
        app = cls(root)
        app.grid(sticky=NSEW)
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        root.resizable(True, False)
        root.mainloop()
        
    def __init__(self):
        Frame.__init__(self)
#        self.resizable(width=FALSE, height=FALSE)
        self.master.title("WP Screenshot Script")
        self.master.rowconfigure(10, weight=1)
        self.master.columnconfigure(5, weight=1)
        self.grid(sticky=W+E+N+S)
        
        self.lab2 = Label(self, width=1, height = 1)
        self.lab2.grid(row=0, column=0)
        
        self.button = Button(self, text="Browse", command=self.load_file, width=20)
        self.button.grid(row=1, column=1, sticky=W+E+N+S)
        
        self.lab = Label(self, width=1, height = 1)
        self.lab.grid(row=2, column=0)
        
        
        self.lab3 = Label(self, width=1, height = 3)
        self.lab3.grid(row=3, column=0)
        
        self.readfromclipboard = Button(self, text="Read From Clipboard", justify=CENTER, wraplength=60, command=self.readfromclipboard, width=20)
        self.readfromclipboard.grid(row=3, column=1, sticky = W+E+N+S)
        
##        self.status = Label(self, width=25, height = 1, text="ready")
##        self.status.grid(row=4, column=1)
##        self.lab4 = Label(self, width=1, height = 1)
##        self.lab4.grid(row=5, column=0)
        
        self.status = Text(height=1, borderwidth=1, width = 40)
        self.status.grid(row=5, column=0, sticky = W+E+N+S, padx = 12)
        self.status.insert(1.0, "ready")
        self.status.configure(state="disabled")
#        self.status.configure(inactiveselectbackground=w.cget("selectbackground"))
        
        
    def path_leaf(path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)
    
    def load_file(self):
        fname = askopenfilename(filetypes=(("PNG Image", "*.png"),
                                           ("JPG Image", "*.jpg;*.jpeg"),
                                           ("GIF Image", "*.gif"),
                                           ("Bitmap Image", "*.bmp"),
                                           ("All Files", "*")))
        print(mimetypes.guess_type(fname)[0])
        try:
            wp = Client('https://your.wordpress.installation/xmlrpc.php', 'Username', 'password')
        except TimeoutError:
            self.status.delete(0, END)
            self.status.insert(0, 'Unable to connect to WP')
        except gaierror:
            self.status.config(state=NORMAL)
            self.status.delete(1.0, END)
            self.status.insert(1.0, 'DNS lookup failed')
            self.status.config(state=DISABLED)
            raise

        print(MyFrame.path_leaf(fname))
        data = {'name': MyFrame.path_leaf(fname), 'type': mimetypes.guess_type(fname)[0]}
        with open(fname, 'rb') as img:
            data['bits'] = xmlrpc_client.Binary(img.read())
        response = wp.call(media.UploadFile(data))
        print(response['url'])
        self.status.config(state=NORMAL)
        self.status.delete(1.0, END)
        self.status.insert(1.0, 'Link: '+response['url'])
        self.status.config(state=DISABLED)

    def readfromclipboard(self):
        temporarybuffer = io.BytesIO()
        ImageGrab.grabclipboard().save(temporarybuffer, format='png')
##        temporarybuffer.seek(0,2)
##        print(temporarybuffer.tell())
        try:
            wp = Client('https://your.wordpress.installation/xmlrpc.php', 'Username', 'password')
        except TimeoutError:
            self.status.delete(0, END)
            self.status.insert(0, 'Unable to connect to WP')
        except gaierror:
            self.status.config(state=NORMAL)
            self.status.delete(1.0, END)
            self.status.insert(1.0, 'DNS lookup failed')
            self.status.config(state=DISABLED)
            raise
        data = {'name': ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz') for i in range(16))+'.png', 'type': 'image/png'}
        data['bits'] = xmlrpc_client.Binary(temporarybuffer.getvalue())
        response = wp.call(media.UploadFile(data))
        print(response['url'])
        self.status.config(state=NORMAL)
        self.status.delete(1.0, END)
        self.status.insert(1.0, 'Link: '+response['url'])
        self.status.config(state=DISABLED)
            
##        if fname:
##            try:
##                print("""here it comes: self.settings["template"].set(fname)""")
##                print(fname)
###                mimetypes.init()
##                print(str(mimetypes.types_map[fname]))
####                wp = Client('https://your.wordpress.installation/xmlrpc.php', 'Username', 'password')
##                
##            except:                     # <- naked except is a bad idea
##                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
##            return


if __name__ == "__main__":
    MyFrame().mainloop()



##app = Tk()
##app.title("GUI Example")
##app.geometry('450x300+200+200')
##app.mainloop()
