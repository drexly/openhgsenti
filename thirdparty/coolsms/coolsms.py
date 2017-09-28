# -*- coding: utf8 -*-

"""
 vi:set et ts=4 enc=utf8 fenc=utf8:
 Copyright (C) 2008-2010 D&SOFT
 http://open.coolsms.co.kr
"""

__version__ = "2.3.1"


import sys
import string
import socket
import time
import random
import os

#- python version compatible 
if sys.version_info[1] < 6:
    import md5
else:
    import hashlib


try:
    True
except NameError:
    False = 0
    True = not False


class mysock:
    def __init__(self, sock=None):
        self.TIMEOUT_SECONDS = 5
        if sock == None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

        self.sock.settimeout(self.TIMEOUT_SECONDS)

    def connect(self, host_port):
        try:
            ret = self.sock.connect_ex(host_port)
            self.file = self.sock.makefile("rb")
            return ret
        except:
            return -1

    def send(self, data):
        datalen = len(data)
        totalsent = 0
        while totalsent < datalen:
            sent = self.sock.send(data[totalsent:])
            if sent == 0:
                raise (RuntimeError, "socket connection broken")
            totalsent = totalsent + sent

    def recv(self, datalen):
        data = ""
        while len(data) < datalen:
            chunk = self.sock.recv(datalen-len(data))
            if chunk == "":
                raise (RuntimeError, "socket connection broken")
            data = data + chunk
        return data

    def readline(self):
        CRLF = "\r\n"
        s = self.file.readline()
        if not s:
            raise EOFError
        if s[-2:] == CRLF:
            s = s[:-2]
        elif s[-1:] in CRLF:
            s = s[:-1]
        return s

    def close(self):
        self.sock.close()


