"""
A simple Python script to send messages to a sever over Bluetooth
using PyBluez (with Python 2).
"""

import bluetooth
from struct import*
import wmi
import os
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volume.GetMute()
volume.GetMasterVolumeLevel()
volume.GetVolumeRange()
c = wmi.WMI(namespace='wmi')
methods = c.WmiMonitorBrightnessMethods()[0]
methods.WmiSetBrightness(50, 0)
serverMACAddress = '9C:B6:D0:DF:98:64'
port = 3
print 'Scanning for Devices'
nearby_devices = bluetooth.discover_devices(lookup_names=True)
print("found %d devices" % len(nearby_devices))
namz = ''
decode = (2,1,1,50,50)
for addr, name in nearby_devices:
    print("  %s - %s" % (addr, name))
    if addr == serverMACAddress:
        namz = name
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
print 'Connecting to', namz
s.connect((serverMACAddress, port))
print 'Connected to ', namz
while 1:
    data = s.recv(1024)
    if data:
        demo = len(data)
        if demo == 5:
            decode = unpack('BBBBB',data)
            print decode
            if decode[0] == 2:
                brightness = decode[4]
                num = decode[3]
                print brightness
                vol = -100*0.6+num*0.6
                if num < 1:
                    volume.SetMute(1,None)
                else:
                    volume.SetMute(0,None)
                volume.SetMasterVolumeLevel(vol, None)
                methods.WmiSetBrightness(brightness, 0)

sock.close()
