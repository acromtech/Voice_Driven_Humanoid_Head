#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  RobotHead.py
#  RobotHead
#  Created by Ingenuity i/o on 2024/11/25
#
# "no description"
#
import ingescape as igs


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class RobotHead(metaclass=Singleton):
    def __init__(self):
        # inputs
        self.Agent_NameI = None
        self.DeviceI = None
        self.PortI = None
        self.Simulation_ModeI = None


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

    def Clear_All(self, sender_agent_name, sender_agent_uuid):
        pass
        # add code here if needed

    def Gif_Choice(self, sender_agent_name, sender_agent_uuid, Answer_Eyes):
        pass
        # add code here if needed

    def Stop(self, sender_agent_name, sender_agent_uuid):
        pass
        # add code here if needed


