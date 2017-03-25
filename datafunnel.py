#gr-spacebase project github.com/wirrell/gr-spacebase
#This file contains the datafunnel object which handles
#plotting functions that plot the status of
#TV whitespace channels as bar charts to display to the operator

import numpy as np
import matplotlib.pyplot as plt
import time

class datafunnel(object):

    """Plots the status of channels sent by the controller.
    Required args:
        channel_bank : should be a
    dictionary of the form {'channel_num' : uhf_channel}

    plot(status_data) : Called to initially plot the first data sent
    through."""

    

    def __init__(self, channel_bank):
        self.channel_list = self.__ordered(channel_bank)
        self.T_plot, self.B_plot = self.__datasort()



    def __ordered(self, input_dict, want_data=False):
        
        """PRIVATE METHOD: Sorts dictionary keys that are sent to channelplot.
        Structured so that unordered dictionaries used for convenience handling
        of uhf channels 21 through 68 in the controller can be sorted into
        numerical order for data plotting. want_data flag used if dictionary
        data is required in order of channel number."""

        int_list = [int(x) for x in input_dict.keys()]
        int_list = sorted(int_list)
        if not want_data:
            return [str(x) for x in int_list]
        ordered_data = []
        for k in [str(x) for x in int_list]:
            ordered_data.append(input_dict[k])
        return ordered_data

    def __datasort(self):

        """PRIVATE METHOD: Returns the sorted channel values. If more than 20
        channels have been sent to be plotted, __datasort() splits them into
        two sets."""

        N = len(self.channel_list)
        #if more than 20 channels to be plotted, split into two sets
        if N > 20:
            T_plot = self.channel_list[:(N//2)]
            B_plot = self.channel_list[(N//2):]
            return T_plot, B_plot
        return self.channel_list, None

    def plot(self, input_data):

        """Plots the status data passed in by the controller. If more
        than 20 points are present, two figures are plotted."""
        
        plt.ion()
        status_data = self.__ordered(input_data, True) #order status data
        ylabels = (('UNOCCUPIED', '', 'UNKNOWN', '', 'OCCUPIED'))#y axis labels
        T_pos = np.arange(len(self.T_plot))
        T_sdata = np.array(status_data[:len(self.T_plot)])
        fig = plt.figure()#initialise figure plot
        subT = fig.add_subplot(211) #enter first subfigure
        dataT = subT.bar(T_pos, T_sdata, align='center', tick_label=self.T_plot)
        subT.set_yticklabels(ylabels) #set ylabels
        plt.axis('tight') #required to ensure bars plot flush to figure
        if self.B_plot:
            #if two sets have been created
            B_pos = np.arange(len(self.B_plot))
            B_sdata = np.array(status_data[len(self.T_plot):])
            subB = fig.add_subplot(212) #initialise new subplot
            dataB = subB.bar(B_pos, B_sdata, align='center', tick_label=self.B_plot)
            subB.set_yticklabels(ylabels)#label y-axis
        fig.canvas.set_window_title('Channel Status Plot @' \
                                    ' {}'.format(time.strftime('%X %x %Z')))
        plt.axis('tight')
        fig.tight_layout() #required to prevent y-labels from being cut off
        fig.canvas.draw()


if __name__ == '__main__':
    dummy_channel_bank = {}
    for i in range(1,40):
        dummy_channel_bank['{}'.format(i)] = 'dummy'
    plotter = datafunnel(dummy_channel_bank)
    dummy_status_data = {}
    for i in range(1,40):
        dummy_status_data['{}'.format(i)] = (np.random.randint(0,2))
    plotter.plot(dummy_status_data)
    while True:
        dummy_status_data_2 = {}
        print 'Running next plot test'
        time.sleep(3)
        for i in range(1,40):
            dummy_status_data_2['{}'.format(i)] = (np.random.randint(0,2))
        plotter.plot(dummy_status_data_2)
        raw_input('Press enter for next plot test.')


    
