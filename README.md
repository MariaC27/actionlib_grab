# actionlib_grab
A ROS actionlib server and client that allows robot to grabs and release an object based ib a strubg request. This incorporates
both the movement of the robot to a certain pose and the use of gripper commands. 

To grab, the robot first moves to the position of the object, which can later be customized using vision processing / target
recognition. The gripper closes, grabbing the object. To release, the robot moves to a different position, which can also
be customized, then opens the gripper, releasing the object. 

Takes a string request of either "grab" or "release", and returns a boolean response of True if the robot grabbed the object or 
False if the robot released the object. 

For use with the 2 armed robot in building 574 of Tufts. 
