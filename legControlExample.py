"""
ECE 4600 - Group Design Project
G08 - ServoSentry
Author - Noah Stieler, 2025

TO RUN THIS FILE:
have the legControl package as a subdirectory in your current working directory.
Run: python -m legControl.legControlExample.py

Some examples of how to use legControl.
"""

from time import time, sleep

from .legControl import LegControl

legControl = LegControl()

def mainTestWalking():
    """
    Tests the walking functionality.
    """
    
    legControl.connect()
    
    legControl.animationStand()
    #Sets the angle of all the legs. To turn, call animationTurnLeft() or animationTurnRight()
    legControl.animationSetAngle(0)

    sleep(5)
    
    #Start the walking animation. The robot now walks
    #until another animation command is called.
    legControl.animationWalk()
    
    while True:
        legControl.update()
        
def mainTestConnection():
    """
    Test on-the-go locomotion system swapping.
    While running this test, the signal wires can be disconnected and
    reconnected without causing any errors.
    """
    
    while True:
        if not legControl.isConnected():
            legControl.connect() #Continuously attempt to establish connection
            legControl.animationWalk()
        
        #This function simply return unless a valid connection is established.
        legControl.update()
        
if __name__ == "__main__":
    """
    Change this to your desired example function
    """
    mainTestConnection()

