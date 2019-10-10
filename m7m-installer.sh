#!/bin/sh


ulang="y"
while [ $ulang = "y" ]
do
  clear
  echo "\033[1;31m#     # ####### #     #    #     #"
  echo "##   ## #    #  ##   ##    ##   ## # #    # ###### #####"
  echo "# # # #     #   # # # #    # # # # # ##   # #      #    #"
  echo "#  #  #    #    #  #  #    #  #  # # # #  # #####  #    #"
  echo "#     #   #     #     #    #     # # #  # # #      #####"
  echo "#     #   #     #     #    #     # # #   ## #      #   #"
  echo "#     #   #     #     #    #     # # #    # ###### #    #"
  echo "            \033[1;32m  M7M Cpu Miner Installer\n\n"
  echo -n "Do Tou Want To Continue (Y/N) : "
  read pil;
  if [ $pil = "y" ]||[ $pil = "Y" ]
  then
      echo "Installing Starting....!"
      apt-get update && apt-get upgrade -y
      apt-get install git build-essential cmake libuv1-dev libmicrohttpd-dev libssl-dev -y
      apt-get install -qqy automake
      apt-get install -qqy libcurl4-openssl-dev
      apt-get install -qqy make
      git clone https://github.com/magi-project/wolf-m7m-cpuminer-V2.git
      cd wolf-m7m-cpuminer-V2
      ./autogen.sh
      ./configure CFLAGS="-O3"
      make
      echo "Installing Finish"
      exit
  elif [ $pil = "n" ]||[ $pil = "N" ]
  then
      echo "\033[1;31mBye Bye.....!"
      sleep 2
      exit
  else
     echo "\033[1;31mERROr : Wrong Input....!"
     sleep 2
  fi
done