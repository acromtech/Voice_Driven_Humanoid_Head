#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Whiteboard
#  Created by Ingenuity i/o on 2024/11/05
#
# "no description"
#

import signal
import getopt
import time
from pathlib import Path
import traceback
import sys

from Whiteboard import *

port = 5670
agent_name = "Whiteboard"
device = None
verbose = False
is_interrupted = False

short_flag = "hvip:d:n:"
long_flag = ["help", "verbose", "interactive_loop", "port=", "device=", "name="]

ingescape_path = Path("~/Documents/Ingescape").expanduser()


def print_usage():
    print("Usage example: ", agent_name, " --verbose --port 5670 --device device_name")
    print("\nthese parameters have default value (indicated here above):")
    print("--verbose : enable verbose mode in the application (default is disabled)")
    print("--port port_number : port used for autodiscovery between agents (default: 31520)")
    print("--device device_name : name of the network device to be used (useful if several devices available)")
    print("--name agent_name : published name for this agent (default: ", agent_name, ")")
    print("--interactive_loop : enables interactive loop to pass commands in CLI (default: false)")


def print_usage_help():
    print("Available commands in the terminal:")
    print("	/quit : quits the agent")
    print("	/help : displays this message")

def return_io_value_type_as_str(value_type):
    if value_type == igs.INTEGER_T:
        return "Integer"
    elif value_type == igs.DOUBLE_T:
        return "Double"
    elif value_type == igs.BOOL_T:
        return "Bool"
    elif value_type == igs.STRING_T:
        return "String"
    elif value_type == igs.IMPULSION_T:
        return "Impulsion"
    elif value_type == igs.DATA_T:
        return "Data"
    else:
        return "Unknown"

def return_event_type_as_str(event_type):
    if event_type == igs.PEER_ENTERED:
        return "PEER_ENTERED"
    elif event_type == igs.PEER_EXITED:
        return "PEER_EXITED"
    elif event_type == igs.AGENT_ENTERED:
        return "AGENT_ENTERED"
    elif event_type == igs.AGENT_UPDATED_DEFINITION:
        return "AGENT_UPDATED_DEFINITION"
    elif event_type == igs.AGENT_KNOWS_US:
        return "AGENT_KNOWS_US"
    elif event_type == igs.AGENT_EXITED:
        return "AGENT_EXITED"
    elif event_type == igs.AGENT_UPDATED_MAPPING:
        return "AGENT_UPDATED_MAPPING"
    elif event_type == igs.AGENT_WON_ELECTION:
        return "AGENT_WON_ELECTION"
    elif event_type == igs.AGENT_LOST_ELECTION:
        return "AGENT_LOST_ELECTION"
    else:
        return "UNKNOWN"

def signal_handler(signal_received, frame):
    global is_interrupted
    print("\n", signal.strsignal(signal_received), sep="")
    is_interrupted = True


def on_agent_event_callback(event, uuid, name, event_data, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Whiteboard)
        # add code here if needed
    except:
        print(traceback.format_exc())


def on_freeze_callback(is_frozen, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Whiteboard)
        # add code here if needed
    except:
        print(traceback.format_exc())


# inputs
def Title_input_callback(io_type, name, value_type, value, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Whiteboard)
        agent_object.TitleI = value
        # add code here if needed
    except:
        print(traceback.format_exc())

def Backgroundcolor_input_callback(io_type, name, value_type, value, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Whiteboard)
        agent_object.BackgroundcolorI = value
        # add code here if needed
    except:
        print(traceback.format_exc())

def Labelsvisible_input_callback(io_type, name, value_type, value, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Whiteboard)
        agent_object.LabelsvisibleI = value
        # add code here if needed
    except:
        print(traceback.format_exc())

def Chatmessage_input_callback(io_type, name, value_type, value, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Whiteboard)
        agent_object.ChatmessageI = value
        # add code here if needed
    except:
        print(traceback.format_exc())

