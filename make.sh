#!/bin/bash
#配置读取的log的路径
readLogFullPath="/tmp/php/"
#配置脚本安装路径
appInstallDir="/home/yangyanxin/workspace"

appCronPath="/etc/cron.d/"
installAppName="mapping_roomid"
installFullPath=$appInstallDir"/"$installAppName
logFullPath=$installFullPath"/log"
reqAddrUrl="http://54.222.218.126/ping2/suntian/display_roomid_hd_onl.php?"


if [ $# -lt 1 ]
then
    echo "usage: make install|uninstall|cleanlog"
    exit 1
fi

appMakeCommand=$1
if [ $appMakeCommand != "install" ] && [ $appMakeCommand != "uninstall" ] && [ $appMakeCommand != "cleanlog" && [ $appMakeCommand != "start" ]
then
    echo $appMakeCommand
    exit 1
fi

if [ $appMakeCommand == "install" ]
then
    if [ -d $installFullPath ]
    then
        echo " use exiting $installFullPath"
        sleep 1
    else
        mkdir -p $installFullPath
    fi

    echo "begin copy workdir"
    cp -rf ./mapping_roomid.py $installFullPath

    echo "begin mkdir log"
    if [ ! -d $logFullPath ]
    then
        echo "make dir for log path"
        mkdir -p $logFullPath
    fi
	
    cat ./mapping_roomid.cron|awk '{gsub("__INSTALL_DIR__","'$installFullPath'",$0);gsub("__READ_LOG_FULL_PATH__","'$readLogFullPath'",$0);gsub("__Reqaddr__","'$reqAddrUrl'",$0);print $0;}' > $appCronPath"mapping_roomid"
    sleep 1
    echo "done"
    exit 0
fi


if [ $appMakeCommand == "uninstall" ]
then
    rm -rf $installFullPath $appCronPath"mapping_roomid"
    echo "done"
fi

if [ $appMakeCommand == "cleanlog" ]
then
    if [ ! -d $logFullPath ]
    then 
        echo "log path not exist"
        exit 0
    fi
    echo $logFullPath"/" 
    rm -rf $logFullPath

    echo "clean log"
fi

if [ $appMakeCommand == "start" ]
then
    cd $installFullPath
    python mapping_roomid.py $readLogFullPath $reqAddrUrl
    echo "done"
fi
