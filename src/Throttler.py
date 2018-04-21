#burp
from burp import IBurpExtender, IHttpListener
from burp import ITab

#java
import java.awt as awt
from java.awt import Panel
from java.awt.event import ActionEvent
from java.awt.event import ActionListener
from java.awt import Color, Font
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

        #self.stdout = PrintWriter(self.callbacks.getStdout(), True)
        #GUI configuration
        self._myPanel = swing.JPanel()
        self._myPanel.setLayout(None)
        self._myPanel.setPreferredSize(awt.Dimension(1200, 1200))

        self._label1 = swing.JLabel("* This extension adds more options to 'Intruder(options)'")
        self._label1.setBounds(15, 5, 500, 100)
        self._myPanel.add(self._label1)

        self._label2 = swing.JLabel("* These settings control the engine used for making HTTP requests in the Intruder attack.")
        self._label2.setBounds(15, 20, 500, 100)
        self._myPanel.add(self._label2)

        self._label3 = swing.JLabel("pause Intruder for specific amount of time for each group attacks:         i.e: pause 30 seconds every 3 requests!")
        self._label3.setBounds(246, 110, 1000, 40)
        self._myPanel.add(self._label3)

        self._label4 = swing.JLabel("Constant Throttling: ")
        self._label4.setBounds(100, 110, 200, 40)
        self._label4.setForeground(Color.RED)
        self._label4.setFont(Font("System", Font.BOLD, 15))
        self._myPanel.add(self._label4)

        self._setButton = swing.JButton("Set", actionPerformed=self.setOptions) #name, action
        self._setButton.setBounds(100, 150, 80, 25) # pos: x ---, pos:y |, width: x, height: y
        self._myPanel.add(self._setButton)

        self._timeLabel = swing.JLabel("Seconds:")
        self._timeLabel.setBounds(210, 150, 80, 25)
        self._myPanel.add(self._timeLabel)

        self._timeTextfield = swing.JTextField()
        self._timeTextfield.setBounds(290, 150, 80, 25)
        self._myPanel.add(self._timeTextfield)

        self._perLabel = swing.JLabel("# of attacks")
        self._perLabel.setBounds(392, 150, 80, 25) # For:
        self._myPanel.add(self._perLabel)

        self._perTextfield  = swing.JTextField()
        self._perTextfield.setBounds(495, 150, 80, 25) #
        self._myPanel.add(self._perTextfield)

        self._stopButton    = swing.JButton("Stop", actionPerformed=self.stopOptions) #name, action
        self._stopButton.setBounds(100, 180, 80, 25)
        self._myPanel.add(self._stopButton)

        self._noticeLabel = swing.JLabel("Notice: this settings will be applied to all Intruders. Even if the attack was cancelled, these settings will continue to have effects unless you press Stop button.")
        self._noticeLabel.setBounds(100, 300, 1500, 100)
        self._myPanel.add(self._noticeLabel)

        self._messageLabel = swing.JLabel() # label message
        self._messageLabel.setBounds(400, 175, 150, 100)
        self._myPanel.add(self._messageLabel)

        self._noticeLabel2 = JLabel("Press Stop button to remove the effects or to set new throttling setting.")
        self._noticeLabel2.setBounds(100, 315, 1500, 100)
        self._myPanel.add(self._noticeLabel2)

        #adding new tab to burp
        callbacks.customizeUiComponent(self._myPanel)
        callbacks.addSuiteTab(self)

    def getTabCaption(self):
        '''Name of our tab'''
        return "Throttler"

    def getUiComponent(self):
        '''return our panel and button we setup'''
        return self._myPanel

    def setOptions(self, button):
        self.per = int(self._perTextfield.getText())
        self.waitTime = int(self._timeTextfield.getText())
        self.stopOption = False
        self._messageLabel.setText("Applied")
        return self.per, self.waitTime, self.stopOption

    def stopOptions(self, button):
        self.per = 1
        self.waitTime = 0
        self.stopOption = True
        self._messageLabel.setText("Effects removed")
        return self.per, self.waitTime, self.stopOption

    def processHttpMessage(self, toolFlag, messageIsRequest, message):
        if self.stopOption == False:
            if messageIsRequest and toolFlag == self.callbacks.TOOL_INTRUDER:
                with self.lock:     
                    if self.count == self.per: # number of attacks per seconds
                        self.count = 0
                        time.sleep(self.waitTime) #self._textfieldTime.getText())
                    self.count += 1
        else:
            if self.lock.locked == True:  # try to figure if the thread is locked or not if it is lock, then unlock it
                try:
                    self.lock.release()
                except Exception, e:
                    print "error in releasing"
            
#get text from textfield
#self.field.getText()
#.setForeground(Color.GREEN)
