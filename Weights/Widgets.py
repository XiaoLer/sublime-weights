#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-08-25
# @Author  : Scholer (scholer.liu@haoqitech.com.cn)
# @Link    :
# @Version : 0.1

# sublime plugin packages
import sublime
import sublime_plugin

# import os
# import sys
import hashlib
import time
import urllib.parse

class EncodingBase(sublime_plugin.TextCommand):

    def timeFormat(self,string):
        if string.isdigit():
            timeArray = time.localtime(int(string))
            return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        else :
            try:
                if len(string) < 11:
                    timeArray = time.strptime(string, "%Y-%m-%d")
                else :
                    timeArray = time.strptime(string, "%Y-%m-%d %H:%M:%S")
            except (ValueError):
                return sublime.message_dialog('[Warning] time data ' + string + ' does not match format.')
            return str(int(time.mktime(timeArray)))

    def urlTrans(self,string):
        if string.find('%') >= 0:
            return urllib.parse.unquote(string)
        else:
            return urllib.parse.quote(string,"-._")

    def encode(self,type,string):
        if not string:
            return
        if type == "md5":
            return hashlib.md5(string.encode("utf8")).hexdigest()
        elif type == "timeformat":
            return self.timeFormat(string)
        elif type == "urltrans":
            return self.urlTrans(string)

    def encodeCommand(self,type,edit):
        for region in self.view.sel():
            if not region.empty():
                selection = self.view.substr(region)
                self.view.replace(edit, region, self.encode(type,selection))

# md5 encode
class Md5EncodingCommand(EncodingBase):
    def run(self,edit):
        self.encodeCommand("md5",edit)

# time format transition
class TimeFormatCommand(EncodingBase):
    def run(self,edit):
        self.encodeCommand("timeformat",edit)

# URL encode/decode
class UrlTransCommand(EncodingBase):
    def run(self,edit):
        self.encodeCommand("urltrans",edit)

# insert unix time
class InsertUinxTimeCommand(sublime_plugin.TextCommand):
    def run(self,edit):
        postion = self.view.sel()[0].begin()
        self.view.insert(edit, postion, str(int(time.time())))

# insert locale date
class InsertDateCommand(sublime_plugin.TextCommand):
    def run(self,edit):
        now = int(time.time())
        timeArray = time.localtime(now)
        postion = self.view.sel()[0].begin()
        self.view.insert(edit, postion, time.strftime("%Y-%m-%d %H:%M:%S", timeArray))

# copy line of selected region to new flie
class PointLineToNewFileCommand(sublime_plugin.TextCommand):
    def run(self,edit):
        allRegion = []
        for region in self.view.sel():
            allRegion.append(self.view.substr(self.view.full_line(region.begin())))
        win = self.view.window()
        tab = win.new_file()
        row = 0
        for string in allRegion:
            postion = tab.text_point(row,0)
            tab.insert(edit,postion,string)
            row+=1

# this will be called when the API is ready to use
def plugin_loaded():
    pass