# Adam Kwok
# Last updated: 2/27/2019

# This program allows the user to control period, enable, and duty cycle from the processor
# Additionally, this interface informs the user that the motors are enabled when the pwm signal is sent to pins

import sys
import time
import mmap
import struct
from PyQt4 import QtCore, QtGui

class TestWidget(QtGui.QWidget):
  def __init__(self, parent):
    super(QtGui.QWidget, self).__init__()
    self.layout = QtGui.QVBoxLayout()
    
    #Initialize tab screen
    self.tabs = QtGui.QTabWidget()
    self.pwm_setup_tab = QtGui.QWidget()
    self.tabs.resize(300,200)
    
    #Add tabs
    self.tabs.addTab(self.pwm_setup_tab, "Test")
    
    # Create PWM Setup Tab tab
    self.pwm_setup_tab.layout = QtGui.QVBoxLayout();
    self.pwm_set_pushbutton = QtGui.QPushButton("Test")
    self.pwm_setup_tab.layout.addWidget(self.pwm_set_pushbutton)
    self.pwm_setup_tab.setLayout(self.pwm_setup_tab.layout)
    
    # Add widgets to overall layout
    self.layout.addWidget(self.tabs)
    self.setLayout(self.layout)

class MyPWMWidget(QtGui.QWidget):
  def __init__(self, parent):
    super(QtGui.QWidget, self).__init__()
    self.layout = QtGui.QVBoxLayout()
    
    #Initialize tab screen
    self.tabs = QtGui.QTabWidget()
    self.pwm_setup_tab = QtGui.QWidget()
    self.pwm_graph_tab = QtGui.QWidget()
    self.tabs.resize(300,200)
    
    #Add tabs
    self.tabs.addTab(self.pwm_setup_tab, "PWM Setup")
    self.tabs.addTab(self.pwm_graph_tab, "PWM Graphs")
    
    # Create PWM Setup Tab tab
    
    self.current_period = None
    self.current_duty = None
    self.current_freq = None
    self.enable = None
    
    self.pwm_setup_tab.layout = QtGui.QGridLayout()
    self.period_comboBox = QtGui.QComboBox(self)
    self.periodLabel = QtGui.QLabel()
    self.dutyLabel = QtGui.QLabel()
    self.freqLabel = QtGui.QLabel()
    self.pwm_enable = QtGui.QLabel()
    self.period_le = QtGui.QLineEdit()
    self.duty_le = QtGui.QLineEdit()
    
    names = [ ' ', 'Current Period:', 'current_period_label', ' ',
              ' ', 'Current Duty Cycle:', 'current_duty_label', ' ',
              ' ', 'Current Frequency:', 'current_frequency_label', ' ',
              'Period', 'Period_label', 'Period_textbox', 'Period_options_dropdown',
              'Duty Cycle', 'Duty_label', 'Duty_textbox', '%',
              'PWM_enabled',' ', 'enable', 'Update PWM']
    positions = [(i, j) for i in range(6) for j in range(4)]
    for position, name in zip(positions, names):

      if name == ' ':
        continue
      if name == 'Current Period:' or name == 'Current Duty Cycle:' or name == 'Current Frequency:' or name == '%' or name == 'Period' or name == 'Duty Cycle':
        label = QtGui.QLabel()
        label.setText(name)
        self.pwm_setup_tab.layout.addWidget(label, *position)
      if name == 'current_period_label':
        if self.current_period is None:
          self.periodLabel.setText('Period not set')
        else :
          self.periodLabel.setText(self.period_le.text() + ' ' + str(self.period_comboBox.currentText()))
        self.pwm_setup_tab.layout.addWidget(self.periodLabel, *position)
      if name == 'current_duty_label':
        if self.current_duty is None:
          self.dutyLabel.setText('Duty cycle not set')
        else:
          self.dutyLabel.setText(self.duty_le.text() + ' %')
        self.pwm_setup_tab.layout.addWidget(self.dutyLabel, *position)
      if name == 'current_frequency_label':
        if self.current_freq is None:
          self.freqLabel.setText('Duty cycle and period not set')
        else:
          self.freqLabel.setText(str(self.current_freq) + ' Hz')
        self.pwm_setup_tab.layout.addWidget(self.freqLabel, *position)
      if name == 'Period_label':
        self.pwm_setup_tab.layout.addWidget(self.period_le, *position)
      if name == 'Duty_label':
        self.pwm_setup_tab.layout.addWidget(self.duty_le, *position)
      if name == 'Period_options_dropdown':
        self.period_comboBox.addItem("ms")
        self.period_comboBox.addItem("us")
        self.period_comboBox.addItem("ns")
        self.pwm_setup_tab.layout.addWidget(self.period_comboBox, *position)
      if name == 'PWM_enabled':
        if self.enable is None:
          self.pwm_enable.setText('Disabled')
        else:
          self.pwm_enable.setText('Enabled')
      if name == 'enable':
        self.enable_pb = QtGui.QPushButton("Enable")
        self.enable_pb.setCheckable(True)
        self.enable_pb.toggle()
        self.enable_pb.clicked.connect(self.pwm_enable_func)
        self.pwm_setup_tab.layout.addWidget(self.enable_pb, *position)
      if name == 'Update PWM':
        self.update_pb = QtGui.QPushButton("Update PWM")
        self.update_pb.setCheckable(True)
        self.update_pb.toggle()
        self.update_pb.clicked.connect(self.update_btnstate)
        self.pwm_setup_tab.layout.addWidget(self.update_pb, *position)

    self.pwm_setup_tab.setLayout(self.pwm_setup_tab.layout)
    
    # Create PWM Graphs.Tab
    self.pwm_graph_tab.layout = QtGui.QVBoxLayout();
    #self.pwm_graph_tab_graph = Figure()
    #self.pwm_graph_tab.layout.addWidget(self.pwm_graph_tab_graph)
    self.pwm_graph_tab.setLayout(self.pwm_graph_tab.layout)
    
    # Add widgets to overall layout
    self.layout.addWidget(self.tabs)
    self.setLayout(self.layout)
    
  def pwm_enable_func(self):
    if self.enable_pb.isChecked():
      if (self.current_freq is None and self.current_duty is None):
        pass
      else:
        output_duty = float(self.current_period)*(float(self.current_duty)/100)
        self.enable = 1
 
        # open dev mem and see to base address
        f = open("/dev/mem", "r+b")

        mem = mmap.mmap(f.fileno(), 32, offset=0x43c00000)
    
        toMem = 1
        reg   = 8   # 0 is reg 1, 4 is reg 2, 8 is reg 3
        mem.seek(reg)  
        mem.write(struct.pack('l', toMem))
      
        toMem = output_duty
        reg   = 4   # 0 is reg 1, 4 is reg 2, 8 is reg 3
        mem.seek(reg)  
        mem.write(struct.pack('l', toMem))
        
        toMem = self.current_period
        reg   = 0   # 0 is reg 1, 4 is reg 2, 8 is reg 3
        mem.seek(reg)
        mem.write(struct.pack('l', toMem))
      
        time.sleep(.5) 
        mem.seek(reg)  
        fromMem = struct.unpack('l', mem.read(4))[0]
        print (reg, " = ", fromMem)
        mem.close()
        f.close()
        
    else:
      self.enable = None
      #Set duty cycle to 0 here
      # open dev mem and see to base address
      f = open("/dev/mem", "r+b")
      mem = mmap.mmap(f.fileno(), 32, offset=0x43c00000)
      
      toMem = 0
      reg   = 0   # 0 is reg 1, 4 is reg 2, 8 is reg 3
      mem.seek(reg)  
      mem.write(struct.pack('l', toMem))
      
      toMem = 0
      reg   = 4   # 0 is reg 1, 4 is reg 2, 8 is reg 3
      mem.seek(reg)  
      mem.write(struct.pack('l', toMem))
      
      toMem = 0
      reg   = 8   # 0 is reg 1, 4 is reg 2, 8 is reg 3
      mem.seek(reg)  
      mem.write(struct.pack('l', toMem))
      
      time.sleep(.5) 
      mem.seek(reg)  
      fromMem = struct.unpack('l', mem.read(4))[0]
      print (reg, " = ", fromMem)
      mem.close()
      f.close()
  
  def update_btnstate(self):
    if self.update_pb.isChecked():
      #Add censoring if duty cycle is below 0 or above 100 or period is less than 0
      
      self.D_isValid = 0
      self.P_isValid = 0
      
      try:
        if float(self.duty_le.text()) < 0 or float(self.duty_le.text()) > 100:
          QtGui.QMessageBox.critical(self, 'Input Error', 'The Duty Cycle must be a number between 0% and 100%')
        else:
          self.D_isValid = 1
          try:
            if float(self.period_le.text()) < 0:
              QtGui.QMessageBox.critical(self, 'Input Error', 'The Period must be 0 or greater')
            else:
              self.P_isValid = 1
          except ValueError:
            QtGui.QMessageBox.critical(self, 'Input Error', 'You must input a positive numerical value for both Period and Duty Cycle')
      except ValueError:
        QtGui.QMessageBox.critical(self, 'Input Error', 'You must input a positive numerical value for both Period and Duty Cycle')
      
      #pre-processes duty cycle and period inputs
      if self.D_isValid and self.P_isValid:
        self.dutyLabel.setText(self.duty_le.text() + ' %')
        self.periodLabel.setText(self.period_le.text() + ' ' + str(self.period_comboBox.currentText()))
        self.current_duty = float(self.duty_le.text())
        self.current_period = float(self.period_le.text())
        
        #Scales period based on combobox values
        if str(self.period_comboBox.currentText()) == 'ms':
          self.current_period = self.current_period * 1000000
        elif str(self.period_comboBox.currentText()) == 'us':
          self.current_period = self.current_period * 1000
        elif str(self.period_comboBox.currentText()) == 'ns':
          self.current_period = self.current_period
        
        #Calculates frequency based on period
        if float(self.current_period) == 0:
          self.current_freq = 0
        else:
          self.current_freq = str(float(1000000000 / float(self.current_period)))
        
        #Sets duty cycle and period labels to current values
        self.periodLabel.setText(self.period_le.text() + ' ' + str(self.period_comboBox.currentText()))
        self.dutyLabel.setText(self.duty_le.text() + ' %')
        
        #sets frequency label and removes excess zeros in exchange for modified label if possible
        if int(float(self.current_freq)) % 1000000 == 0:
          self.freqLabel.setText(str(float(self.current_freq)/1000000) + ' MHz')
        elif int(float(self.current_freq)) % 1000 == 0:
          self.freqLabel.setText(str(float(self.current_freq)/1000) + ' kHz')
        else:
          self.freqLabel.setText(str(self.current_freq) + ' Hz')

class MainWindow(QtGui.QMainWindow):
  def __init__(self):
    super(QtGui.QMainWindow,self).__init__()
    
    # Name widgets
    self.PWM_widget = MyPWMWidget(self)
    self.Test_Widget = TestWidget(self)
    
    # Layout
    widget = QtGui.QWidget()
    vbox = QtGui.QHBoxLayout(widget)
    vbox.addWidget(self.PWM_widget)
    vbox.addWidget(self.Test_Widget)
    
    self.title = 'Gui Containing Tab with Labels and Text Boxes Prototype'
    self.showMaximized()
    self.setWindowTitle(self.title)
    self.layout().addWidget(widget)
    self.show()
    
def main():
  app = QtGui.QApplication(sys.argv)
  mainWindow = MainWindow()
  sys.exit(app.exec_())
  
if __name__ == '__main__':
  main()