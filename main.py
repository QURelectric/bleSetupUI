from bluez_peripheral.util import *
from bluez_peripheral.advert import Advertisement
from bluez_peripheral.agent import NoIoAgent
import asyncio


from bluez_peripheral.gatt.service import Service
from bluez_peripheral.gatt.characteristic import characteristic, CharacteristicFlags as CharFlags

import struct


#GLOBALS**************************
usernames = [["lbalog", "password"], ["admin", "admin"]]
user = ""
loggedIn = False


#******************************



class HeartRateService(Service):
    def __init__(self):
        # Base 16 service UUID, This should be a primary service.
        super().__init__("180D", True)

    @characteristic("2A37", CharFlags.NOTIFY)
    def heart_rate_measurement(self, options):
        # This function is called when the characteristic is read.
        # Since this characteristic is notify only this function is a placeholder.
        # You don't need this function Python 3.9+ (See PEP 614).
        # You can generally ignore the options argument 
        # (see Advanced Characteristics and Descriptors Documentation).
        pass

    def update_heart_rate(self, new_rate):
        # Call this when you get a new heartrate reading.
        # Note that notification is asynchronous (you must await something at some point after calling this).
        flags = 0

        # Bluetooth data is little endian.
        rate = struct.pack("<BB", flags, new_rate)
        self.heart_rate_measurement.changed(rate)

class AuthService(Service):
    def __init__(self):
        # Base 16 service UUID, This should be a primary service.
        super().__init__("181D", True)

    @characteristic("A002", CharFlags.ENCRYPT_AUTHENTICATED_READ)
    def uname_read(self, options):
        # This function is called when the characteristic is read.
        # Since this characteristic is notify only this function is a placeholder.
        # You don't need this function Python 3.9+ (See PEP 614).
        # You can generally ignore the options argument 
        # (see Advanced Characteristics and Descriptors Documentation).
        pass

    def uname_update(self, new_uname):
        # Call this when you get a new heartrate reading.
        # Note that notification is asynchronous (you must await something at some point after calling this).
        flags = 0

        # Bluetooth data is little endian.
        uname = struct.pack("<BB", flags, new_uname)
        user = new_uname
        self.uname_read.changed(uname)  

    @characteristic("A003", CharFlags.ENCRYPT_AUTHENTICATED_READ)
    def upass_read(self, options):
        # This function is called when the characteristic is read.
        # Since this characteristic is notify only this function is a placeholder.
        # You don't need this function Python 3.9+ (See PEP 614).
        # You can generally ignore the options argument 
        # (see Advanced Characteristics and Descriptors Documentation).
        pass

    def upass_update(self, new_upass):
        # Call this when you get a new heartrate reading.
        # Note that notification is asynchronous (you must await something at some point after calling this).
        flags = 0

        # Bluetooth data is little endian.
        upass = struct.pack("<BB", flags, new_upass)
        for i in usernames:
            if(usernames[i][0] == user):
                if(usernames[i][1] == new_upass):
                    loggedIn =True
        self.upass_read.changed(upass)  



async def main():
    # Alternativly you can request this bus directly from dbus_next.
    bus1 = await get_message_bus()
    bus2 = await get_message_bus()

    hrservice = HeartRateService()
    authservice = AuthService()
    await hrservice.register(bus1)
    await authservice.register(bus2)

    # An agent is required to handle pairing 
    agent1 = NoIoAgent()
    agent2 = NoIoAgent()
    # This script needs superuser for this to work.
    await agent1.register(bus1)
    await agent2.register(bus2)

    adapter1 = await Adapter.get_first(bus1)
    adapter2 = await Adapter.get_first(bus2)

    # Start an advert that will last for 60 seconds.
    advert1 = Advertisement("Jeep2024", ["180D"], 0x0340, 60)
    await advert1.register(bus1, adapter1)

    advert2 = Advertisement("Jeep2024Auth", ["181D"], 0x0340, 60)
    await advert2.register(bus2, adapter2)

    print("running")

    while True:
        
        
        # Handle dbus requests.
        await asyncio.sleep(5)

    await bus.wait_for_disconnect()



if __name__ == "__main__":
    asyncio.run(main())

