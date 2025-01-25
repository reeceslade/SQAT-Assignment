import tkinter as tk
from tkinter import filedialog as fd, messagebox as mb
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_pdf import PdfPages
from tkinter import ttk

class StudentAssessmentAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Assessment Analysis")
        self.root.geometry("1200x800")

        self.dataframe = None  # Holds the assessment DataFrame
        self.assessment1_weight = tk.DoubleVar(value=50.0)  # Weight for Assessment 1
        self.assessment2_weight = tk.DoubleVar(value=50.0)  # Weight for Assessment 2

        # Load CSV button
        self.load_csv_button = tk.Button(self.root, text="Load CSV", command=self.load_csv)
        self.load_csv_button.pack(pady=10)

        # Frame for holding assessment weightings
        self.weighting_frame = tk.Frame(self.root)
        self.weighting_frame.pack(pady=10)

        # Labels and entries for assessment weightings
        tk.Label(self.weighting_frame, text="Assessment 1 weighting (%)").grid(row=0, column=0)
        self.assessment1_entry = tk.Entry(self.weighting_frame, textvariable=self.assessment1_weight)
        self.assessment1_entry.grid(row=0, column=1)

        tk.Label(self.weighting_frame, text="Assessment 2 Weighting (%)").grid(row=0, column=2)
        self.assessment2_entry = tk.Entry(self.weighting_frame, textvariable=self.assessment2_weight)
        self.assessment2_entry.grid(row=0, column=3)

        # Trace changes to weightings
        self.assessment1_weight.trace("w", self.update_weights)
        self.assessment2_weight.trace("w", self.update_weights)

        # IntVars to track assessment status counts
        self.withdrawn_count = tk.IntVar(value=0)
        self.interrupted_count = tk.IntVar(value=0)
        self.non_submission1_count = tk.IntVar(value=0)
        self.non_submission2_count = tk.IntVar(value=0)

        # Frame to display counts of assessments
        self.status_frame = tk.Frame(self.root)
        self.status_frame.pack(pady=10)

        # Labels to display counts
        tk.Label(self.status_frame, text="Withdrawn").grid(row=0, column=0)
        tk.Label(self.status_frame, textvariable=self.withdrawn_count).grid(row=0, column=1)
        tk.Label(self.status_frame, text="Interrupted").grid(row=0, column=2)
        tk.Label(self.status_frame, textvariable=self.interrupted_count).grid(row=0, column=3)

        tk.Label(self.status_frame, text="Non Submissions for Assessment 1").grid(row=1, column=0)
        tk.Label(self.status_frame, textvariable=self.non_submission1_count).grid(row=1, column=1)
        tk.Label(self.status_frame, text="Non Submissions for Assessment 2").grid(row=1, column=2)
        tk.Label(self.status_frame, textvariable=self.non_submission2_count).grid(row=1, column=3)

        # Frame for displaying data
        self.data_frame = tk.Frame(self.root)
        self.data_frame.pack(fill=tk.BOTH, expand=True)
        self.create_data_display()

        # Frame for histograms
        self.histogram_frame = tk.Frame(self.root)
        self.histogram_frame.pack(pady=10)

        # Button to print summary and histograms
        self.print_button = tk.Button(self.root, text="Print Summary and Histograms", command=self.print_summary)
        self.print_button.pack(pady=10)

    def load_csv(self):
        file_path = fd.askopenfilename(filetypes=[("CSV Files", "*.csv")])  # Open file dialog for CSV files
        if file_path:  # If a file was selected
            try:
                self.dataframe = pd.read_csv(file_path)  # Load the CSV file into a DataFrame
                self.calculate_overall_grades()
                self.update_counts()
                self.update_data_display()
                self.update_histograms()
            except Exception as e:
                mb.showerror("Error", f"Failed to load CSV file.\n{str(e)}")

    def update_weights(self, *args):
        try:
            assessment1_weight = float(self.assessment1_weight.get())
            assessment2_weight = 100.0 - assessment1_weight  # Calculate Assessment 2 weight
            self.assessment2_weight.set(assessment2_weight)  # Update Assessment 2 weight
            if self.dataframe is not None:
                self.calculate_overall_grades()
                self.update_data_display()
        except ValueError:
            pass

    def calculate_overall_grades(self):
        if self.dataframe is not None:
            self.dataframe['Overall'] = (
                self.dataframe['assessment1'] * self.assessment1_weight.get() / 100 +
                self.dataframe['assessment2'] * self.assessment2_weight.get() / 100
            )
            self.update_counts()

    def update_counts(self):
        if self.dataframe is not None:
            self.withdrawn_count.set((self.dataframe['W_or_I'] == 'W').sum())
            self.interrupted_count.set((self.dataframe['W_or_I'] == 'I').sum())
            self.non_submission1_count.set((self.dataframe['assessment1_NS'] == 'Y').sum())
            self.non_submission2_count.set((self.dataframe['assessment2_NS'] == 'Y').sum())

    def update_data_display(self):
        if hasattr(self, 'data_treeview'):
            self.data_treeview.destroy()

        self.data_treeview = ttk.Treeview(self.data_frame, columns=list(self.dataframe.columns), show="headings")
        self.data_treeview.pack(fill=tk.BOTH, expand=True)

        # Set up column headings and widths
        for column in self.dataframe.columns:
            self.data_treeview.heading(column, text=column)
            self.data_treeview.column(column, width=100, anchor="center")

        # Insert data into the Treeview
        for _, row in self.dataframe.iterrows():
            tags = []
            if row['assessment1'] <= 36 or row['assessment2'] <= 36 or row['Overall'] <= 38:
                tags.append("orange")
            elif row['assessment1'] == 35 or row['assessment2'] == 35 or row['Overall'] == 37:
                tags.append("yellow")
            elif row['assessment1_NS'] == 'Y' or row['assessment2_NS'] == 'Y':
                tags.append("lightgrey")
            elif row['W_or_I'] in ['W', 'I']:
                tags.append("darkgrey")

            self.data_treeview.insert("", tk.END, values=list(row), tags=tags)

        # Configure tag colors
        self.data_treeview.tag_configure("orange", background="orange")
        self.data_treeview.tag_configure("yellow", background="yellow")
        self.data_treeview.tag_configure("lightgrey", background="lightgrey")
        self.data_treeview.tag_configure("darkgrey", background="darkgrey")

    def update_histograms(self):
        if self.dataframe is not None:
            # Clear existing plots
            plt.clf()
            fig, axs = plt.subplots(1, 3, figsize=(15, 5))

            # Create histograms for each assessment
            self.dataframe['assessment1'].plot(kind='hist', ax=axs[0], bins=range(0, 101, 5), color='blue', alpha=0.7)
            self.dataframe['assessment2'].plot(kind='hist', ax=axs[1], bins=range(0, 101, 5), color='green', alpha=0.7)
            self.dataframe['Overall'].plot(kind='hist', ax=axs[2], bins=range(0, 101, 5), color='red', alpha=0.7)

            # Set titles for the histograms
            axs[0].set_title('Assessment 1')
            axs[1].set_title('Assessment 2')
            axs[2].set_title('Overall Grade')

            # Set limits for the histograms
            for ax in axs:
                ax.set_xlim(0, 100)
                ax.set_ylim(0, 10)

            plt.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=self.histogram_frame)
            canvas.draw()
            canvas.get_tk_widget().pack()

    def print_summary(self):
        file_path = fd.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            with PdfPages(file_path) as pdf:
                fig, axs = plt.subplots(1, 3, figsize=(15, 5))
                
                axs[0].hist(self.dataframe['assessment1'], bins=range(0, 101, 5), color='blue')
                axs[0].set_title('Assessment 1')
                
                axs[1].hist(self.dataframe['assessment2'], bins=range(0, 101, 5), color='green')
                axs[1].set_title('Assessment 2')
                
                axs[2].hist(self.dataframe['Overall'], bins=range(0, 101, 5), color='red')
                axs[2].set_title('Overall Grade')

                pdf.savefig(fig)
                plt.close(fig)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentAssessmentAnalyzer(root)
    root.mainloop()
