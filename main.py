import sys
import subprocess
import subprocess as sp
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import  QApplication, QPushButton, QLineEdit
from PyQt4 import QtCore, QtGui
from UI import  Ui_MainWindow
from refined import *
from tkinter import messagebox
import tkinter as tk
 
class main(QtGui.QMainWindow):
     
     def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.le = QLineEdit()
        self.le.setObjectName("host")
        self.le.setText("Host")

        self.pb = QPushButton()
        self.pb.setObjectName("connect")
        self.pb.setText("Connect")
        
        self.connect(self.ui.pushButton1_0, SIGNAL("clicked()"),self.button_display_orginal_model)
        self.connect(self.ui.pushButton1_1, SIGNAL("clicked()"),self.button_edit_orginal_model)
        self.connect(self.ui.pushButton1_2, SIGNAL("clicked()"),self.button_view_orginal_model)
        self.connect(self.ui.pushButton2_0, SIGNAL("clicked()"),self.button_generate_species)
        self.connect(self.ui.pushButton2_1, SIGNAL("clicked()"),self.button_edit_species)
        self.connect(self.ui.pushButton2_2, SIGNAL("clicked()"),self.button_view_species)
        self.connect(self.ui.pushButton3_0, SIGNAL("clicked()"),self.button_generate_atomic_refinment)
        self.connect(self.ui.pushButton3_1, SIGNAL("clicked()"),self.button_edit_atomic_refinment)
        self.connect(self.ui.pushButton3_2, SIGNAL("clicked()"),self.button_view_atomic_refinment)
        self.connect(self.ui.pushButton4_0, SIGNAL("clicked()"),self.button_generate_complex_refinment)
        self.connect(self.ui.pushButton4_1, SIGNAL("clicked()"),self.button_edit_complex_refinment)
        self.connect(self.ui.pushButton4_2, SIGNAL("clicked()"),self.button_view_complex_refinment)
        self.connect(self.ui.pushButton5_0, SIGNAL("clicked()"),self.button_generate_refined_model)
        self.connect(self.ui.pushButton5_1, SIGNAL("clicked()"),self.button_display_refined_model)
        self.connect(self.ui.pushButton5_2, SIGNAL("clicked()"),self.button_view_refined_model)
        
     def button_display_orginal_model(self):
          
          orginal_filename = self.ui.lineEdit_1.text()
          
          try:
               f = open(orginal_filename, "r")
               
               self.ui.textEdit_original_model.clear()
               
               b = print_chemical_reaction(orginal_filename)
               for i in range (0,len(b)):
                    self.ui.textEdit_original_model.append(b[i])
               
          except IOError as e:
               root = tk.Tk()
               root.withdraw()
               messagebox.showerror(title="Error",message=e.strerror + ": '" + e.filename + "'")
          
          
          
          
     def button_edit_orginal_model(self):
          orginal_filename = self.ui.lineEdit_1.text()
          try:
               f = open(orginal_filename, "r")
                     
               if os.name == "darwin":#Mac
                    sp.Popen(["open", orginal_filename]) 
               elif  os.name=='posix': #linux
                    sp.Popen(["gedit", orginal_filename])
               elif  os.name=="nt":     #win
                    sp.Popen( ["write", orginal_filename])
          
          except IOError as e:
               root = tk.Tk()
               root.withdraw()
               messagebox.showerror(title="Error",message=e.strerror + ": '" + e.filename + "'")
                        
                   
     def button_view_orginal_model(self):
          orginal_filename = self.ui.lineEdit_1.text()
          try:
               f = open(orginal_filename, "r")
               if os.name == "darwin":#Mac
                    sp.Popen(["open", orginal_filename]) 
               elif  os.name=='posix': #linux
                    sp.Popen(["firefox", orginal_filename])
               elif  os.name=="nt":     #win
                    sp.Popen(["explorer", orginal_filename])
          except IOError as e:
               root = tk.Tk()
               root.withdraw()
               messagebox.showerror(title="Error",message=e.strerror + ": '" + e.filename + "'")
               
         
          
  #****************************************************************************************************             
                    
     def button_generate_species(self):
          orginal_filename = self.ui.lineEdit_1.text()
          try:
               f = open(orginal_filename, "r")
               dict_species=extract_species(orginal_filename)
               species_filename= self.ui.lineEdit_2.text()
               f = open(species_filename, "w")
               write_species(dict_species,species_filename)
               
          except IOError as e:
               root = tk.Tk()
               root.withdraw()
               messagebox.showerror(title="Error",message=e.strerror + ": '" + e.filename + "'")
         
          
     def button_edit_species(self):
          species_filename= self.ui.lineEdit_2.text()
          try:
               f = open(species_filename, "r")
               if os.name == "darwin":#Mac
                    sp.Popen(["open", species_filename]) 
               elif  os.name=='posix': #linux
                    sp.Popen(["gedit", species_filename])
               elif  os.name=="nt":     #win
                    sp.Popen(["write", species_filename])
          except IOError as e:
               root = tk.Tk()
               root.withdraw()
               messagebox.showerror(title="Error",message=e.strerror + ": '" + e.filename + "'")
          
     def button_view_species(self):
          species_filename= self.ui.lineEdit_2.text()
          
          try:
               f = open(species_filename, "r")
               if os.name == "darwin":#Mac
                    sp.Popen(["open", species_filename]) 
               elif  os.name=='posix': #linux
                    sp.Popen(["firefox", species_filename])
               elif  os.name=="nt":     #win
                    sp.Popen(["explorer", species_filename])
          except IOError as e:
               root = tk.Tk()
               root.withdraw()
               messagebox.showerror(title="Error",message=e.strerror + ": '" + e.filename + "'")
               
          
               
 #************************************************************************************************         
               
     def button_generate_atomic_refinment(self):
          species_filename= self.ui.lineEdit_2.text()
          try:
               f = open(species_filename, "r")
               atomic_refinment_filename= self.ui.lineEdit_3.text()
               f = open(atomic_refinment_filename, "w")
               write_atomic_refinement(species_filename,atomic_refinment_filename)
               
          except IOError as e:
               root = tk.Tk()
               root.withdraw()
               messagebox.showerror(title="Error",message=e.strerror + ": '" + e.filename + "'")
          

     def button_edit_atomic_refinment(self):
          atomic_refinment_filename= self.ui.lineEdit_3.text()
          try:
               f = open(atomic_refinment_filename, "r")
               if os.name == "darwin":#Mac
                    sp.Popen(["open", atomic_refinment_filename]) 
               elif  os.name=='posix': #linux
                    sp.Popen(["gedit", atomic_refinment_filename])
               elif  os.name=="nt":     #win
                    sp.Popen(["write",  atomic_refinment_filename])
          except IOError as e:
               root = tk.Tk()
               root.withdraw()
               messagebox.showerror(title="Error",message=e.strerror + ": '" + e.filename + "'")
          
               
          
         
          
     def button_view_atomic_refinment(self):
          atomic_refinment_filename= self.ui.lineEdit_3.text()
          try:
               f = open(atomic_refinment_filename, "r")
               if os.name == "darwin":#Mac
                    sp.Popen(["open", atomic_refinment_filename]) 
               elif  os.name=='posix': #linux
                    sp.Popen(["firefox", atomic_refinment_filename])
               elif  os.name=="nt":     #win
                    sp.Popen(["explorer",  atomic_refinment_filename])
          except IOError as e:
               root = tk.Tk()
               root.withdraw()
               messagebox.showerror(title="Error",message=e.strerror + ": '" + e.filename + "'")
          
          
 #**********************************************************************************************
               

     def button_generate_complex_refinment(self):
          species_filename= self.ui.lineEdit_2.text()
          try:
               atomic_refinment_filename= self.ui.lineEdit_3.text()
               dict_complex_refinement_generated = generate_complex_refinement(species_filename,atomic_refinment_filename)
               complex_refinment_filename= self.ui.lineEdit_4.text()
               write_complex_refinement(dict_complex_refinement_generated,complex_refinment_filename)
               
          except IOError as e:
               root = tk.Tk()
               root.withdraw()
               messagebox.showerror(title="Error",message=e.strerror + ": '" + e.filename + "'")
          

     def button_edit_complex_refinment(self):
          complex_refinment_filename= self.ui.lineEdit_4.text()
          try:
               f = open(complex_refinment_filename, "r")
               if os.name == "darwin":#Mac
                    sp.Popen(["open", complex_refinment_filename]) 
               elif  os.name=='posix': #linux
                    sp.Popen(["gedit", complex_refinment_filename])
               elif  os.name=="nt":     #win
                    sp.Popen(["write",  complex_refinment_filename])
                 
          except IOError as e:
               root = tk.Tk()
               root.withdraw()
               messagebox.showerror(title="Error",message=e.strerror + ": '" + e.filename + "'")
          
          
          
     def button_view_complex_refinment(self):
          complex_refinment_filename= self.ui.lineEdit_4.text()
          try:
               f = open(complex_refinment_filename, "r")
               if os.name == "darwin":#Mac
                    sp.Popen(["open", complex_refinment_filename]) 
               elif  os.name=='posix': #linux
                    sp.Popen(["firefox", complex_refinment_filename])
               elif  os.name=="nt":     #win
                    sp.Popen(["explorer",  complex_refinment_filename])
                
          except IOError as e:
               root = tk.Tk()
               root.withdraw()
               messagebox.showerror(title="Error",message=e.strerror + ": '" + e.filename + "'")
          
