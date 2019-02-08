#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Copyright (c) 2016 Xu Zhihao (Howe).  All rights reserved.
This program is free software; you can redistribute it and/or modify
This programm is tested on kuboki base turtlebot."""
'''
或许为了能够尽量准确的被唤醒，所以，要给robot起一个比较生癖的名字，例如，小达
'''


import array
import base64
import chunk
import json
import os
import sys
import wave

import numpy as np
import requests
import rospy
from pyaudio import PyAudio, paInt16
from std_msgs.msg import String
import datalib


class for_hearder():
    def __init__(self):
        # if_continue = ''
        # while not rospy.is_shutdown() and if_continue == '':
        #     self.define()
        #     self.recode()
        #     words = self.reg()
        #     reg = rospy.Publisher('tts_for_pub_to_speaker', String, queue_size=1)
        #     reg.publish(words)
        #     #self.savewav("testing")#testing
        #     if_continue = raw_input('pls input ＥＮＴＥＲ to continue')
        pass
    #全局变量，判断，当，把文字传给speak后，speak说完后，才能进行下一步。
    # isSpeaked = False
    isResult = 'listen'
    dl = datalib.datalib()
    datalibs = dl.datadict
    tts_for_pub_to_speaker = None
    gps_for_pub = None
    gps_for_sub = None
    returnsth_info = 'default'
    returnsth_gps  = 'default'
    def run_for_hearder(self):
        # self.define()
        # self.offlineCalled()
        # tts_for_pub_to_speaker = rospy.Publisher('tts_for_pub_to_speaker', String, queue_size=1)
        # rospy.Subscriber('tts_for_pub_to_speaker', String, self.getsubscriber, queue_size=1)
        # #第一次语音识别，目的是要听到robot名字（小达）
        # words = self.reg()
        # speaker_words = None
        # if not '你好世界' in words:
        #     print '你说的并不是你好世界，请叫我名字，你好世界'
        #     print '你说的是，',words
        #     self.isResult = 'right'
        #     #判断是否是报错，如果报错，也需要输出
        #     if 'x' in words:
        #         wordss = words[1:]
        #         wordss += '请再说一遍'
        #         #hearder和speaker的识别符，以减轻代码压力
        #         wordss += ')'
        #         tts_for_pub_to_speaker.publish(wordss)
        #         self.isResult = 'wrong'
        #     if self.isResult == 'right':
        #         self.offlineCalled()
        # #while:end
        # #意味着离线唤醒已经ok
        # #接下来是语音识别
        # if self.isResult == 'right':
        #     tts_for_pub_to_speaker.publish('嘿，吃过饭了吗，我听到了你的呼唤，我的名字叫,你好世界，很高兴和你交流(')
        #     self.mainChat()
        #     words = self.reg()
        #     #将结果输出及publish后，进行判断模块
        #     self.mainReCalled()

        self.define()
        gps_for_pub = rospy.Publisher('chatter',String)
        gps_for_sub = rospy.Subscriber('speachnav',String,self.gpsrecall,queue_size=1)
        while not rospy.is_shutdown():
            rospy.Subscriber('stt_for_pub_to_hearder', String, self.getsubscriber, queue_size=1)
            if self.isResult == 'listen':
                self.offlineCalled()
                self.tts_for_pub_to_speaker = rospy.Publisher('tts_for_pub_to_speaker', String, queue_size=1)
                #第一次语音识别，目的是要听到robot名字（小达）
                words = self.reg()
                speaker_words = None
                if not '你好世界' in words and not 'x' in words:
                    print '你说的是，',words,',请叫我名字，你好世界'
                    wordss = '你说的是，'+words+',请叫我名字，你好世界'
                    self.tts_for_pub_to_speaker.publish(wordss)
                    self.isResult = 'waitspeakfinish'
                    #判断是否是报错，如果报错，也需要输出
                elif 'x' in words:
                    wordss = words[1:]
                    wordss += '请再说一遍'
                    #hearder和speaker的识别符，以减轻代码压力
                    wordss += ')'
                    self.tts_for_pub_to_speaker.publish(wordss)
                    self.isResult = 'waitspeakfinish'
                else:
                    # tts_for_pub_to_speaker.publish('你好世界为您服务，我的语音结束后就可以说话')
                    self.tts_for_pub_to_speaker.publish('滴滴，学生卡(')
                    self.isResult = 'waitspeakfinish'
                #意味着离线唤醒开始等待其他结果isResult
            elif self.isResult == 'waitspeakfinish':
                print '等待语音说完，再跳转'
                wait1s = rospy.Rate(5)
                wait1s.sleep()
            elif self.isResult == 'talk':
                #接下来是语音识别
                self.mainChat()
                words = self.reg()
                res = self.mainReCalled(words)
                print 'res 的内容：：：：  ',res
                if res == 'nogps' or res == 'noinfo':
                    self.isResult = 'waitspeakfinish'
                    self.tts_for_pub_to_speaker.publish('未识别到正确语句，请用某某怎么走或者介绍某某与我交流，现在请您重新唤醒我')
                if res == 'togps':
                    self.isResult = 'waitspeakfinish'
                    self.tts_for_pub_to_speaker.publish('正在为您查询路径')
                if res == 'toinfo':
                    # self.isResult = 'waitspeakfinish'
                    # self.tts_for_pub_to_speaker.publish('正在为您查询地点介绍情况')
                    pass
                if res == 'default':
                    self.tts_for_pub_to_speaker.publish('有未定义的情况出现而导致识别不到，sorry哦亲')
                if res == 'endback':
                    pass
                #将结果输出及publish后，进行判断模块
    def getsubscriber(self,recall):
        print 'for_speak返回的数据是 : ',recall.data
        if recall.data == 'ready':
            self.isResult = 'talk'
        if recall.data == 'ok':
            self.isResult = 'listen'
        if recall.data == 'default':
            self.isResult = 'listen'
        print '主进程识别符为 : ',self.isResult
    def gpsrecall(self,recall):
        pass
    def offlineCalled(self):
        pa = PyAudio()
        stream = pa.open(
            format=paInt16,
            channels=self.nchannel,
            rate=self.SAMPLING_RATE,
            input=True,
            frames_per_buffer=self.NUM_SAMPLES)
        save_count = 0
        save_buffer = []
        NO_WORDS = self.NO_WORDS

        #tent42 聆听是一种希望全程存在的一种行为，所以只要roscore没有结束，便一直运行
        while not rospy.is_shutdown():
            # print '后台等待被离线唤醒，robot暂命名：小达 '  # 读入NUM_SAMPLES个取样
            # print 'time_out in', time_out  
            string_audio_data = stream.read(self.NUM_SAMPLES)  # 读入NUM_SAMPLES个取样
            audio_data = np.fromstring(string_audio_data, dtype=np.short) # 将读入的数据转换为数组

            #tent42 开始判断是否有声音
            # no_sounds_time 定义
            if np.max(audio_data) > self.UPPER_LEVEL:
                # 读取语音质量maybe
                large_sample_count = np.sum(audio_data > self.LOWER_LEVEL)
                # 判断语音质量是否可以，如果可以则赋值，下一句if便可以通过
                if large_sample_count > self.COUNT_NUM:
                    save_count = self.SAVE_LENGTH
                # 判断语音质量是否可以
                if save_count > 0:
                    save_buffer.append(string_audio_data)
                print '有声音被听到'
                for int_t in range(1,11):
                    string_audio_data = stream.read(self.NUM_SAMPLES)  # 读入NUM_SAMPLES个取样
                    audio_data = np.fromstring(string_audio_data, dtype=np.short) # 将读入的数据转换为数组
                    print '声音正在捕获，共捕获5秒，现在是第——',int_t,'——秒'
                    # 读取语音质量maybe
                    large_sample_count = np.sum(audio_data > self.LOWER_LEVEL)
                    # 判断语音质量是否可以，如果可以则赋值，下一句if便可以通过
                    if large_sample_count > self.COUNT_NUM:
                        save_count = self.SAVE_LENGTH
                    # 判断语音质量是否可以
                    if save_count > 0:
                        save_buffer.append(string_audio_data)
                #for:end
                if len(save_buffer)>0:
                    self.Voice_String = save_buffer
                    save_buffer=[]
                    print '数据已经写入，开始baidusdk网楼请求stt,break跳出循环，等待语音被解析，以及返回结果'
                #if:end
                break
                #while:break
            print '没有声音，goto到最上层聆听'
            #while:end
    def mainChat(self):
        pa = PyAudio()
        stream = pa.open(
            format=paInt16,
            channels=self.nchannel,
            rate=self.SAMPLING_RATE,
            input=True,
            frames_per_buffer=self.NUM_SAMPLES)
        save_count = 0
        save_buffer = []
        time_out = self.TIME_OUT
        NO_WORDS = self.NO_WORDS
        AlreadySaySth = False

        while not rospy.is_shutdown() and NO_WORDS and time_out:
            time_out -= 1
            print '现在robot开始与人交流，但总时限为60秒，目前秒数——', time_out  # 读入NUM_SAMPLES个取样
            string_audio_data = stream.read(self.NUM_SAMPLES)  # 将读入的数据转换为数组
            audio_data = np.fromstring(string_audio_data, dtype=np.short)

            # 查看是否没有语音输入
            # NO_WORDS -= 1 的意思是，总时长是60s，但是如果开始交流，当判断没有再来语音后5s即退出，而不是再以60s来断
            if np.max(audio_data) > self.UPPER_LEVEL:
                NO_WORDS = self.NO_WORDS
                AlreadySaySth = True
            elif np.max(audio_data) < self.UPPER_LEVEL and AlreadySaySth:
                NO_WORDS -= 1
            else:
                pass
            
            print '等待语音中断时间 ', NO_WORDS
            print '声音质量———————— ', np.max(audio_data)

            # 计算大于LOWER_LEVEL的取样的个数
            large_sample_count = np.sum(audio_data > self.LOWER_LEVEL)

            # 如果个数大于COUNT_NUM，则至少保存SAVE_LENGTH个块
            if large_sample_count > self.COUNT_NUM:
                save_count = self.SAVE_LENGTH
            else:
                save_count -= 1

            # 将要保存的数据存放到save_buffer中
            if save_count < 0:
                save_count = 0
            elif save_count > 0:
                save_buffer.append(string_audio_data)
            else:
                pass

            # 将save_buffer中的数据写入WAV文件，WAV文件的文件名是保存的时刻
            if len(save_buffer) > 0 and NO_WORDS == 0:
                self.Voice_String = save_buffer
                save_buffer = []
                rospy.loginfo("Recode a piece of voice successfully!")
                #return self.Voice_String

            elif len(save_buffer) > 0 and time_out == 0:
                self.Voice_String = save_buffer
                save_buffer = []
                rospy.loginfo("Recode a piece of voice successfully!")
                #return self.Voice_String
            else:
                pass
            #rospy.loginfo( '\n\n')
    def mainReCalled(self,getWords):
        if not '怎么走' in getWords:
            self.returnsth_gps = 'nogps'
        if '怎么走' in getWords:
            self.gps_for_pub.publish(getWords)
        #if:end gps判断结束
        #if:begin info判断开始
        if not '介绍' in getWords:
            self.returnsth_info = 'noinfo'
        if '介绍' in getWords:
            self.returnsth_info = 'toinfo'
            getWords = getWords.replace('介绍','')
            print '去掉getwords杂词，现在的输出是什么：：：',getWords
            if len(getWords) > 0:
                i = len(self.datalibs)
                for key in self.datalibs:
                    i -= 1
                    getWords = getWords.replace(key,'')
                    if len(getWords) <= 0:
                        self.tts_for_pub_to_speaker.publish(self.datalibs[key]+',介绍完毕，想要再次对话还请先唤醒我')
                        self.isResult = 'waitspeakfinish'
                        return 'endback'
                    if len(getWords) >0 and i == 0:
                        return 'noinfo'
        #all_if:end
        #if:begin return
        if 'no' in self.returnsth_gps :
            return self.returnsth_info
        if 'no' in self.returnsth_info:
            return self.returnsth_gps
    def reg(self):
        #get token
        requestData = {
            "grant_type": self.Grant_type,
            "client_id": self.Api_Key,
            "client_secret": self.Secrect_Key
        }

        result = requests.post(url=self.Token_url, data=requestData)

        token_data = json.loads(result.text)

        #self.Print_Response(token_data)

        if 'access_token' in token_data:
            token = token_data['access_token']
            rospy.loginfo('token success\n')
        else:
            rospy.loginfo('token failed\n')

        #self.print_data_len(self.Voice_String)

        str_voice = self.conventor(self.Voice_String)

        speech = base64.b64encode(str_voice)

        size = len(str_voice)

        RegData = {
            "format": self.FORMAT,
            "rate": self.SAMPLING_RATE,
            "channel": self.nchannel,
            "cuid": self.USER_ID,
            "token": token,
            "len": size,
            "speech": speech,
            "lan": self.LAN
        }

        HTTP_HEADER = {
            'Content-Type':
            'audio/%s;rate=%s' % (self.FORMAT, self.SAMPLING_RATE),
            'Content-length':
            str(len(json.dumps(RegData)))
        }
        #tent42 len() is output a int type , but request function need str or byte type so , add a str() func
        rospy.loginfo("%s        :: t need to see this HTTP_HEADER",
                      str(HTTP_HEADER))

        r = requests.post(
            url=self.Reg_url,
            data=json.dumps(RegData, sort_keys=True),
            headers=HTTP_HEADER)

        rospy.loginfo('response')
        self.Print_Response(r.headers)
        result = json.loads(r.text)
        self.Print_Response(result)
        rospy.loginfo('result: %s \n' % result['err_msg'])  #,type(result)
        rospy.loginfo('response\n')

        #tent42
        if result[u'err_msg'] == 'success.':
            word = result['result'][0].encode('utf-8')
            if word != '':
                if word[len(word) - 3:len(word)] == '，':
                    rospy.loginfo('cog. result:　%s \n' % word[0:len(word) - 3])
                    return word[0:len(word) - 3]
                else:
                    rospy.loginfo(word)
                    return word
            else:
                rospy.loginfo("音频文件不存在或格式错误\n")
                return '音频文件不存在或格式错误'
        else:
            rospy.loginfo(self.error_reason[result[u'err_no']])
            return self.error_reason[result[u'err_no']]

        rospy.sleep(2)

    def define(self):
        self.error_reason = {
            3300: 'x输入参数不正确',
            3301: 'x识别错误',
            3302: 'x验证失败',
            3303: 'x语音服务器后端问题',
            3304: 'x请求 GPS 过大，超过限额',
            3305: 'x产品线当前日请求数超过限额',
            3312: 'x在规定时间内没有未和robot发生语音关系'
        }

        if rospy.has_param('~REG_NUM_SAMPLES'):
            pass
        else:
            rospy.set_param('~REG_NUM_SAMPLES', 2000)

        if rospy.has_param('~REG_SAMPLING_RATE'):
            pass
        else:
            rospy.set_param('~REG_SAMPLING_RATE', 8000)

        if rospy.has_param('~REG_UPPER_LEVEL'):
            pass
        else:
            rospy.set_param('~REG_UPPER_LEVEL', 5000)

        if rospy.has_param('~REG_LOWER_LEVEL'):
            pass
        else:
            rospy.set_param('~REG_LOWER_LEVEL', 500)

        if rospy.has_param('~REG_COUNT_NUM'):
            pass
        else:
            rospy.set_param('~REG_COUNT_NUM', 20)

        if rospy.has_param('~REG_SAVE_LENGTH'):
            pass
        else:
            rospy.set_param('~REG_SAVE_LENGTH', 8)

        if rospy.has_param('~REG_TIME_OUT'):
            pass
        else:
            rospy.set_param('~REG_TIME_OUT', 60)

        if rospy.has_param('~REG_NO_WORDS'):
            pass
        else:
            rospy.set_param('~REG_NO_WORDS', 6)

        if rospy.has_param('~REG_Api_Key'):
            pass
        else:
            rospy.set_param('~REG_Api_Key', "pmUzrWcsA3Ce7RB5rSqsvQt2")

        if rospy.has_param('~REG_Secrect_Key'):
            pass
        else:
            rospy.set_param('~REG_Secrect_Key',
                            "d39ec848d016a8474c7c25e308b310c3")

        if rospy.has_param('~REG_Grant_type'):
            pass
        else:
            rospy.set_param('~REG_Grant_type', "client_credentials")

        if rospy.has_param('~REG_Token_url'):
            pass
        else:
            rospy.set_param('~REG_Token_url',
                            "https://openapi.baidu.com/oauth/2.0/token")

        if rospy.has_param('~REG_Reg_url'):
            pass
        else:
            rospy.set_param('~REG_Reg_url', "http://vop.baidu.com/server_api")

        if rospy.has_param('~REG_USER_ID'):
            pass
        else:
            rospy.set_param('~REG_USER_ID', "8168466")

        if rospy.has_param('~REG_FORMAT'):
            pass
        else:
            rospy.set_param('~REG_FORMAT', "wav")

        if rospy.has_param('~REG_LAN'):
            pass
        else:
            rospy.set_param('~REG_LAN', "zh")

        if rospy.has_param('~REG_nchannel'):
            pass
        else:
            rospy.set_param('~REG_nchannel', 1)

        self.NUM_SAMPLES = rospy.get_param(
            '~REG_NUM_SAMPLES')  # default 2000 pyaudio内置缓冲大小
        #print 'self.NUM_SAMPLES',self.NUM_SAMPLES,type(self.NUM_SAMPLES)

        self.SAMPLING_RATE = rospy.get_param(
            '~REG_SAMPLING_RATE')  # default 8000 取样频率
        #print 'self.SAMPLING_RATE',self.SAMPLING_RATE,type(self.SAMPLING_RATE)

        self.UPPER_LEVEL = rospy.get_param(
            '~REG_UPPER_LEVEL')  # default 5000 声音保存的阈值
        #print 'self.UPPER_LEVEL',self.UPPER_LEVEL,type(self.UPPER_LEVEL)

        self.LOWER_LEVEL = rospy.get_param(
            '~REG_LOWER_LEVEL')  # default 500 声音保存的阈值
        #print 'self.LOWER_LEVEL',self.LOWER_LEVEL,type(self.LOWER_LEVEL)

        self.COUNT_NUM = rospy.get_param(
            '~REG_COUNT_NUM'
        )  # default 20 NUM_SAMPLES个取样之内出现COUNT_NUM个大于LOWER_LEVEL的取样则记录声音
        #print 'self.COUNT_NUM',self.COUNT_NUM,type(self.COUNT_NUM)

        self.SAVE_LENGTH = rospy.get_param(
            '~REG_SAVE_LENGTH'
        )  # default 8 声音记录的最小长度：SAVE_LENGTH * NUM_SAMPLES 个取样
        #print 'self.SAVE_LENGTH',self.SAVE_LENGTH,type(self.SAVE_LENGTH)

        self.TIME_OUT = rospy.get_param('~REG_TIME_OUT')  # default 60 录音时间，单位s
        #print 'self.TIME_OUT',self.TIME_OUT,type(self.TIME_OUT)

        self.NO_WORDS = rospy.get_param('~REG_NO_WORDS')  # default 6
        #print 'self.NO_WORDS',self.NO_WORDS,type(self.NO_WORDS)

        self.Api_Key = rospy.get_param(
            '~REG_Api_Key')  # default "pmUzrWcsA3Ce7RB5rSqsvQt2"
        #print 'self.Api_Key',self.Api_Key,type(self.Api_Key)

        self.Secrect_Key = rospy.get_param(
            '~REG_Secrect_Key')  # default "d39ec848d016a8474c7c25e308b310c3"
        #print 'self.Secrect_Key',self.Secrect_Key,type(self.Secrect_Key)

        self.Grant_type = rospy.get_param(
            '~REG_Grant_type')  # default "client_credentials"
        #print 'self.Grant_type',self.Grant_type,type(self.Grant_type)

        self.Token_url = rospy.get_param(
            '~REG_Token_url'
        )  # default 'https://openapi.baidu.com/oauth/2.0/token'
        #print 'self.Token_url',self.Token_url,type(self.Token_url)

        self.Reg_url = rospy.get_param(
            '~REG_Reg_url')  # default 'http://vop.baidu.com/server_api'
        #print 'self.Reg_url',self.Reg_url,type(self.Reg_url)

        self.USER_ID = rospy.get_param('~REG_USER_ID')  # default '8168466'
        #print 'self.USER_ID',self.USER_ID,type(self.USER_ID)

        self.FORMAT = rospy.get_param('~REG_FORMAT')  # default 'wav'
        #print 'self.FORMAT',self.FORMAT,type(self.FORMAT)

        self.LAN = rospy.get_param('~REG_LAN')  # default 'zh'
        #print 'self.LAN',self.LAN,type(self.LAN)

        self.nchannel = rospy.get_param('~REG_nchannel')  # default 1
        #print 'self.nchannel',self.nchannel,type(self.nchannel)

        self.Voice_String = []

    #testing
    #print 'NUM_SAMPLES',type(self.nchannel)

    def Print_Response(self, data):
        for i in data:
            print ' ', i, ': ', data[i]

    def recode(self):
        pa = PyAudio()
        stream = pa.open(
            format=paInt16,
            channels=self.nchannel,
            rate=self.SAMPLING_RATE,
            input=True,
            frames_per_buffer=self.NUM_SAMPLES)
        save_count = 0
        save_buffer = []
        time_out = self.TIME_OUT
        NO_WORDS = self.NO_WORDS

        while True and NO_WORDS:
            time_out -= 1
            print 'time_out in', time_out  # 读入NUM_SAMPLES个取样
            string_audio_data = stream.read(self.NUM_SAMPLES)  # 将读入的数据转换为数组
            audio_data = np.fromstring(string_audio_data, dtype=np.short)

            # 查看是否没有语音输入
            NO_WORDS -= 1
            if np.max(audio_data) > self.UPPER_LEVEL:
                NO_WORDS = self.NO_WORDS
            print 'self.NO_WORDS ', NO_WORDS
            print 'np.max(audio_data) ', np.max(audio_data)

            # 计算大于LOWER_LEVEL的取样的个数
            large_sample_count = np.sum(audio_data > self.LOWER_LEVEL)

            # 如果个数大于COUNT_NUM，则至少保存SAVE_LENGTH个块
            if large_sample_count > self.COUNT_NUM:
                save_count = self.SAVE_LENGTH
            else:
                save_count -= 1
            print 'save_count',save_count

            # 将要保存的数据存放到save_buffer中
            if save_count < 0:
                save_count = 0
            elif save_count > 0:
                save_buffer.append(string_audio_data)
            else:
                pass

            # 将save_buffer中的数据写入WAV文件，WAV文件的文件名是保存的时刻
            if len(save_buffer) > 0 and NO_WORDS == 0:
                self.Voice_String = save_buffer
                save_buffer = []
                rospy.loginfo("Recode a piece of voice successfully!")
                #return self.Voice_String

            elif len(save_buffer) > 0 and time_out == 0:
                self.Voice_String = save_buffer
                save_buffer = []
                rospy.loginfo("Recode a piece of voice successfully!")
                #return self.Voice_String
            else:
                pass
            #rospy.loginfo( '\n\n')

    def conventor(self, Data_to_String):
        Voice_data = str()
        for Data in Data_to_String:
            Voice_data_h = array.array('b', Data)
            #print Voice_data_h
            Voice_data_h.byteswap()
            #print Voice_data_b
            Voice_data_s = Voice_data_h.tostring()
            Voice_data += Voice_data_s
        return Voice_data

    def print_data_len(self, data):
        print len(data)
        n = 0
        for i in data:
            n += 1
            print n

        ###########################################################
        ########################  testing  ########################
        ###########################################################

    def savewav(self, filename):
        rospy.loginfo('存储音频')
        file_path = '/home/turtlebot/xu_slam/src/simple_voice/src'
        WAVE_FILE = '%s/%s.wav' % (file_path, filename)
        wf = wave.open(WAVE_FILE, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(self.SAMPLING_RATE)
        wf.writeframes("".join(self.Voice_String))
        wf.close()
        rospy.loginfo('音频数据已存')


if __name__ == "__main__":
    rospy.init_node('for_hearder')
    rospy.loginfo("initialization system")
    for_hearder.run_for_hearder(for_hearder())
    rospy.loginfo("process done and quit")
