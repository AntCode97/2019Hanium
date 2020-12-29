import numpy as np
import random
from keras.layers import Dense
from keras.models import Sequential
from keras.models import load_model
from keras.utils import to_categorical

import Leap
import Sample_module
import libardrone
import sys
import thread
import time

model = load_model('model.h5')


def main():
   listenerA = Sample_module.SampleListener()
   listenerB = Sample_module.SampleListener()
   controller = Leap.Controller()

   drone = libardrone.ARDrone()

   listenerA.on_init(controller)
   listenerA.on_connect(controller)
   while True:
      try:
         listenerA.on_frame(controller)
         palmA = listenerA.plst
         boneA = listenerA.boneZ
         yawA = listenerA.yaw
         handsA = listenerA.hands
         if handsA >= 1:
            if len(palmA) > 0:
               if abs(palmA[2]-boneA)>=40:
                  print "Bba"
                  drone.takeoff()
                  while True:
                     listenerB.on_frame(controller)
                     palmB = listenerB.plst
                     boneB = listenerB.boneZ
                     yawB = listenerB.yaw
                     handsB = listenerB.hands
                     if handsB >= 1:

                        x = palmA[0] - palmB[0]
                        y = palmA[1] - palmB[1]
                        z = palmA[2] - palmB[2]

                        if x > 80:
                           xdir = -1
                        elif x < -80:
                           xdir = 1
                        else:
                           xdir = 0

                        if y > 80:
                           ydir = -1
                        elif y < -80:
                           ydir = 1
                        else:
                           ydir = 0

                        if z > 80:
                           zdir = 1
                        elif z < -80:
                           zdir = -1
                        else:
                           zdir = 0

                        direction = [xdir, ydir, zdir]

                        if direction == [0, 0, 0]:
                           print "Stop"
                           drone.hover()
                           if (yawA - yawB) > 35:
                              print "turn left"
                              drone.turn_left()
                           elif (yawA - yawB) < -35:
                              print "turn right"
                              drone.turn_right()
                           if abs(palmB[2] - boneB) < 40:
                              print "Muk"
                              break

                     print palmB

                     palmB2 = np.array([palmB])
                     print palmB2

                     palmB3 = np.array([0, 0, 0])
                     palmB3 = np.array(palmB2[0:1, 0:3])
                     print palmB3
                     try :
                        y_pred = model.predict(palmB3)
                        print y_pred
                        print np.shape(y_pred)
                        max1 = 0
                        i = 1
                        for i in range(1, 27):
                           if (max1 <= y_pred[0, i]):
                              max1 = y_pred[0, i]
                              max_n = i

                     except ValueError :
                        print "error.."
                        y_pred = 0
                        print y_pred
                        print np.shape(y_pred)
                        max_n = 13





                     print max_n
                     if max_n == 0:
                        print "Down_backward_left"
                        drone.move_down_backward_left()
                     elif max_n == 1:
                        print "Down_backward"
                        drone.move_down_backward()
                     elif max_n == 2:
                        print "Down_backward_right"
                        drone.move_down_backward_right()
                     elif max_n == 3:
                        print "Down_left"
                        drone.move_down_left()
                     elif max_n == 4:
                        print "Down"
                        drone.move_down()
                     elif max_n == 5:
                        print "Down_right"
                        drone.move_down_right()
                     elif max_n == 6:
                        print "Down_forward_left"
                        drone.move_forward_left()
                     elif max_n == 7:
                        print "Down_forward"
                        drone.move_down_forward()
                     elif max_n == 8:
                        print "Down_forward_right"
                        drone.move_forward_right()
                     elif max_n == 9:
                        print "Backward_left"
                        drone.move_backward()
                     elif max_n == 10:
                        print "Backward"
                        drone.move_backward()
                     elif max_n == 11:
                        print "Backward_right"
                        drone.move_backward_right()
                     elif max_n == 12:
                        print "Left"
                        drone.move_left()
                     elif max_n == 13:
                        print "Center"
                     elif max_n == 14:
                        print "Right"
                        drone.move_right()
                     elif max_n == 15:
                        print "Forward_left"
                        drone.move_forward_left()
                     elif max_n == 16:
                        print "Forward"
                        drone.move_forward()
                     elif max_n == 17:
                        print "Forward_right"
                        drone.move_forward_right()
                     elif max_n == 18:
                        print "Up_backward_left"
                        drone.move_up_backward_left()
                     elif max_n == 19:
                        print "Up_backward"
                        drone.move_up_backward()
                     elif max_n == 20:
                        print "Up_backward_right"
                        drone.move_backward_right()
                     elif max_n == 21:
                        print "Up_left"
                        drone.move_up_left()
                     elif max_n == 22:
                        print "Up"
                        drone.move_up()
                     elif max_n == 23:
                        print "Up_right"
                        drone.move_up_right()
                     elif max_n == 24:
                        print "Up_forward_left"
                        drone.move_up_forward_left()
                     elif max_n == 25:
                        print "Up_forward"
                        drone.move_up_forward()
                     elif max_n == 26:
                        print "Up_forward_right"
                        drone.move_up_forward_right()
                     else:
                        print "stop"

                     try:
                        if abs(palmB[2] - boneB) < 40:
                           print "Muk"
                           break
                        del palmB[:]
                     except IndexError :
                        print "indexerror"

                     palmB3 = np.array([0, 0, 0])

                     print "speed : %f" % (drone.speed)
                  else:
                     print "No Hand Recognition"
            elif abs(palmA[2]-boneA) < 40:
               print "Muk"
               drone.land()
               print "Land"
               del palmA[:]

         else:
            print "No Hand Recognition"
            drone.land()
      except KeyboardInterrupt:
         break



main()
