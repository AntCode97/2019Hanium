################################################################################
# Copyright (C) 2012-2016 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import Leap, sys, thread, time


class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    def __init__(self):
        self.plst=[]
        self.boneZ=0
        self.yaw = 0
        self.hands = 0

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        time.sleep(1.5)
        frame = controller.frame()

        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers))
        self.hands = len(frame.hands)

        # Get hands
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            print "  %s, position: %s" % (
                handType, hand.palm_position)
            spp=''  # palm position string type
            spp=str(hand.palm_position)
            tmp=''
            for i in range(1,len(spp)-1):
                tmp+=spp[i]
            tmpp=tmp.split(', ')
            for j in range(3):
                self.plst.append(float(tmpp[j]))
            # Get Yaw
            direction = hand.direction
            self.yaw = direction.yaw * Leap.RAD_TO_DEG
            print ("  yaw: %f degrees") % (self.yaw)
            # Get middle fingers
            mfinger=hand.fingers[2]

            # Get middle finger distal bone
            mbone = mfinger.bone(3)
            print "  %s finger %s end point : %s" % (
                self.finger_names[mfinger.type],
                self.bone_names[mbone.type],
                mbone.next_joint)
            sdp=''
            sdp=str(mbone.next_joint)
            tmp=''
            for i in range(1,len(sdp)-1):
                tmp+=sdp[i]
            tmpd=tmp.split(', ')
            self.boneZ=float(tmpd[2])
 
        if not frame.hands.is_empty:
            print ""


def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    #time.sleep(10)
    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
