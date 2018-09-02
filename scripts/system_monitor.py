#!/usr/bin/env python3

import os
import sys
import time
import numpy
import datetime

import rospy
from std_msgs.msg import Float64


# --
data_exp_dir = '/home/amigos/data/experiment/'
nname = 'system_monitor'
home_dir = os.path.join(data_exp_dir, nname)
# --

interval = int(sys.argv[1])


class status_monitor(object):
    
    def __init__(self):
        self.l218_ch5 = 0
        self.l218_ch6 = 0
        self.l218_ch7 = 0
        self.power_ch1 = 0
        self.power_ch2 = 0
        self.sisv_ch1 = 0
        self.sisi_ch1 = 0
        self.sisv_ch2 = 0
        self.sisi_ch2 = 0
        self.sub_l218_ch5 = rospy.Subscriber('lakeshore_ch5', Float64, self.callback_l218, callback_args=5)
        self.sub_l218_ch6 = rospy.Subscriber('lakeshore_ch6', Float64, self.callback_l218, callback_args=6)
        self.sub_l218_ch6 = rospy.Subscriber('lakeshore_ch7', Float64, self.callback_l218, callback_args=7)
        self.sub_sisv_ch1 = rospy.Subscriber('cpz3177_ch1', Float64, self.callback_sis, callback_args='sisv_ch1')
        self.sub_sisi_ch1 = rospy.Subscriber('cpz3177_ch2', Float64, self.callback_sis, callback_args='sisi_ch1')
        self.sub_sisv_ch2 = rospy.Subscriber('cpz3177_ch3', Float64, self.callback_sis, callback_args='sisv_ch2')
        self.sub_sisi_ch2 = rospy.Subscriber('cpz3177_ch4', Float64, self.callback_sis, callback_args='sisi_ch2')
        self.sub_power_ch1 = rospy.Subscriber('cpz3177_ch33', Float64, self.callback_power, callback_args='power_ch1')
        self.sub_power_ch2 = rospy.Subscriber('cpz3177_ch34', Float64, self.callback_power, callback_args='power_ch2')
        pass

    def callback_l218(self, req, ch):
        exec('self.l218_ch{} = req.data'.format(ch))
        return

    def callback_sis(self, req, name):
        exec('self.{} = req.data'.format(name))
        return

    def callback_power(self, req, name):
        exec('self.{} = req.data'.format(name))
        return

    def write_file(self):
        now = datetime.datetime.utcnow()
        day = now.strftime("%Y%m%d_")
        name = now.strftime("%H%M%S")
        filename =  day + name + ".txt"
        saveto = os.path.join(home_dir, filename)
        print(saveto)
        while not rospy.is_shutdown():
            ctime = time.time()
            f = open(saveto, 'a')
            ch5_K = self.l218_ch5
            ch6_K = self.l218_ch6
            ch7_K = self.l218_ch7         
            dBm1 = self.power_ch1
            dBm2 = self.power_ch2
            ch1_mv = self.sisv_ch1 * 10
            ch1_ua = self.sisi_ch1 * 1000
            ch2_mv = self.sisv_ch2 * 10
            ch2_ua = self.sisi_ch2 * 1000
            msg1 = '{ctime:.1f} {ch5_K:.1f} {ch6_K:.1f} {ch7_K:.1f} {dBm1:+.1f} {dBm2:+.1f} {ch1_mv:+.1f} {ch1_ua:+.1f} {ch2_mv:+.1f} {ch2_ua:+.1f}\n'.format(**locals())
            msg2 = '{ctime:.1f} {ch5_K:.1f}K {ch6_K:.1f}K {ch7_K:.1f}K {dBm1:+.1f}dBm {dBm2:+.1f}dBm {ch1_mv:+.1f}mV {ch1_ua:+.1f}uA {ch2_mv:+.1f}mV {ch2_ua:+.1f}uA'.format(**locals())            
            print(msg2)
            f.write(msg1)
            f.close()

            time.sleep(interval)
            continue
        return    

if __name__ == '__main__':
    if not os.path.exists(home_dir):
        os.makedirs(home_dir)
        pass

    st = status_monitor()
    rospy.init_node(nname)
    ut = time.gmtime()
    print('start recording [filename :'+time.strftime("%Y%m%d_%H%M%S", ut)+'.txt]')
    st.write_file()
             
        
