#burp
from burp import IBurpExtender, IHttpListener
from burp import ITab

#java
import java.awt as awt
from java.awt import Panel
from java.awt.event import ActionEvent
from java.awt.event import ActionListener
from javax.swing import JButton;
from javax.swing import JTextPane, JTextField
from javax.swing import JLabel
from javax import swing
from java.io import PrintWriter


#python
import threading, time
from array import array


class BurpExtender(IBurpExtender, ITab, IHttpListener):
    per = 1 
    count = 0
    waitTime = 0
    lock = threading.Lock()
    stopOption = False

    def registerExtenderCallbacks(self, callbacks):

        self.callbacks = callbacks
        callbacks.registerHttpListener(self)
        callbacks.setExtensionName("Throttler")

        self.stdout = PrintWriter(self.callbacks.getStdout(), True)

        #creating GUI components
        self._newpanel = Panel()

        self._setButton = JButton("Set", actionPerformed=self.setOptions) #name, action
        self._timeLabel = JLabel("Seconds:")
        self._timeTextfield = JTextField()
        self._perLabel = JLabel("For:")
        self._perTextfield = JTextField()
        self._stopButton = JButton("Stop", actionPerformed=self.stopOptions) #name, action

        #GUI configuration
        self._setButton.setBounds(100, 100, 80, 25) # pos: x ---, pos:y |, width: x, height: y
        self._timeLabel.setBounds(210, 100, 80, 25)
        self._timeTextfield.setBounds(290, 100, 80, 25) #
        self._perLabel.setBounds(395, 100, 80, 25) # For:
        self._perTextfield.setBounds(450, 100, 80, 25) #                                                      
        self._stopButton.setBounds(100, 130, 80, 25)
        self._newpanel.setLayout(None)

        #main window dimensions
        self._newpanel.setPreferredSize(awt.Dimension(1200, 1200))

        #adding components to window
        self._newpanel.add(self._setButton)
        self._newpanel.add(self._timeLabel)
        self._newpanel.add(self._timeTextfield)
        self._newpanel.add(self._perLabel)
        self._newpanel.add(self._perTextfield)
        self._newpanel.add(self._stopButton)
        
        
        #adding new tab to burp
        callbacks.customizeUiComponent(self._newpanel)
        callbacks.addSuiteTab(self)

    def getTabCaption(self):
        '''Name of our tab'''
        return "Throttler"

    def getUiComponent(self):
        '''return our panel and button we setup'''
        return self._newpanel

    def setOptions(self, button):
        self.stdout.println("set options >")
        self.per = int(self._perTextfield.getText())
        self.waitTime = int(self._timeTextfield.getText())
        self.stopOption = False
        return self.per, self.waitTime, self.stopOption

    def stopOptions(self, button):
        self.per = 1
        self.waitTime = 0
        self.stopOption = True
        return self.per, self.waitTime, self.stopOption

    def processHttpMessage(self, toolFlag, messageIsRequest, message):
        if self.stopOption == False:
            if messageIsRequest and toolFlag == self.callbacks.TOOL_INTRUDER:
                with self.lock:
                    self.count += 1     
                    if self.count == self.per: # number of attacks per seconds
                        self.count = 0
                        time.sleep(self.waitTime) #self._textfieldTime.getText())

        else:
            if self.lock.locked == True:   
                try:
                    self.lock.release()
                    self.stdout.println("released")
                except Exception, e:
                    print "error in releasing"
            
#get text from textfield
#self.field.getText()
#.setForeground(Color.GREEN)