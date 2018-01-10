#!/usr/bin/env python
import rospy

# to get commandline arguments
import sys

# Because of transformations
import tf
import tf2_ros

def broadcast_euclid_transform(tx, ty, tz, rx, ry, rz):
    pass


if __name__ == '__main__':
    tx = float(sys.argv[1])  # this is ROS coordinates, so in meters and radians
    ty = float(sys.argv[2])
    tz = float(sys.argv[3])
    rx = float(sys.argv[4])
    ry = float(sys.argv[5])
    rz = float(sys.argv[6])

    rospy.init_node("transform_broadcast_tester")
    rotation = tf.transformations.quaternion_from_euler(rx, ry, rz)


    br = tf2_ros.StaticTransformBroadcaster()
    # noinspection PyArgumentList
    br.sendTransform(
        (tx, ty, tz),
        rotation,
        rospy.Time.now(),
        "commu_link",  # Publish a transform to `commu_link` (the origin of the commu coordinate system)
        "camera_link"  # to `camera_link` (provided by euclid)
    )

    rospy.spin()