class sms:
    def __init__(self, bdebug = False):
        self.hosts = ["alpha.coolsms.co.kr", "bravo.coolsms.co.kr", "delta.coolsms.co.kr"]
        self.port = 80
        self._charset = "euckr"
        self.module_version = "python/2.2"
        self.app_version = ""

        self.version = "TBSP/1.0"
        self.connected = False
        self.userid = ""
        self.passwd = ""
        self.crypt = "MD5"
        self.msgque = []
        self.result = []
        self.sock = False
        self.bdebug = bdebug

    def validate_attachment(self, the_filename):
        if os.path.exists(the_filename):
            if os.path.getsize(the_filename) <= 204800:
                if os.path.splitext(the_filename)[1] == ".jpg":
                    return True
                else:
                    #return False
                    raise (TypeError, "This file is not a jpg file: '%s'" % the_filename)
            else:
                #return False
                raise (ValueError, "File size to les than a 200Kbyte: '%s'" % the_filename)
        else:
            raise (IOError, "No such file or directory: '%s'" % the_filename)

    def is_connected(self):
        if self.sock == False:
            return False
        return True

    def debug(self, debugstr):
        if self.bdebug == True:
            print (debugstr)

    def __connect__(self, host, port):
        connected = False

        self.sock = mysock()
        if self.sock.connect((host, port)) == 0:
            self.debug("connected to %s:%u" % (host, port))
            connected = True
        else:
            self.debug("connect error to %s:%u" % (host, port))

        return connected

    def connect(self):
        connected = False

        for host in self.hosts:
            connected = self.__connect__(host, self.port)
            if connected == True:
                break
        return connected

    def disconnect(self):
        if self.sock != False:
            self.sock.close()

    def setuser(self, userid, passwd):
        self.userid = userid
        self.passwd = passwd

    def setattachdir(self, attachment_dir=""):
        if attachment_dir:
            if os.path.exists(attachment_dir):
                self.attachment_dir = attachment_dir
                return True
            else:
                raise (IOError, "No such file or directory: '%s'" % attachment_dir)
        else:
            self.attachment_dir = os.getcwd()
            return True

    def setcrypt(self, crypt="MD5"):
        self.crypt = crypt

    def charset(self, _charset="euckr"):
        self._charset = _charset

    def appversion(self, version):
        self.app_version = version

    def emptyall(self):
        del self.msgque[:]
        del self.result[:]

    def emptymsgque(self):
        del self.msgque[:]

    def add(self, callno, callback, msg, name="", date="", msgid="", grpid="", type="SMS",
            subject="", attachment=""):

        if type == "MMS":
            if not self.validate_attachment(self.attachment_dir+os.sep+attachment):
                return False

        self.msgque.append({ 
                "callno" : callno
                , "callback" : callback
                , "msg" : msg
                , "name" : name
                , "date" : date
                , "msgid" : msgid
                , "grpid" : grpid
                , "type" : type
                , "subject" : subject
                , "attachment" : attachment
            })
        return True

    def addsms(self, callno, callback, msg, date="", msgid="", grpid="", name=""):
        self.add(callno, callback, msg, name, date, msgid, grpid, "SMS")

    def addlms(self, callno, callback, subject, msg, date="", msgid="", grpid="", name=""):
        self.add(callno, callback, msg, name, date, msgid, grpid, "LMS", subject)

    def addmms(self, callno, callback, subject, msg, attachment,
                date="", msgid="", grpid="", name=""):
        if self.add(callno, callback, msg, name, date,
            msgid, grpid, "MMS", subject, attachment):
            return True
        else:
            return False

    def count(self):
        return len(self.msgque)

    def md5(self, str):
        if sys.version_info[1] < 6:
            #- ptyon version 2.6.X under
            hash = md5.new()
        else:
            #- ptyon version 2.6.X upper
            hash = hashlib.md5()

        hash.update(str)
        return string.join(map(lambda v: "%02x" % ord(v), hash.digest()), "")

    def keygen(self):
        microsecond = "%f" % (time.time())
        randnum = "%u" % (random.randint(100000,999999))
        return time.strftime("%Y%m%d%H%M%S", time.localtime(time.time())) + microsecond[-6:] + randnum

    def send(self):

        if self.is_connected() == False:
            self.debug("not connected.")
            return

        count = 0
        for i in range(len(self.msgque)):
            x = self.msgque[i]
            msg = {}

            msg["VERSION"] = self.version
            msg["MODULE-VERSION"] = self.module_version

            if len(self.app_version) > 0:
                msg["APP-VERSION"] = self.app_version   

            msg["COMMAND"] = "SEND"

            if len(self._charset) > 0:
                msg["CHARSET"] = self._charset

            msg["TYPE"] = x["type"]

            if len(x["subject"]) > 0:
                msg["SUBJECT"] = x["subject"]

            msg["MESSAGE"] = x["msg"]

            if len(x["attachment"]) > 0:
                msg["ATTACHMENT"] = x["attachment"]

            if len(x["msgid"]) != 0:
                msg["MESSAGE-ID"] = x["msgid"]

            if x["grpid"]:
                msg["GROUP-ID"] = x["grpid"]
        
            msg["CALLED-NUMBER"] = x["callno"]
            msg["CALLING-NUMBER"] = x["callback"]

            if len(x["name"]) != 0:
                msg["CALLED-NAME"] = x["name"]

            if len(x["date"]) != 0:
                msg["RESERVE-DATE"] = x["date"]

            if self.crypt == "MD5":
                msg["CRYPT-METHOD"] = "MD5"
                passwd = self.md5(self.passwd)
            else:
                passwd = self.passwd

            msg["AUTH-ID"] = self.userid
            msg["AUTH-PASS"] = passwd
            msg["LANGUAGE"] = "PYTHON-" + string.split(sys.version, " ")[0]

            if x["type"] == "MMS":
                cscpstr = cscp_build(tbsp_build(msg), self.attachment_dir, x["attachment"])
            else:
                cscpstr = cscp_build(tbsp_build(msg))

            self.sock.send(cscpstr)

            result = cscp_parse(self.sock)
            ack = tbsp_parse(result["TBSP"])

            self.result.append(ack)
            count = count + 1

        self.emptymsgque()

        return count


    def credits(self):
        return remain()

    def remain(self):
        if self.is_connected() == False:
            self.debug("not connected.")
            return

        msg = {}

        msg["VERSION"] = self.version
        msg["MODULE-VERSION"] = self.module_version
        if len(self.app_version) > 0:
            msg["APP-VERSION"] = self.app_version   
        msg["COMMAND"] = "CHECK-CREDITS"
        if self.crypt == "MD5":
            msg["CRYPT-METHOD"] = "MD5"
            passwd = self.md5(self.passwd)
        else:
            passwd = self.passwd
        msg["AUTH-ID"] = self.userid
        msg["AUTH-PASS"] = passwd
        msg["LANGUAGE"] = "PYTHON-" + string.split(sys.version, " ")[0]

        cscpstr = cscp_build(tbsp_build(msg))

        self.sock.send(cscpstr)

        result = cscp_parse(self.sock)
        ack = tbsp_parse(result["TBSP"])

        return ack

    def rcheck(self, msgid):
        if self.is_connected() == False:
            self.debug("not connected.")
            return

        msg = {}

        msg["VERSION"] = self.version
        msg["MODULE-VERSION"] = self.module_version

        if len(self.app_version) > 0:
            msg["APP-VERSION"] = self.app_version   

        msg["COMMAND"] = "CHECK-RESULT"

        if self.crypt == "MD5":
            msg["CRYPT-METHOD"] = "MD5"
            passwd = self.md5(self.passwd)
        else:
            passwd = self.passwd
        msg["AUTH-ID"] = self.userid
        msg["AUTH-PASS"] = passwd
        msg["MESSAGE-ID"] = msgid
        msg["LANGUAGE"] = "PYTHON-" + string.split(sys.version, " ")[0]

        cscpstr = cscp_build(tbsp_build(msg))

        self.sock.send(cscpstr)

        result = cscp_parse(self.sock)
        ack = tbsp_parse(result["TBSP"])

        return ack

    def cancel(self, msgid):
        if self.is_connected() == False:
            self.debug("not connected.")
            return

        msg = {}

        msg["VERSION"] = self.version
        msg["MODULE-VERSION"] = self.module_version
        if len(self.app_version) > 0:
            msg["APP-VERSION"] = self.app_version   
        msg["COMMAND"] = "CANCEL"
        if self.crypt == "MD5":
            msg["CRYPT-METHOD"] = "MD5"
            passwd = self.md5(self.passwd)
        else:
            passwd = self.passwd
        msg["AUTH-ID"] = self.userid
        msg["AUTH-PASS"] = passwd
        msg["MESSAGE-ID"] = msgid
        msg["LANGUAGE"] = "PYTHON-" + string.split(sys.version, " ")[0]

        cscpstr = cscp_build(tbsp_build(msg))

        self.sock.send(cscpstr)

        result = cscp_parse(self.sock)
        ack = tbsp_parse(result["TBSP"])

        return ack

    def groupcancel(self, gid):
        if self.is_connected() == False:
            self.debug("not connected.")
            return

        msg = {}

        msg["VERSION"] = self.version
        msg["MODULE-VERSION"] = self.module_version
        if len(self.app_version) > 0:
            msg["APP-VERSION"] = self.app_version   
        msg["COMMAND"] = "GROUP-CANCEL"
        if self.crypt == "MD5":
            msg["CRYPT-METHOD"] = "MD5"
            passwd = self.md5(self.passwd)
        else:
            passwd = self.passwd
        msg["AUTH-ID"] = self.userid
        msg["AUTH-PASS"] = passwd
        msg["GROUP-ID"] = gid
        msg["LANGUAGE"] = "PYTHON-" + string.split(sys.version, " ")[0]

        cscpstr = cscp_build(tbsp_build(msg))

        self.sock.send(cscpstr)

        result = cscp_parse(self.sock)
        ack = tbsp_parse(result["TBSP"])

        return ack

    def getr(self):
        return self.result

    def printr(self):
        for i in range(len(self.result)):
            x = self.result[i]

            print ("Called Number: " + x["CALLED-NUMBER"])
            print ("Message ID: " + x["MESSAGE-ID"])
            print ("GROUP-ID: " + x["GROUP-ID"])
            print ("Result Code: " + x["RESULT-CODE"])
            print ("Result Message: " + x["RESULT-MESSAGE"])


