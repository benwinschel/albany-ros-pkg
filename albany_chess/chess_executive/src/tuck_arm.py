#!/usr/bin/env python

""" 
  Copyright (c) 2011 Michael E. Ferguson.  All right reserved.

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software Foundation,
  Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

import roslib; roslib.load_manifest('arbotix_controllers')
import rospy
import actionlib
import sys

from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from control_msgs.msg import *

servos = ['arm_shoulder_pan_joint', 'arm_shoulder_lift_joint', 'arm_elbow_flex_joint', 'arm_wrist_flex_joint', 'arm_wrist_roll_joint']

forward = [-0.0409061543436171, 0.014913702104443736, 1.4817828305200882, 1.6515859816235403, -0.066472500808377785]
to_side = [1.4675082870772636, 0.024501082028728992, 1.4817828305200882, 1.6157930965728755, -0.066472500808377785]
tucked = [1.4675082870772636, -0.48576058283045309, 1.4817828305200882, 1.7180584824319183, -0.066472500808377785]

class tuck_arm:
    
    def __init__(self, client=None):
        if client != None:
            self._client = client
        else:
            self._client = actionlib.SimpleActionClient('follow_joint_trajectory', FollowJointTrajectoryAction)
        self._client.wait_for_server()

    def tuck(self):
        # prepare a joint trajectory
        msg = JointTrajectory()
        msg.joint_names = servos
        msg.points = list()
    
        point = JointTrajectoryPoint()
        point.positions = forward
        point.velocities = [ 0.0 for servo in msg.joint_names ]
        point.time_from_start = rospy.Duration(5.0)
        msg.points.append(point)
        point = JointTrajectoryPoint()
        point.positions = to_side
        point.velocities = [ 0.0 for servo in msg.joint_names ]
        point.time_from_start = rospy.Duration(8.0)
        msg.points.append(point)
        point = JointTrajectoryPoint()
        point.positions = tucked
        point.velocities = [ 0.0 for servo in msg.joint_names ]
        point.time_from_start = rospy.Duration(11.0)
        msg.points.append(point)

        # publish
        msg.header.stamp = rospy.Time.now() + rospy.Duration(0.1)
        #self.pub.publish(msg)

        goal = FollowJointTrajectoryGoal()
        goal.trajectory = msg
        self._client.send_goal(goal)
        
    def untuck(self):
        # prepare a joint trajectory
        msg = JointTrajectory()
        msg.joint_names = servos
        msg.points = list()
        
        point = JointTrajectoryPoint()
        point.positions = to_side
        point.velocities = [ 0.0 for servo in msg.joint_names ]
        point.time_from_start = rospy.Duration(3.0)
        msg.points.append(point)

        # publish
        msg.header.stamp = rospy.Time.now() + rospy.Duration(0.1)
        #self.pub.publish(msg)

        goal = FollowJointTrajectoryGoal()
        goal.trajectory = msg
        self._client.send_goal(goal)
    
if __name__=="__main__":
    rospy.init_node("tuck_arm")
    tuck = tuck_arm()
    
    # tucking or untucking?
    if len(sys.argv) > 1 and sys.argv[1].find("u") > -1:
        tuck.untuck()
    else:
        tuck.tuck()
    
    # sleep three secs (while latched)
    rospy.sleep(3)
