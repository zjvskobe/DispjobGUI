import Tkinter as tk
import ttk
import os

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

class DispjobGUI(tk.Tk, object):
    def __init__(self):
        super(DispjobGUI, self).__init__()
        self.title("DispjobGUI")
        #self.geometry("800x600")
        self.frame_left_top = tk.Frame(width=400, height=200)
        self.frame_right_top = tk.Frame(width=400, height=200)
        self.frame_bottom = tk.Frame(width=800, height=400)

        # define left top
        self.var_entry = tk.StringVar()
        self.jobdir_title = tk.Label(self.frame_left_top, text = "JobDir:")
        self.jobdir_entry = tk.Entry(self.frame_left_top, textvariable=self.var_entry)
        self.jobdir_title.grid(row=0, column=0)
        self.jobdir_entry.grid(row=0, column=1)

        #define right top
        self.update_button = tk.Button(self.frame_right_top, text="ClickUpdate")
        self.update_button.grid(row=0, column=1)

        #define bottom:
        self.tree = ttk.Treeview(self.frame_bottom, show="headings", height=18, columns=("a", "b", "c", "d"))
        self.vbar = ttk.Scrollbar(self.frame_bottom, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vbar.set)

        self.tree.column("a", width=50, anchor='center')
        self.tree.column("b", width=550, anchor='center')
        self.tree.column("c", width=100, anchor='center')
        self.tree.column("d", width=100, anchor='center')
        self.tree.heading("a", text="JobID")
        self.tree.heading("b", text="JobDir")
        self.tree.heading("c", text="Completed")
        self.tree.heading("d", text="JobStatus")
        self.gettree()
        self.tree.grid(row=0, column=0, sticky=tk.NSEW)
        self.vbar.grid(row=0, column=1, sticky=tk.NS)

        #define golbal:
        self.frame_left_top.grid(row=0, column=0, sticky=tk.EW)
        self.frame_right_top.grid(row=0, column=1,sticky=tk.EW)
        self.frame_bottom.grid(row=1, column=0, columnspan=2)


        #self.frame_left_top.grid_propagate(0)
        #self.frame_right_top.grid_propagate(0)
        #self.frame_bottom.grid_propagate(0)

    def dispjob(self):
        workDir = 'JobDirs'
        jobDirs = os.listdir(workDir)
        currentPath = os.getcwd()
        jobInfo = []
        for dir in jobDirs:
            current_dir = currentPath+"\\"+workDir+"\\"+dir
            force_file = current_dir + "\\" + 'force_glb.out'
            last_line = readLastLineofFile(force_file)
            force_info = last_line.rstrip().split()
            total_step = 10 # this need parsing from input.par, given a temp
            iter_step = int(force_info[0])
            complete_rate = '%.1f%%' % (iter_step*100.0/total_step)
            #print complete_rate
            jobInfo.append((dir, complete_rate, 'R'))
        return jobInfo

    def gettree(self):
        jobInfos = self.dispjob()
        for i, jobInfo in enumerate(jobInfos):
            self.tree.insert("", i, values=(i, jobInfo[0], jobInfo[1], jobInfo[2]))
if __name__ == '__main__':
    dispjob = DispjobGUI()
    dispjob.mainloop()
    #dispjob.dispjob()
    pass