def tbsp_parse(tbspstr):
    tbsparr = string.split(tbspstr, "\n")
    property = {}

    for line in tbsparr:
        element = string.split(line, ":")
        if len(element) < 2:
            continue
        name = element[0]
        value = element[1]

        if name == "MESSAGE":
            if property.has_key(name):
                property[name] = property[name] + "\n" + value
            else:
                property[name] = value
        else:
            property[name] = value
    return property

def tbsp_build(tbsp):
    tbspstr = ""

    for key in tbsp.keys():
        if key == "MESSAGE":
            msgarr = string.split(tbsp[key], "\n")
            for line in msgarr:
                tbspstr = tbspstr + key + ":" + line + "\n"
        else:
            tbspstr = tbspstr + key + ":" + tbsp[key] + "\n"
    return tbspstr

def cscp_parse(sock):
    CSCP_VERSION_SIZE = 7
    CSCP_BODYLEN_SIZE = 8
    CSCP_PARAID_SIZE = 2
    CSCP_PARABODYLEN_SIZE = 8

    cscp_rcv = {}
    cscp_rcv["VERSION"] = sock.recv(CSCP_VERSION_SIZE)
    cscp_rcv["BODYLEN"] = sock.recv(CSCP_BODYLEN_SIZE)
    cscp_rcv["PARAID"] = sock.recv(CSCP_PARAID_SIZE)
    cscp_rcv["PARABODYLEN"] = sock.recv(CSCP_PARABODYLEN_SIZE)

    bodylen = int(cscp_rcv["PARABODYLEN"])
    cscp_rcv["TBSP"] = sock.recv(bodylen)

    return cscp_rcv

def cscp_read(sock):
    CSCP_VERSION_SIZE = 7
    CSCP_BODYLEN_SIZE = 8

    version = sock.recv(CSCP_VERSION_SIZE)
    bodylen = sock.recv(CSCP_BODYLEN_SIZE)
    bodylen = int(bodylen)
    
    if bodylen > 0:
        body = sock.recv(bodylen)

    return body

def cscp_build(cscpstr, attach_dir="", attach_file=""):
    capsule = "CSCP2.0"

    if attach_file:
        attachment = read_attachfile(attach_dir, attach_file) 

        #- body total length
        capsule += "%8d" % (20+len(cscpstr)+len(attachment))

        capsule += "ME"
        capsule += "%8d" % len(cscpstr)
        capsule += cscpstr

        capsule += "AT"
        capsule += "%8d" % len(attachment)
        capsule += attachment

    else:
        #- body total length
        capsule += "%8d" % (10+len(cscpstr))

        capsule += "ME"
        capsule += "%8d" % len(cscpstr)
        capsule += cscpstr

    return capsule

def read_attachfile(the_dir, the_file):
    file_length = "%3d" % len(the_file)
    f = file(the_dir+os.sep+the_file, "rb")
    file_image = f.read()
    f.close()

    return file_length+the_file+file_image

#-- END