def Clear_input_callback(io_type, name, value_type, value, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Whiteboard)
        # add code here if needed
    except:
        print(traceback.format_exc())

def Ui_Command_input_callback(io_type, name, value_type, value, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Whiteboard)
        agent_object.Ui_CommandI = value
        # add code here if needed
    except:
        print(traceback.format_exc())

# services
def Chat_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Whiteboard)
        Message = tuple_args[0]
        agent_object.Chat(sender_agent_name, sender_agent_uuid, Message)
    except:
        print(traceback.format_exc())


def Snapshot_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Whiteboard)
        agent_object.Snapshot(sender_agent_name, sender_agent_uuid)
    except:
        print(traceback.format_exc())


def Clear_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Whiteboard)
        agent_object.Clear(sender_agent_name, sender_agent_uuid)
    except:
        print(traceback.format_exc())


def Showlabels_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Whiteboard)
        agent_object.Showlabels(sender_agent_name, sender_agent_uuid)
    except:
        print(traceback.format_exc())


def Hidelabels_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Whiteboard)
        agent_object.Hidelabels(sender_agent_name, sender_agent_uuid)
    except:
        print(traceback.format_exc())


def Addshape_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Whiteboard)
        Type = tuple_args[0]
        X = tuple_args[1]
        Y = tuple_args[2]
        Width = tuple_args[3]
        Height = tuple_args[4]
        Fill = tuple_args[5]
        Stroke = tuple_args[6]
        Strokewidth = tuple_args[7]
        agent_object.Addshape(sender_agent_name, sender_agent_uuid, Type, X, Y, Width, Height, Fill, Stroke, Strokewidth)
    except:
        print(traceback.format_exc())


def Addtext_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Whiteboard)
        Text = tuple_args[0]
        X = tuple_args[1]
        Y = tuple_args[2]
        Color = tuple_args[3]
        agent_object.Addtext(sender_agent_name, sender_agent_uuid, Text, X, Y, Color)
    except:
        print(traceback.format_exc())


def Addimage_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Whiteboard)
        Base64 = tuple_args[0]
        X = tuple_args[1]
        Y = tuple_args[2]
        Width = tuple_args[3]
        Height = tuple_args[4]
        agent_object.Addimage(sender_agent_name, sender_agent_uuid, Base64, X, Y, Width, Height)
    except:
        print(traceback.format_exc())


def Addimagefromurl_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Whiteboard)
        Url = tuple_args[0]
        X = tuple_args[1]
        Y = tuple_args[2]
        agent_object.Addimagefromurl(sender_agent_name, sender_agent_uuid, Url, X, Y)
    except:
        print(traceback.format_exc())


def Remove_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Whiteboard)
        Elementid = tuple_args[0]
        agent_object.Remove(sender_agent_name, sender_agent_uuid, Elementid)
    except:
        print(traceback.format_exc())


def Translate_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Whiteboard)
        Elementid = tuple_args[0]
        Dx = tuple_args[1]
        Dy = tuple_args[2]
        agent_object.Translate(sender_agent_name, sender_agent_uuid, Elementid, Dx, Dy)
    except:
        print(traceback.format_exc())


def Moveto_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Whiteboard)
        Elementid = tuple_args[0]
        X = tuple_args[1]
        Y = tuple_args[2]
        agent_object.Moveto(sender_agent_name, sender_agent_uuid, Elementid, X, Y)
    except:
        print(traceback.format_exc())


def Setstringproperty_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Whiteboard)
        Elementid = tuple_args[0]
        Property = tuple_args[1]
        Value = tuple_args[2]
        agent_object.Setstringproperty(sender_agent_name, sender_agent_uuid, Elementid, Property, Value)
    except:
        print(traceback.format_exc())


