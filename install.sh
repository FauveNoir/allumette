#!/bin/zsh

echo "This is OpenAllumette installator\n\n"


DISTRIBUTION=`lsb_release -i | sed 's/Distributor ID:\t//'`

case $DISTRIBUTION in
	"Debian")
		echo "* Installing all needed packages"
		sudo aptitude install git python3 python3-pip

		echo "* Installing Pygame with Pip"
		pip3 install Pygame

		echo "Downloading and inpacking OpenAllumette"
		git clone github.com/FauveNoir/allumette.git ~/.allumette
		ln -s ~/.allumette/nim.py ~/.local/bin/allumette

		echo "\n\nYou can now run OpenAllumette with the command allumette. Good game."
	;;
	*)
		echo "There is not yet installation for your distribution.\nMaybe are you a volunteer to do it? :)"
	;;
esac
