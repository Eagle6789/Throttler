#burp
from burp import IIntruderAttack, IHttpService
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
import sys


class BurpExtender(IBurpExtender, ITab, IHttpListener):
    per = 1 
    count = 0
    waitTime = 0
    total = 0
    lock_stat = 0
    stat = False

    def registerExtenderCallbacks(self, callbacks):

        self.callbacks = callbacks
        callbacks.registerHttpListener(self)
        callbacks.setExtensionName("Throttler v0.2")

        self.stdout = PrintWriter(self.callbacks.getStdout(), True)

        #GUI configuration
        self._lock = threading.Lock()
        self._myPanel = swing.JPanel()
        self._myPanel.setLayout(None)
        self._myPanel.setPreferredSize(awt.Dimension(1200, 1200))

        self._label1 = swing.JLabel("* This extension adds more options to 'Intruder(options)'")
        self._label1.setBounds(15, 1, 500, 100)
        self._myPanel.add(self._label1)

        self._label2 = swing.JLabel("* These settings control the engine used for making HTTP requests in the Intruder attack.")
        self._label2.setBounds(15, 15, 500, 100)
        self._myPanel.add(self._label2)

        self._label3 = swing.JLabel(" pause Intruder for specific amount of time for each group attacks:         i.e: pause 30 seconds every 3 requests!")
        self._label3.setBounds(246, 80, 1000, 40)
        self._myPanel.add(self._label3)

        self._label4 = swing.JLabel("Constant Throttling: ")
        self._label4.setBounds(100, 80, 200, 40)
        self._label4.setForeground(Color.RED)
        self._label4.setFont(Font("System", Font.BOLD, 15))
        self._myPanel.add(self._label4)

        self._setButton = swing.JButton("Set", actionPerformed=self.setOptions) #name, action
        self._setButton.setBounds(100, 120, 80, 25) # pos: x ---, pos:y |, width: x, height: y
        self._myPanel.add(self._setButton)

        self._timeLabel = swing.JLabel("Seconds:")
        self._timeLabel.setBounds(210, 120, 80, 25)
        self._myPanel.add(self._timeLabel)

        self._timeTextfield = swing.JTextField()
        self._timeTextfield.setBounds(290, 120, 80, 25)
        self._myPanel.add(self._timeTextfield)

        self._perLabel = swing.JLabel("# of attacks:")
        self._perLabel.setBounds(410, 120, 80, 25) # For:
        self._myPanel.add(self._perLabel)

        self._perTextfield  = swing.JTextField()
        self._perTextfield.setBounds(495, 120, 80, 25) #
        self._myPanel.add(self._perTextfield)
        #stop button
        self._stopButton = swing.JButton("Stop", actionPerformed=self.stopOptions) #name, action
        self._stopButton.setBounds(280, 270, 80, 50)
        self._myPanel.add(self._stopButton)

        self._messageLabel = swing.JLabel() # label message
        self._messageLabel.setBounds(400, 270, 150, 50)
        self._myPanel.add(self._messageLabel)

        self._noticeLabel = swing.JLabel("Notice: this settings will be applied to all Intruders. Even if the attack was cancelled, these settings will")
        self._noticeLabel.setBounds(30, 600, 1500, 100)
        self._noticeLabel.setForeground(Color.RED)
        self._noticeLabel.setFont(Font("System", Font.BOLD, 13))
        self._myPanel.add(self._noticeLabel)

        self._noticeLabel2 = JLabel("continue to have effects unless you press Stop button. Press Stop button to remove the effects or to set new throttling setting.")
        self._noticeLabel2.setBounds(30, 615, 1500, 100)
        self._noticeLabel2.setFont(Font("System", Font.BOLD, 13))
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
        try:
            self.per = int(self._perTextfield.getText())
            self.waitTime = int(self._timeTextfield.getText())
            self.stat = True
            self._messageLabel.setText("Settings applied")
            return self.per, self.waitTime, self.stat

        except Exception, e:
            print "No values were supplied!"
            self._messageLabel.setText("Settings can't be applied!")

    def stopOptions(self, button):
        self.per = 0
        self.waitTime = 0
        self.stat = False
        self._messageLabel.setText("Settings reseted")
        self.lock_stat = 1
        if self._lock.locked == True:  # try to figure out if the thread is locked or not if it is lock, then unlock it
            try:
                #self._lock.acquire()
                self._lock.release()
            except Exception, e:
                print "release lock error"
        return self.per, self.waitTime, self.stat

    def resetDefault(self, button):
        self.per = 0
        self.waitTime = 0
        self.stat = False
        self.stdout.println("reset")
        try:
            for i in range(self.total):
                  self._lock.release()
        except Exception, e:
            print e
        
        return self.per, self.waitTime, self.stat

    def processHttpMessage(self, toolFlag, messageIsRequest, message):
        if self.stat == True:
            if messageIsRequest and toolFlag == self.callbacks.TOOL_INTRUDER:
                if self.count == self.per: # number of attacks per seconds
                    if self.lock_stat == 1:
                        try:
                            if self._lock.locked == True:
                                self._lock.release()
                            
                        except Exception, e:
                                print e
                        self.lock_stat = 0
                    self.total += 1
                    with self._lock:
                        time.sleep(self.waitTime)
                    self.count = 0
                self.count += 1
        else:
            if self._lock.locked == True:  # try to figure out if the thread is locked or not if it is lock, then unlock it
                try:
                    #self._lock.acquire()
                    self._lock.release()
                except Exception, e:
                    print "release lock error"
