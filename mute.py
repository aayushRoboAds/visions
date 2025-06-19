from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL, GUID
from comtypes.client import CreateObject
from pycaw.pycaw import IAudioEndpointVolume
from pycaw.api.mmdeviceapi import IMMDeviceEnumerator

def mute_microphone(mute: bool):

    # CLSID for MMDeviceEnumerator: {BCDE0395-E52F-467C-8E3D-C4579291692E}
    CLSID_MMDeviceEnumerator = GUID('{BCDE0395-E52F-467C-8E3D-C4579291692E}')

    # Create the device enumerator COM object
    device_enumerator = CreateObject(CLSID_MMDeviceEnumerator, interface=IMMDeviceEnumerator)

    # Constants
    eCapture = 1  # Audio capture devices (microphone)
    eConsole = 0  # Role (console)

    # Get the default audio capture device (microphone)
    mic_device = device_enumerator.GetDefaultAudioEndpoint(eCapture, eConsole)

    # Activate volume control interface
    volume_interface = mic_device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(volume_interface, POINTER(IAudioEndpointVolume))

    if mute:
        # Mute microphone
        volume.SetMute(1, None)
        print("Microphone muted.")
    else:
        # Unmute microphone
        volume.SetMute(0, None)
        print("Microphone unmuted.")
