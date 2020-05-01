# -*- coding:utf-8 -*-
#!/usr/bin/env python

import subprocess
import os
import sys
import StringIO as StringIO
import codecs

CURL_PATH = "bin/curl"
CURL_MAX_TIME = 8
CURL_RANGE = r"33543139328-33752035327"
CURL_SPEED_TIME = 5
CURL_TEST_URL = r"5/795514b6-aad9-4c1c-ac2a-60c1492d7f31/0c57204f-f4f0-4bf6-b119-b7afc231994d/0.0.61375.0.6574fcb5-72f2-4c85-98c1-bd1059c79934/Destiny2_0.0.61375.0_neutral__z7wx9v9k22rmg"
CURL_HOST = "\"Host: assets1.xboxlive.com\""
CURL_WRITEOUT = "\"%{speed_download}\""

CDN_CONF_NAME = "configs/cdn.list"


def createArgv(ip_addr):
    sw = StringIO.StringIO()
    sw.write(r"-s -o nul")
    sw.write(r" -m %d"%(CURL_MAX_TIME))
    sw.write(r" -r %s"%(CURL_RANGE))
    sw.write(r" -y %d"%(CURL_SPEED_TIME))
    sw.write(r" --url http://%s/%s"%(ip_addr, CURL_TEST_URL))
    sw.write(r" -H %s"%(CURL_HOST))
    sw.write(r" -w %s"%(CURL_WRITEOUT))
    return sw.getvalue()

def subprocess_call(proc_name, argv):
    # print("%s %s"%(proc_name, argv))
    ret_code = 0
    try:
        process = subprocess.Popen("%s %s"%(proc_name , argv), shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        process.wait()
        output, unused_err = process.communicate()
        retcode = process.poll()
        ret_msg = output
    except Exception,ex :
        ret_code = 1
        ret_msg = "0"
        print(ex)
        pass
    result = ret_msg
    return (ret_code, ret_msg)

ip_dicts = {}
best_ips = []


def trim_str(line):
    line = line.replace(" ", "")
    line = line.replace("\r", "\n")
    line = line.replace("\n", "")
    return line

def main():
    cwd = os.getcwd()
    global ip_dicts
    global best_ips
    print("***************  Xbox CDN SpeedTest *****************")
    print("** Finding your best CDN for Xbox Game Downloads ****")
    urls = codecs.open(CDN_CONF_NAME, "rb", "utf-8").readlines()
    for index,line in enumerate(urls):
        if ("." in line):
            line = trim_str(line)
            ip_dicts[line] = 0
    all_count = len(ip_dicts.keys())
    cur_index = 0
    for ip_addr in ip_dicts.keys():
        cur_index += 1
        sys.stdout.write("[TEST %d/%d] [Address: %s]"%(cur_index, all_count, ip_addr))
        argv = createArgv(ip_addr)
        ret_x = subprocess_call(CURL_PATH, argv)
        spd_float = 0
        if (ret_x[0] == 0):
            spd = trim_str(ret_x[1])
            try:
                spd_float = int(float(spd) / 1024.0)
            except:
                spd_float = 0
                pass
            sys.stdout.write(" ....... %dKB/s"%(spd_float))
        else:
            sys.stdout.write(" ....... %sKB/s"%("0.0"))
            pass

        sys.stdout.write(" \n")
        ip_dicts[ip_addr] = spd_float
    best_ips = sorted(ip_dicts.items(),key=lambda x:x[1],reverse=True)
    
    print("[LOG]All CDN Test complete. Have fun!")
    if (len(best_ips) > 0):
        best_ip = best_ips[0][0]
        best_spd = best_ips[0][1]
        if (best_spd > 0):
            print("[LOG]Your Best CDN is %s, %dKB/s!"%(best_ip, best_spd))
            generate_hosts()
            generate_smartdns_configs()
            generate_dnsmasq_merlin_configs()
            generate_dnsmasq_openwrt_configs()
        else:
            print("[LOG]All CDN Failed, Bye Bye!")
    else:
        print("[LOG]All CDN Failed, Bye Bye!")
    pass

def generate_hosts():
    global best_ips
    bw = codecs.open("hosts_best_output.txt", "wb", "utf-8")
    if (len(best_ips) > 0):
        best_ip = best_ips[0][0]
        best_spd = best_ips[0][1]
        if (best_spd > 0):
            bw.write("%s %s\r\n"%(best_ip, "assets1.xboxlive.com"))
            bw.write("%s %s\r\n"%(best_ip, "assets2.xboxlive.com"))
            bw.write("%s %s\r\n"%(best_ip, "dlassets.xboxlive.com"))
    bw.close()
    pass

def generate_smartdns_configs():
    global best_ips
    bw = codecs.open("smartdns_best_output.txt", "wb", "utf-8")
    if (len(best_ips) > 0):
        best_ip = best_ips[0][0]
        best_spd = best_ips[0][1]
        if (best_spd > 0):
            bw.write("address /%s/%s\r\n"%("assets1.xboxlive.com", best_ip))
            bw.write("address /%s/%s\r\n"%("assets2.xboxlive.com", best_ip))
            bw.write("address /%s/%s\r\n"%("dlassets.xboxlive.com", best_ip))
    bw.close()
    pass

def generate_dnsmasq_merlin_configs():
    global best_ips
    bw = codecs.open("merlin_dnsmasq_best_output.txt", "wb", "utf-8")
    if (len(best_ips) > 0):
        best_ip = best_ips[0][0]
        best_spd = best_ips[0][1]
        if (best_spd > 0):
            bw.write("address=/%s/%s\r\n"%("assets1.xboxlive.com", best_ip))
            bw.write("address=/%s/%s\r\n"%("assets2.xboxlive.com", best_ip))
            bw.write("address=/%s/%s\r\n"%("dlassets.xboxlive.com", best_ip))
    bw.close()
    pass

def generate_dnsmasq_openwrt_configs():
    global best_ips
    bw = codecs.open("openwrt_dnsmasq_best_output.txt", "wb", "utf-8")
    if (len(best_ips) > 0):
        best_ip = best_ips[0][0]
        best_spd = best_ips[0][1]
        if (best_spd > 0):
            bw.write("address=/%s/%s\r\n"%("assets1.xboxlive.com", best_ip))
            bw.write("address=/%s/%s\r\n"%("assets2.xboxlive.com", best_ip))
            bw.write("address=/%s/%s\r\n"%("dlassets.xboxlive.com", best_ip))
    bw.close()
    pass

if __name__ == "__main__":
    main()
    pass
