#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  RobotHead.py
#  RobotHead
#  Created by Ingenuity i/o on 2024/11/24
#
# "no description"
#

import ingescape as igs
import ctypes
import os
import time

# services
def Add_Image_callback(agent, sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    agent_object = my_data
    assert isinstance(agent_object, RobotHead)
    Image_Path = tuple_args[0]
    X = tuple_args[1]
    Y = tuple_args[2]
    Width = tuple_args[3]
    Height = tuple_args[4]
    agent_object.Add_Image(sender_agent_name, sender_agent_uuid, Image_Path, X, Y, Width, Height)

def Chat_callback(agent, sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    agent_object = my_data
    assert isinstance(agent_object, RobotHead)
    Message_Text = tuple_args[0]
    agent_object.Chat(sender_agent_name, sender_agent_uuid, Message_Text)

def Clear_callback(agent, sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    agent_object = my_data
    assert isinstance(agent_object, RobotHead)
    agent_object.Clear(sender_agent_name, sender_agent_uuid)

def Gif_Choice_callback(agent, sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    agent_object = my_data
    assert isinstance(agent_object, RobotHead)
    Answer_Eyes = tuple_args[0]
    agent_object.Gif_Choice(sender_agent_name, sender_agent_uuid, Answer_Eyes)

def Stop_callback(agent, sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    agent_object = my_data
    assert isinstance(agent_object, RobotHead)
    agent_object.Stop(sender_agent_name, sender_agent_uuid)


class RobotHead(igs.Agent):
    def __init__(self, activated = True):
        super().__init__("RobotHead", activated)

        self.service_init("add_image", Add_Image_callback, self)
        self.service_arg_add("add_image", "image_path", igs.STRING_T)
        self.service_arg_add("add_image", "x", igs.INTEGER_T)
        self.service_arg_add("add_image", "y", igs.INTEGER_T)
        self.service_arg_add("add_image", "width", igs.INTEGER_T)
        self.service_arg_add("add_image", "height", igs.INTEGER_T)

        self.service_init("chat", Chat_callback, self)
        self.service_arg_add("chat", "message_text", igs.STRING_T)

        self.service_init("clear", Clear_callback, self)

        self.service_init("gif_choice", Gif_Choice_callback, self)
        self.service_arg_add("gif_choice", "answer_eyes", igs.STRING_T)

        self.service_init("stop", Stop_callback, self)



    # services
    def Add_Image(self, sender_agent_name, sender_agent_uuid, Image_Path, X, Y, Width, Height):
        pass
        # add code here if needed

    def Chat(self, sender_agent_name, sender_agent_uuid, Message_Text):
        pass
        # add code here if needed

    def Clear(self, sender_agent_name, sender_agent_uuid):
        pass
        # add code here if needed

    def Gif_Choice(self, sender_agent_name, sender_agent_uuid, Answer_Eyes):
        pass
        # add code here if needed

    def Stop(self, sender_agent_name, sender_agent_uuid):
        pass
        # add code here if needed