def Setdoubleproperty_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Whiteboard)
        Elementid = tuple_args[0]
        Property = tuple_args[1]
        Value = tuple_args[2]
        agent_object.Setdoubleproperty(sender_agent_name, sender_agent_uuid, Elementid, Property, Value)
    except:
        print(traceback.format_exc())


def Getelementids_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Whiteboard)
        agent_object.Getelementids(sender_agent_name, sender_agent_uuid)
    except:
        print(traceback.format_exc())


def Getelements_callback(sender_agent_name, sender_agent_uuid, service_name, tuple_args, token, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, Whiteboard)
        agent_object.Getelements(sender_agent_name, sender_agent_uuid)
    except:
        print(traceback.format_exc())


if __name__ == "__main__":

    # catch SIGINT handler before starting agent
    signal.signal(signal.SIGINT, signal_handler)
    interactive_loop = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_flag, long_flag)
    except getopt.GetoptError as err:
        igs.error(err)
        sys.exit(2)
    for o, a in opts:
        if o == "-h" or o == "--help":
            print_usage()
            exit(0)
        elif o == "-v" or o == "--verbose":
            verbose = True
        elif o == "-i" or o == "--interactive_loop":
            interactive_loop = True
        elif o == "-p" or o == "--port":
            port = int(a)
        elif o == "-d" or o == "--device":
            device = a
        elif o == "-n" or o == "--name":
            agent_name = a
        else:
            assert False, "unhandled option"

    igs.agent_set_name(agent_name)
    igs.log_set_console(verbose)
    igs.log_set_file(True, None)
    igs.log_set_stream(verbose)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.debug(f"Ingescape version: {igs.version()} (protocol v{igs.protocol()})")

    if device is None:
        # we have no device to start with: try to find one
        list_devices = igs.net_devices_list()
        list_addresses = igs.net_addresses_list()
        if len(list_devices) == 1:
            device = list_devices[0]
            igs.info("using %s as default network device (this is the only one available)" % str(device))
        elif len(list_devices) == 2 and (list_addresses[0] == "127.0.0.1" or list_addresses[1] == "127.0.0.1"):
            if list_addresses[0] == "127.0.0.1":
                device = list_devices[1]
            else:
                device = list_devices[0]
            print("using %s as de fault network device (this is the only one available that is not the loopback)" % str(device))
        else:
            if len(list_devices) == 0:
                igs.error("No network device found: aborting.")
            else:
                igs.error("No network device passed as command line parameter and several are available.")
                print("Please use one of these network devices:")
                for device in list_devices:
                    print("	", device)
                print_usage()
            exit(1)

    agent = Whiteboard()

    igs.observe_agent_events(on_agent_event_callback, agent)
    igs.observe_freeze(on_freeze_callback, agent)

    igs.input_create("title", igs.STRING_T, None)
    igs.input_create("backgroundColor", igs.STRING_T, None)
    igs.input_create("labelsVisible", igs.BOOL_T, None)
    igs.input_create("chatMessage", igs.STRING_T, None)
    igs.input_create("clear", igs.IMPULSION_T, None)
    igs.input_create("ui_command", igs.STRING_T, None)

    igs.output_create("lastChatMessage", igs.STRING_T, None)
    igs.output_create("lastAction", igs.STRING_T, None)
    igs.output_create("ui_error", igs.STRING_T, None)

    igs.observe_input("title", Title_input_callback, agent)
    igs.observe_input("backgroundColor", Backgroundcolor_input_callback, agent)
    igs.observe_input("labelsVisible", Labelsvisible_input_callback, agent)
    igs.observe_input("chatMessage", Chatmessage_input_callback, agent)
    igs.observe_input("clear", Clear_input_callback, agent)
    igs.observe_input("ui_command", Ui_Command_input_callback, agent)

    igs.service_init("chat", Chat_callback, agent)
    igs.service_arg_add("chat", "message", igs.STRING_T)
    igs.service_init("snapshot", Snapshot_callback, agent)
    igs.service_init("clear", Clear_callback, agent)
    igs.service_init("showLabels", Showlabels_callback, agent)
    igs.service_init("hideLabels", Hidelabels_callback, agent)
    igs.service_init("addShape", Addshape_callback, agent)
    igs.service_arg_add("addShape", "type", igs.STRING_T)
    igs.service_arg_add("addShape", "x", igs.DOUBLE_T)
    igs.service_arg_add("addShape", "y", igs.DOUBLE_T)
    igs.service_arg_add("addShape", "width", igs.DOUBLE_T)
    igs.service_arg_add("addShape", "height", igs.DOUBLE_T)
    igs.service_arg_add("addShape", "fill", igs.STRING_T)
    igs.service_arg_add("addShape", "stroke", igs.STRING_T)
    igs.service_arg_add("addShape", "strokeWidth", igs.DOUBLE_T)
    igs.service_init("addText", Addtext_callback, agent)
    igs.service_arg_add("addText", "text", igs.STRING_T)
    igs.service_arg_add("addText", "x", igs.DOUBLE_T)
    igs.service_arg_add("addText", "y", igs.DOUBLE_T)
    igs.service_arg_add("addText", "color", igs.STRING_T)
    igs.service_init("addImage", Addimage_callback, agent)
    igs.service_arg_add("addImage", "base64", igs.DATA_T)
    igs.service_arg_add("addImage", "x", igs.DOUBLE_T)
    igs.service_arg_add("addImage", "y", igs.DOUBLE_T)
    igs.service_arg_add("addImage", "width", igs.DOUBLE_T)
    igs.service_arg_add("addImage", "height", igs.DOUBLE_T)
    igs.service_init("addImageFromUrl", Addimagefromurl_callback, agent)
    igs.service_arg_add("addImageFromUrl", "url", igs.STRING_T)
    igs.service_arg_add("addImageFromUrl", "x", igs.DOUBLE_T)
    igs.service_arg_add("addImageFromUrl", "y", igs.DOUBLE_T)
    igs.service_init("remove", Remove_callback, agent)
    igs.service_arg_add("remove", "elementId", igs.INTEGER_T)
    igs.service_init("translate", Translate_callback, agent)
    igs.service_arg_add("translate", "elementId", igs.INTEGER_T)
    igs.service_arg_add("translate", "dx", igs.DOUBLE_T)
    igs.service_arg_add("translate", "dy", igs.DOUBLE_T)
    igs.service_init("moveTo", Moveto_callback, agent)
    igs.service_arg_add("moveTo", "elementId", igs.INTEGER_T)
    igs.service_arg_add("moveTo", "x", igs.DOUBLE_T)
    igs.service_arg_add("moveTo", "y", igs.DOUBLE_T)
    igs.service_init("setStringProperty", Setstringproperty_callback, agent)
    igs.service_arg_add("setStringProperty", "elementId", igs.INTEGER_T)
    igs.service_arg_add("setStringProperty", "property", igs.STRING_T)
    igs.service_arg_add("setStringProperty", "value", igs.STRING_T)
    igs.service_init("setDoubleProperty", Setdoubleproperty_callback, agent)
    igs.service_arg_add("setDoubleProperty", "elementId", igs.INTEGER_T)
    igs.service_arg_add("setDoubleProperty", "property", igs.STRING_T)
    igs.service_arg_add("setDoubleProperty", "value", igs.DOUBLE_T)
    igs.service_init("getElementIds", Getelementids_callback, agent)
    igs.service_init("getElements", Getelements_callback, agent)

    igs.start_with_device(device, port)
    # catch SIGINT handler after starting agent
    signal.signal(signal.SIGINT, signal_handler)

    if interactive_loop:
        print_usage_help()
        while True:
            command = input()
            if command == "/quit":
                break
            elif command == "/help":
                print_usage_help()
    else:
        while (not is_interrupted) and igs.is_started():
            time.sleep(2)

    if igs.is_started():
        igs.stop()
