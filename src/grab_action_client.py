#! /usr/bin/env python

from __future__ import print_function
from std_msgs.msg import String
import rospy
 


# Brings in the SimpleActionClient
import actionlib

import actionlib_grab.msg



def grab_client():

	client = actionlib.SimpleActionClient('Grab', actionlib_grab.msg.GrabAction)


	client.wait_for_server()

	retStr = String()
	retStr.data = "grab"	
	#options: "grab" or "release"	

	goal = actionlib_grab.msg.GrabGoal(action = retStr)

	client.send_goal(goal)

	client.wait_for_result()

	return client.get_result()


if __name__ == '__main__':
	try:
		#initializes a node so the client can publish and subscribe using ROS
		rospy.init_node('grab_client_py')
		result = grab_client()
		print("Result:", result.outcome)
	except rospy.ROSInterruptException:
        	print("program interrupted before completion", file=sys.stderr)

