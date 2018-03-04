import os
import kivy3
import serial
import bluetooth
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy3 import Mesh, Material
from kivy3 import Scene, Renderer, PerspectiveCamera
from kivy3.extras.geometries import BoxGeometry
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from struct import *
import binascii

global smsbool
global s
global voicebool
global phoneID
global Volume
global Brightness
global hostMACAddress
global clientInfo
global client
global CommsOpen
hostMACAddress = '9C:B6:D0:DF:98:64'
Volume = 50
Brightness = 50
smsbool = True
voicebool = True
CommsOpen = False

Builder.load_file('UIBarebone.kv')
class BTComms:

    def opencomms(self):
        global hostMACAddress
        global client
        global s
        print('Opening Port')
        port = 3
        backlog = 1
        size = 1024
        s = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        s.bind((hostMACAddress, port))
        s.listen(backlog)
        try:
            client, clientInfo = s.accept()
            print("Accepted connection from ", clientInfo)
        except:
            print('Faliure')
    def closecomms(self):
        global s
        global client
        print('Closing Comms')
        client.close()
        s.close()
    def send(self):
        global client
        global s
        global smsbool
        global voicebool
        global phoneID
        global Volume
        global Brightness
        outb= pack('BBBBB',phoneID,smsbool,voicebool,int(Volume),int(Brightness))
        print(outb)
        s.listen(1)
        client.send(outb)


class MenuScreen(Screen):
    #pass
    def test(self):
        print ("Help Me")
    def SetActivePhone(self,ID):
        global phoneID
        phoneID = ID
        print(phoneID)
    def ToggleComms(self):
        global CommsOpen
        comms = BTComms()
        if CommsOpen == False:
            self.ids.Combut.text = 'Opening Comms'
            comms.opencomms()
            self.ids.Combut.text = 'Close Program'
            CommsOpen == True
        elif CommsOpen == True:
            comms.closecomms()
            self.ids.Combut.text = 'Open Comms'
            CommsOpen == False

class SettingsScreen(Screen):
    #pass
    def SetScreenZero(self):
        global Brightness
        self.ids.s2.value = 0
        Brightness = self.ids.s2.value
    def SetVolumeZero(self):
        global Volume
        self.ids.s1.value = 0
        Volume = self.ids.s1.value
    def UpdateVolume(self):
        global Volume
        Volume = self.ids.s1.value
    def UpdateBrightness(self):
        global Brightness
        Brightness = self.ids.s2.value
    def ToggleSMS(self):
        global smsbool
        if smsbool == True:
            self.ids.b1.text = 'Enable SMS'
            smsbool = False
        elif smsbool == False:
            self.ids.b1.text = 'Disable SMS'
            smsbool = True
    def ToggleVoice(self):
        global voicebool
        if voicebool == True:
            self.ids.b2.text = 'Enable Calling'
            voicebool = False
        elif voicebool == False:
            self.ids.b2.text = 'Disable Calling'
            voicebool = True
    def SendToComms(self):
        comms = BTComms()
        comms.send()
class AboutScreen(Screen):
    pass

# Create the screen manager
sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(SettingsScreen(name='settings'))
sm.add_widget(AboutScreen(name='about'))

class UpToBlue(App):

    def build(self):
        return sm


if __name__ == '__main__':
    UpToBlue().run()
