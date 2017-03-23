#gr-spacebase project github.com/wirrell/gr-spacebase
#This file contains the class for the main controller
#The controller instances channel objects and stores
#them in a channel banks whilst continuously monitoring
#their status and last scan time.

from channel_list import uhfchanlist
import uhf_channel
import os
import sys
import random
import pprint
import time

class controller(object):

    """Controller class which stores and monitors all channels.
    monitor : method that continously monitors the status of channels and runs
    update scans.
    
    __define_update : Returns the prefered output function for the class.
    Defaults to sys.stdout.write but can be passed a pipe from outside.
    
    __buildchannels : builds full channel bank and stores channel classes
    
    __initialscan : runs inital scan for all stored channels
    
    __dataupdate : FIXME Under construction data output method
    
    channel_bank : stored channels
    status_bank : stored channels' statuses
    time_bank : time of each stored channel's last scan"""

    def __init__(self, pipeout=False): #pipeout is passed pipe for output
        self.chan_list = uhfchanlist().full_list()#chan nums and frequencies
        self.channel_bank = {}#stores instanced channel classes
        self.status_bank = {}#stores channel occupied status
        self.time_bank = {}#stores channel lastscan times
        self.pipeout = pipeout
        self.__buildchannels()
        self.__initialscan()
        self.monitor()

    def __postupdate(self, x):
        print 'in post update'
        """PRIVATE METHOD: Defines whether the postupdate function passes to a
        pipe or sys.stdout.write()"""
        x = x + '\n'
        os.write(self.pipeout, x) 
        #print x


        
    def __buildchannels(self):
        """PRIVATE METHOD: instances channel classes using frequencies data
        taken from uhfchanlist.full_list. Stores instanced channels in
        self.channel_bank using the same keys provided by full_list."""
        for chan_num, frequencies in self.chan_list.iteritems():
            channel = uhf_channel.channel(chan_num, frequencies)
            self.channel_bank[chan_num] = channel
            
    def __initialscan(self):
        """PRIVATE METHOD: runs initial scan of all instances channels and
        saves both their status and lastscan time to self.status_bank and
        self.time_bank respectively."""
        for channel in self.channel_bank:
            if not self.channel_bank[channel].scan():
                self.__postupdate("""Inital Scan for channel {}
                                failed""".format(channel))
                continue #If channel scan fails, moves to next channel
            self.__postupdate("Initial Scan of channel {} complete, STATUS :\
            {}".format(
                                                self.channel_bank[channel].chan_id,
                                                self.channel_bank[channel].status))
            self.status_bank[channel] = self.channel_bank[channel].status
            self.time_bank[channel] = self.channel_bank[channel].lastscan

    def monitor(self):
        """monitor method: sorts channels into high and low priority lists
        based on their status. Iteratively scans all high priority channels as
        well as one low priority channel chosen at random. After each scan loop
        a child process is spawned using os.fork() which runs the private
        __dataupdate function to display the latest data to the operator."""
        high_priority = []
        low_priority = []
        for channel_num, channel in self.channel_bank.iteritems():
            if channel.status == 'OCCUPIED': 
                #occupied channels are low scanning priority
                low_priority.append(channel)
                continue
            high_priority.append(channel)
        while True:
            for channel in high_priority: #scan all channels in high priority
                if not channel.scan():
                    self.__postupdate("Routine scan of {} failed.".format(
                                                                channel.chan_id))
                    continue #If channel scan fails, moves to next channel
                if channel.status == 'OCCUPIED':
                    #move to low priority and update status bank
                    high_priority.remove(channel)
                    low_priority.append(channel)
                    self.status_bank[channel.chan_id] = 'OCCUPIED'
                    self.time_bank[channel.chan_id] = channel.lastscan
                self.__postupdate("High Priority Channel {} scanned. STATUS :\
                {}".format(
                                                               channel.chan_id,
                                                               channel.status))
            low_random = random.choice(low_priority)
            #check a low priority channel at random
            if not occupied_random.scan():
                self.__postupdate("Routine scan of {} failed.".format(
                                                            low_random.chan_id))
                continue #If channel scan fails, move to next channel
            if low_random.status != 'OCCUPIED':
                #if channel status has changed, move to high priority queue
                low_priority.remove(low_random)
                high_priority.append(low_random)
                self.status_bank[low_random.chan_id] = low_random.status
                self.time_bank[low_random.chan_id] = low_random.lastscan
                self.__postupdate("Low Priority Channel {} scanned. STATUS :\
                {}".format(
                                                               channel.chan_id,
                                                               channel.status))
            self.__postupdate("monitor pass complete")
            #spawn child process to display data to operator whilst
            #parent continues to monitor channels
            pid = os.fork()
            if not pid:
                #within child process
                self.__dataupdate()

    def __dataupdate(self):
        os._exit(0)
        #FIXME data plotting method to be written
        



if __name__ == '__main__':
    print "controller.py : Running controller class test"
    print "use keyboard interupt 'ctrl-c' to exit."
    time.sleep(2)
    print "test starting"
    test_controller = controller()
