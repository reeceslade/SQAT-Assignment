import tkinter as a
from tkinter import filedialog as b, messagebox as c
import pandas as d
import matplotlib.pyplot as e
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as f
from matplotlib.backends.backend_pdf import PdfPages
from tkinter import ttk as g

class h:
    def __init__(self, i):
        self.i = i
        self.i.title("Student Assessment Analysis")
        self.i.geometry("1200x800")

        self.j = None # Holds dataframe
        self.k = a.DoubleVar(value=50.0) # weighting for assessment
        self.l = a.DoubleVar(value=50.0) # weighting for assessment

        
        self.m = a.Button(self.i, text="Load CSV", command=self.n) # when clicked loads self.n (file dialogue)
        self.m.pack(pady=10) # padding to button

        
        self.o = a.Frame(self.i) # Frame for holding assment weighting inputs
        self.o.pack(pady=10) # padding

        a.Label(self.o, text="Assessment 1 weighting (%)").grid(row=0, column=0) # label
        self.p = a.Entry(self.o, textvariable=self.k) # user can input or adjust weightings
        self.p.grid(row=0, column=1)

        a.Label(self.o, text="Assessment 2 Weighting (%)").grid(row=0, column=2) # label
        self.q = a.Entry(self.o, textvariable=self.l) # user can input or adjust weightings
        self.q.grid(row=0, column=3)

        self.k.trace("w", self.r) # Sets up a listener that calls the method self.r whenever the value of self.k or self.l changes. This is used to perform actions based on the weightings (e.g., recalculating grades).
        self.l.trace("w", self.r)

        self.s = a.IntVar(value=0) # track statuses related to assesment such as counts of students who withdrew or interuppted their assessments
        self.t = a.IntVar(value=0)
        self.u = a.IntVar(value=0)
        self.v = a.IntVar(value=0)

        self.w = a.Frame(self.i) # Creates another frame that displays various counts related to student assessments.
        self.w.pack(pady=10)
        a.Label(self.w, text="Withdrawn").grid(row=0, column=0)
        a.Label(self.w, textvariable=self.s).grid(row=0, column=1)
        a.Label(self.w, text="interrupted").grid(row=0, column=2)
        a.Label(self.w, textvariable=self.t).grid(row=0, column=3)

        a.Label(self.w, text="Non Submissions for assessment 1").grid(row=1, column=0)
        a.Label(self.w, textvariable=self.u).grid(row=1, column=1)
        a.Label(self.w, text="Non submissions for assessment 2").grid(row=1, column=2)
        a.Label(self.w, textvariable=self.v).grid(row=1, column=3)

  
        self.x = a.Frame(self.i)
        self.x.pack(pady=10)
        self.y()

  
        self.z = a.Frame(self.i)
        self.z.pack(fill=a.BOTH, expand=True)
        self.aa = None

        self.bb = a.Frame(self.i)
        self.bb.pack(pady=10)
        self.cc, self.dd = e.subplots(1, 3, figsize=(10, 3))

        self.ee()


        self.ff = a.Button(self.i, text="Print Summery and Histograms", command=self.gg)
        self.ff.pack(pady=10)
        
        # SET UP HISTOGRAM PLOTS


    def n(self):
        hh = b.askopenfilename(filetypes=[("CSV Files", "*.csv")]) # Only open csv files
        if hh: # if a file was selected
            try:
                self.j = d.read_csv(hh) # open the csv file
                self.ii()
                self.jj()
                self.kk()
                self.ee()
            except Exception as ll:
                c.showerror("Error", f"Failed to load CSV file.\n{str(ll)}")

    def r(self, *mm):
        try:
            nn = float(self.k.get())
            oo = 100.0 - nn
            self.l.set(oo)
            if self.j is not None:
                self.ii()
                self.jj()
        except ValueError:
            pass

    def ii(self):
        if self.j is not None:
            self.j['Overall'] = (self.j['assessment1'] * self.k.get() / 100) + (self.j['assessment2'] * self.l.get() / 100)
            self.kk()

    def kk(self):
        if self.j is not None:
            self.s.set((self.j['W_or_I'] == 'W').sum())
            self.t.set((self.j['W_or_I'] == 'I').sum())
            self.u.set((self.j['assessment1_NS'] == 'Y').sum())
            self.v.set((self.j['assessment2_NS'] == 'Y').sum())

    def jj(self):
        if self.aa:
            self.aa.destroy()

        self.aa = g.Treeview(self.z, columns=list(self.j.columns), show="headings")
        self.aa.pack(fill=a.BOTH, expand=True)

        for pp in self.j.columns:
            self.aa.heading(pp, text=pp)
            self.aa.column(pp, width=100, anchor="center")

        for _, qq in self.j.iterrows():
            rr = []
            if qq['assessment1'] <= 36 or qq['assessment2'] <= 36 or qq['Overall'] <= 38:
                rr.append("orange")
            elif qq['assessment1'] == 35 or qq['assessment2'] == 35 or qq['Overall'] == 37:
                rr.append("yellow")
            elif qq['assessment1_NS'] == 'Y' or qq['assessment2_NS'] == 'Y':
                rr.append("lightgrey")
            elif qq['W_or_I'] in ['W', 'I']:
                rr.append("darkgrey")
            self.aa.insert("", a.END, values=list(qq), tags=rr)

        self.aa.tag_configure("orange", background="orange")
        self.aa.tag_configure("yellow", background="yellow")
        self.aa.tag_configure("lightgrey", background="lightgrey")
        self.aa.tag_configure("darkgrey", background="darkgrey")

    def ee(self):
        if self.j is not None:
            self.dd[0].cla()
            self.dd[1].cla()
            self.dd[2].cla()

            self.j['assessment1'].plot(kind='hist', ax=self.dd[0], bins=range(0, 101, 5), color='blue', alpha=0.7)
            self.j['assessment2'].plot(kind='hist', ax=self.dd[1], bins=range(0, 101, 5), color='green', alpha=0.7)
            self.j['Overall'].plot(kind='hist', ax=self.dd[2], bins=range(0, 101, 5), color='red', alpha=0.7)

            self.dd[0].set_title('Assessment 1')
            self.dd[1].set_title('Assessment_2')
            self.dd[2].set_title('Overall')

            for ss in self.dd:
                ss.set_xlim(0, 100)
                ss.set_ylim(0, 10)

            self.cc.tight_layout()
            tt = f(self.cc, master=self.bb)
            tt.draw()
            tt.get_tk_widget().pack()

    def y(self):
        uu = [
            ("orange", "At least one assessment below 36 or unit below 38"),
            ("yellow", "At least one assessment at 35 or unit at 37"),
            ("lightgrey", "Non Submissions in row"),
            ("darkgrey", "Withdrawn or Interrupted")
        ]
        for vv, ww in uu:
            xx = a.Frame(self.x)
            xx.pack(anchor='w')
            yy = a.Label(xx, bg=vv, width=2, height=1)
            yy.pack(side=a.LEFT)
            zz = a.Label(xx, text=ww)
            zz.pack(side=a.LEFT)

    def gg(self):

        file_path = b.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            with PdfPages(file_path) as pdf:
               
                fig, axs = e.subplots(1, 3, figsize=(15, 5))
                
                axs[0].hist(self.j['assessment1'], bins=range(0, 101, 5))
                axs[0].set_title('Assessment 1')
                
                axs[1].hist(self.j['assessment2'], bins=range(0, 101, 5))
                axs[1].set_title('Assessment 2')
                
                axs[2].hist(self.j['Overall'], bins=range(0, 101, 5))
                axs[2].set_title('Overall Grade')

                pdf.savefig(fig)
                e.close(fig)

if __name__ == "__main__":
    aaa = a.Tk()
    bbb = h(aaa)
    aaa.mainloop()