#*******************************************************************************************************************************         

     def button_generate_refined_model(self):
          try:
               orginal_model_filename = self.ui.lineEdit_1.text()
               species_filename= self.ui.lineEdit_2.text()
               dict_species_with_atomic=read_species(species_filename)
               atomic_refinment_filename= self.ui.lineEdit_3.text()
               dict_atomic_refinement = read_atomic_refinement(atomic_refinment_filename)
               complex_refinment_filename= self.ui.lineEdit_4.text()
               dict_complex_refinement_read = read_complex_refinement(complex_refinment_filename)
               reactions = read_reactions(orginal_model_filename)
               reaction_dic = generate_reactions(reactions, dict_complex_refinement_read)
               refined_model_filename = self.ui.lineEdit_5.text()
               write_reaction(dict_species_with_atomic,dict_atomic_refinement,dict_complex_refinement_read,reaction_dic,refined_model_filename)

          except IOError as e:
               root = tk.Tk()
               root.withdraw()
               messagebox.showerror(title="Error",message=e.strerror + ": '" + e.filename + "'")
         
          
     def button_display_refined_model(self):
          refined_model_filename = self.ui.lineEdit_5.text()
          
          try:
               f = open(refined_model_filename, "r")
               self.ui.textEdit_refined_model.clear()
               b = print_chemical_reaction(refined_model_filename)
               for i in range (0,len(b)):
                    self.ui.textEdit_refined_model.append(b[i])
               
          except IOError as e:
               root = tk.Tk()
               root.withdraw()
               messagebox.showerror(title="Error",message=e.strerror + ": '" + e.filename + "'")
              
          
     def button_view_refined_model(self):
          refined_model_filename= self.ui.lineEdit_5.text()
          try:
               f = open(refined_model_filename, "r")
               if os.name == "darwin":#Mac
                    sp.Popen(["open",refined_model_filename ]) 
               elif  os.name=='posix': #linux
                    sp.Popen(["firefox", refined_model_filename])
               elif  os.name=="nt":     #win
                    sp.Popen(["explorer",  refined_model_filename])
                   
          except IOError as e:
               root = tk.Tk()
               root.withdraw()
               messagebox.showerror(title="Error",message=e.strerror + ": '" + e.filename + "'")
          
                         
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    
    project= main()
    project.show()
    
    
    sys.exit(app.exec_())       
