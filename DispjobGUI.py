import Tkinter as tk
import tkFileDialog
import tkMessageBox
import ttk
import os
from matplotlib.pyplot import figure, show, title
from matplotlib.figure import Figure


# read big file's last line:
def readLastLineofFile(filename):
    with open(filename) as f:
        first_line = f.readline()
        off = -50
        while True:
            f.seek(off, 2)
            lines = f.readlines()
            if len(lines)>=2:
                last_line = lines[-1]
                break
            off *= 2
    return last_line


def readForceFile(filename):
    iter=[]
    CL = []
    CD = []
    with open(filename) as f:
        f.readline()
        while True:
            line = f.readline()
            if not line:
                break
            #print line
            line_split = line.rstrip().split()
            iter.append(int(line_split[0]))
            CL.append(float(line_split[1]))
            CD.append(float(line_split[2]))
    return (iter, CL, CD)


class MyFigure(Figure):
    def __init__(self, *args, **kwargs):
        """
        custom kwarg figtitle is a figure title
        """
        figtitle = kwargs.pop('figtitle')
        Figure.__init__(self, *args, **kwargs)
        self.text(0.5, 0.95, figtitle, ha='center')


class DispjobGUI(tk.Tk, object):
    def __init__(self):
        super(DispjobGUI, self).__init__()
        self.jobInfos = []

        self.title("DispjobGUI")
        self.geometry("800x600")
        self.frame_left_top = tk.Frame(self)
        self.frame_right_top = tk.Frame(self)
        self.frame_bottom = tk.Frame(self)

        # define left top
        self.workdir_path = tk.StringVar()
        #default is current dir:
        self.workdir_path.set(os.getcwd())
        self.workdir_title = tk.Label(self.frame_left_top, text ="WorkingDir:")
        self.workdir_entry = tk.Entry(self.frame_left_top, textvariable=self.workdir_path, width=40)
        self.askdir_button = tk.Button(self.frame_left_top, text='...', command=self.openjobdir)

        self.exefile_path = tk.StringVar()
        self.exefile_title = tk.Label(self.frame_left_top, text="Executable:")
        self.exefile_entry = tk.Entry(self.frame_left_top, textvariable=self.exefile_path, width=40)
        self.askexe_button = tk.Button(self.frame_left_top, text='...', command=self.openexefile)

        self.cores_var = tk.StringVar()
        self.cores_var.set(0)
        self.cores_title = tk.Label(self.frame_left_top, text = "Cores:")
        self.cores_entry = tk.Entry(self.frame_left_top, textvariable=self.cores_var, width=5)

        self.workdir_title.grid(row=0, column=0, padx=5, sticky=tk.E)
        self.workdir_entry.grid(row=0, column=1)
        self.askdir_button.grid(row=0, column=2, padx=5)
        self.exefile_title.grid(row=1, column=0, padx=5, sticky=tk.E)
        self.exefile_entry.grid(row=1, column=1)
        self.askexe_button.grid(row=1, column=2, padx=5)
        self.cores_title.grid(row=2, column=0, padx=5, sticky=tk.E)
        self.cores_entry.grid(row=2, column=1, sticky=tk.W)

        #define right top
        self.update_button = tk.Button(self.frame_right_top, text="Update", width=10, command=self.updatetree)
        self.update_button.grid(row=0, column=0)
        self.submit_button = tk.Button(self.frame_right_top, text="Submit", width=10, command=self.submit)
        self.submit_button.grid(row=0, column=2)
        self.completed_var = tk.StringVar()
        self.completed_var.set(0)
        self.uncompled_var = tk.StringVar()
        self.uncompled_var.set(0)
        self.running_var = tk.StringVar()
        self.running_var.set(0)
        self.pending_var = tk.StringVar()
        self.pending_var.set(0)
        self.completed_title = tk.Label(self.frame_right_top, text="Completed:")
        self.completed_label = tk.Label(self.frame_right_top, textvariable=self.completed_var)
        self.uncompled_title = tk.Label(self.frame_right_top, text="UnCompleted:")
        self.uncompled_label = tk.Label(self.frame_right_top, textvariable=self.uncompled_var)
        self.running_title = tk.Label(self.frame_right_top, text="Running:")
        self.running_label = tk.Label(self.frame_right_top, textvariable=self.running_var)
        self.pending_title = tk.Label(self.frame_right_top, text="Pending:")
        self.pending_label = tk.Label(self.frame_right_top, textvariable=self.pending_var)
        self.completed_title.grid(row=1, column=0, sticky=tk.E)
        self.completed_label.grid(row=1, column=1)
        self.running_title.grid(row=1, column=2, sticky=tk.E)
        self.running_label.grid(row=1, column=3)
        self.uncompled_title.grid(row=2, column=0, sticky=tk.E)
        self.uncompled_label.grid(row=2, column=1)
        self.pending_title.grid(row=2, column=2, sticky=tk.E)
        self.pending_label.grid(row=2, column=3)

        #define bottom:
        self.tree = ttk.Treeview(self.frame_bottom, show="headings", height=18, columns=("a", "b", "c", "d"))
        self.vbar = ttk.Scrollbar(self.frame_bottom, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vbar.set)
        self.tree.bind("<Double-1>", self.ondouble_click)
        self.tree.column("a", width=50, anchor='center')
        self.tree.column("b", width=550, anchor='center')
        self.tree.column("c", width=100, anchor='center')
        self.tree.column("d", width=100, anchor='center')
        self.tree.heading("a", text="JobID")
        self.tree.heading("b", text="JobDir")
        self.tree.heading("c", text="Completed")
        self.tree.heading("d", text="JobStatus")
        self.tree.grid(row=0, column=0, sticky=tk.NSEW)
        self.vbar.grid(row=0, column=1, sticky=tk.NS)
        self.frame_bottom.columnconfigure(0, weight=1)
        self.frame_bottom.rowconfigure(0, weight=1)

        #define golbal:
        self.frame_left_top.grid(row=0, column=0, sticky=tk.EW)
        self.frame_right_top.grid(row=0, column=1,sticky=tk.EW)
        self.frame_bottom.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

    def dispjob(self, workDir):
        #print workDir
        jobDirs = os.listdir(workDir)
        #print jobDirs
        jobInfo = []
        for dir in jobDirs:
            current_dir = workDir+"\\"+dir
            force_file = current_dir + "\\" + 'force_glb.out'
            last_line = readLastLineofFile(force_file)
            force_info = last_line.rstrip().split()
            total_step = 10 # this need parsing from input.par, given a temp
            iter_step = int(force_info[0])
            complete_rate = '%.1f%%' % (iter_step*100.0/total_step)
            #print complete_rate
            jobInfo.append((current_dir, complete_rate, 'R'))
        return jobInfo

    def updatetree(self):
        askmessage = "Update jobs in "+self.workdir_path.get()+"?"
        if tkMessageBox.askyesno(message=askmessage) :
            # clear old content
            map(self.tree.delete, self.tree.get_children(""))
            self.jobInfos = self.dispjob(self.workdir_path.get())
            self.running_var.set(len(self.jobInfos))
            for i, jobInfo in enumerate(self.jobInfos):
                self.tree.insert("", i, values=(i, jobInfo[0], jobInfo[1], jobInfo[2]))

    def openjobdir(self):
        self.workdir_path.set(tkFileDialog.askdirectory())

    def openexefile(self):
        self.exefile_path.set(tkFileDialog.askopenfilename())

    def submit(self):
        askmessage = "Submit by command \"xrmpi "+self.cores_var.get()+" "+self.exefile_path.get()+"\"?"
        if tkMessageBox.askyesno(message=askmessage):
            pass

    def ondouble_click(self, event):
        '''
        item = self.tree.selection()[0]
        print "you clicked on", self.tree.item(item, "values")
        tl = tk.Toplevel(self)
        tl_label = tk.Label(tl, text=self.tree.item(item, "values"))
        tl_label.pack()
        '''
        item = self.tree.selection()[0]
        force_file = self.tree.item(item, "values")[1] + "/force_glb.out"
        iter, CL, CD = readForceFile(force_file)
        fig = figure(FigureClass=MyFigure, figtitle=force_file, figsize=(8, 4))
        plot_CL = fig.add_subplot(121)  # 111 shoud be positon
        plot_CL.plot(iter, CL)
        title("CL")
        plot_CD = fig.add_subplot(122)
        title("CD")
        plot_CD.plot(iter, CD)
        show()

if __name__ == '__main__':
    dispjob = DispjobGUI()
    dispjob.mainloop()
    pass