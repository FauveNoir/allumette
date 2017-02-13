#!/bin/zsh

echo "This is OpenAllumette installator\n\n"


DISTRIBUTION=`lsb_release -i | sed 's/Distributor ID:\t//'`

case $DISTRIBUTION in
	"Debian")
		echo "* Installing all dependencies"
		sudo aptitude install python3 mercurial python3-dev python3-numpy libsdl-dev libsdl-image1.2-dev \
		  libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev libportmidi-dev \
		  libavformat-dev libswscale-dev libjpeg-dev libfreetype6-dev git

		echo "* Installing python3-pygame"
		cd /tmp/
		hg clone https://bitbucket.org/pygame/pygame
		cd pygame

		echo "Bulid pygame and install it"
		python3 setup.py build
		sudo python3 setup.py install

		echo "OpenAllumette installation"
		git clone github.com/FauveNoir/allumette.git ~/.allumette
		ln -s ~/.allumette/nim.py ~/.local/bin/allumette

		echo "\n\nYou can now run OpenAllumette with the command allumette. Good game."
	;;
	*)
		echo "There is not yet installation for your distribution.\nMaybe are you a volunteer to do it? :)
	;;
esac
