import Leap, sys, thread, time, Sample_module, libardrone

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
                        if len(palmB) > 0:
                           vector = []
                           for i in range(len(palmA)):
                              vector.append(abs(palmB[i]-palmA[i]))

                           index = 3
                           if max(vector) >= 100:
                              index = vector.index(max(vector))

                           if index == 0:
                              if palmB[0] - palmA[0] > 0:
                                 print "right"
                                 drone.move_right()
                              else:
                                 print "left"
                                 drone.move_left()
                           elif index == 1:
                              if palmB[1] - palmA[1] > 0:
                                 print "up"
                                 drone.move_up()
                              else:
                                 print "down"
                                 drone.move_down()
                           elif index == 2:
                              if palmB[2] - palmA[2] > 0:
                                 print "back"
                                 drone.move_backward()
                              else:
                                 print "front"
                                 drone.move_forward()
                           else:
                              print "stop"
                              drone.hover()
                              if (yawA - yawB) > 35:
                                  drone.turn_left()
                                  print "turn left"
                              elif (yawA - yawB) < -35:
                                  drone.turn_right()
                                  print "turn right"

                              if abs(palmB[2] - boneB) < 40:
                                 print "Muk"
                                 drone.land()
                                 break
                           del palmB[:]
                     else:
                        print "No Hand Recognition"
                        drone.land()


               elif abs(palmA[2]-boneA)<40:
                  print "Muk"
                  del palmA[:]
         else:
            print "No Hand Recognition"
            drone.land()

      except KeyboardInterrupt:
         break

   

main()
