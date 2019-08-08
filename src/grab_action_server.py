#! /usr/bin/env python

from std_msgs.msg import String
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper

import rospy

import urx

import sys

import actionlib

import actionlib_grab.msg



class GrabAction(object):
	_result = actionlib_grab.msg.GrabResult()



	def __init__(self, name):
		self._action_name = name
		self._as = actionlib.SimpleActionServer(self._action_name, 
		actionlib_grab.msg.GrabAction, execute_cb=self.execute_cb,
		auto_start = False)

		self._as.start()
		

	def execute_cb(self, goal):
		r = rospy.Rate(1)
		success = True

		rospy.loginfo('%s: Executing, returning value of %s' %(self._action_name,
		goal.action))

		if self._as.is_preempt_requested():
                	rospy.loginfo('%s: Preempted' % self._action_name)
                	self._as.set_preempted()
                	success = False
                		


		if success:

			#make sure to comment out all robot commands when robot 
			#is not present in order to avoid timeout errors 

			rob = urx.Robot("172.22.22.2")
			robotiqgrip = Robotiq_Two_Finger_Gripper(rob, 1.25)



			#commands to move the robot to position 
			
			a = 0.05
			v = 0.1
			

			pose = rob.getl()
			rospy.loginfo("Current pose: %s"% (rob.getl()))
			rob.movep(pose, acc=a, vel=v, wait=True)


			rospy.loginfo('Print request of %s'%(goal.action))

			#need to do this so data type matches the request
			#std_msgs/String is not the same as a regular string!
			compStr1 = String()
			compStr1.data = "grab"

			compStr2 = String()
			compStr2.data = "release"




			#conditional statements 

			if(goal.action == compStr1):
				check = True  #returns true if grabbed the object


				#commands: move to a certain point and then close gripper, grabbing object  

				rob.movel((pose[0], pose[1], pose[2] + 0.1, pose[3], pose[4], pose[5]), a, v, relative=True)
				#this move command can later be customized based on CAMERA/VISION PROCESSING data  

				robotiqgrip.close_gripper()

				rospy.loginfo("grab")



			if(goal.action == compStr2):
				check = False #returns false if released the object


				#commands: move to a certain point and then open gripper, releasing object

				rob.movel((pose[0], pose[1], pose[2] - 0.1, pose[3], pose[4], pose[5]), a, v, relative=True)
				#move command can later be customized based on CAMERA/VISION PROCESSING data  

				robotiqgrip.open_gripper()

				rospy.loginfo("release")


			rob.close()
			sys.exit()


			self._result.outcome = check
			rospy.loginfo('%s: Succeeded' % self._action_name)
	            	self._as.set_succeeded(self._result)

if __name__ == '__main__':
	rospy.init_node('Grab')
	server = GrabAction(rospy.get_name())

       
	rospy.spin()





