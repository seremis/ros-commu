#!/usr/bin/env python

import sys

import rospy
from ssd.msg import ClassifiedObjectArray, ClassifiedObject

from dialogue.dialogue_definition_quiz_objects import DialogueLibraryQuiz
from dialogue.dialogue_manager import DialogueManager


def classification_result_callback(manager, data):
    # type: (DialogueManager, ClassifiedObjectArray) -> None
    rospy.logdebug("Received classification results with {} objects.".format(len(data.objects)))

    image = data.image

    for obj in data.objects:  # type: ClassifiedObject
        short_term_history = manager.get_topic_history()[-10:]

        count = short_term_history.count(obj.label)

        if count <= 0:

            area = obj.bbox.x_size * obj.bbox.y_size
            norm_area = area / (image.width * image.height)

            if obj.label == "person":
                priority = norm_area * 1.5
                if priority > 1:
                    priority = 1

                manager.add_topic(obj.label, obj.id, priority)
            else:
                manager.add_topic(obj.label, obj.id, norm_area)


def init_message_listeners(manager):
    rospy.loginfo("Initializing message listeners...")

    def classification_callback(data):
        classification_result_callback(manager, data)

    rospy.Subscriber("/ssd_node/classification_result", ClassifiedObjectArray, classification_callback)

    rospy.loginfo("Initializing message listeners done.")


def init_message_publishers(manager):
    rospy.loginfo("Initializing message publishers...")

    rospy.loginfo("Initializing message publishers done.")


if __name__ == '__main__':
    rospy.init_node("dialogue")
    rospy.loginfo("Starting dialogue node..")

    rospy.loginfo("Creating DialogueManager..")

    manager = DialogueManager(DialogueLibraryQuiz())

    rospy.loginfo("DialogueManager created.")

    init_message_listeners(manager)
    init_message_publishers(manager)

    try:
        manager.start(False)
    except:
        e = sys.exc_info()[0]
        rospy.loginfo("DialogueManager stopped because of an error.")
        rospy.loginfo(e)
