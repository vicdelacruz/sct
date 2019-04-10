#!/bin/bash
if [ `ps -ef |grep -E 'sshfs.*ngsct.*receive' |grep nonempty |wc -l` = 0 ]; then
    if [ ! -d "/root/ngsct/send" ]; then
        mkdir /root/ngsct/send
    fi
    echo 'amd' | sshfs AMD@192.168.0.100:'D:\\SCT\send' /root/ngsct/receive -o password_stdin -o nonempty
fi
    
if [ `ps -ef |grep -E 'sshfs.*ngsct.*sct' |grep nonempty  |wc -l` = 0 ]; then
    if [ ! -d "/root/ngsct/sct" ]; then
        mkdir /root/ngsct/sct
    fi
    echo 'amd' | sshfs AMD@192.168.0.100:'D:\\SCT\program' /root/ngsct/sct -o password_stdin -o nonempty
fi
    
if [ `ps -ef |grep -E 'sshfs.*ngsct.*send' |grep nonempty  |wc -l` = 0 ]; then
    if [ ! -d "/root/ngsct/receive" ]; then
        mkdir /root/ngsct/receive
    fi
    echo 'amd' | sshfs AMD@192.168.0.100:'D:\\SCT\receive' /root/ngsct/send -o password_stdin -o nonempty
fi

sleep 10

if [ `ps -ef |grep sct |grep python3 |wc -l` = 0 ]; then
    cd /root/ngsct/sct/
    python3 sct/main.py &
fi
