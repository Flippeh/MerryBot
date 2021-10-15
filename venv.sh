#!/bin/bash
# venv.sh
# Installs Python 3.10.0 and creates a venv if there is not one already.
#
# TODO:
# - [ ] add option for args to customize script (i.e. venv_name, python_ver, setup, packages)
# - [ ] configure venv with setup.py

version=$(python3 -c 'import sys; print(sys.version_info[:])')
version_att2=$(python3.10 -c 'import sys; print(sys.version_info[:])')
pattern="(3, 10, 0, 'final', *)"

if [[ $version =~ $pattern ]]
then
	echo "Python 3.10.0 already installed."
else
	if [[ $version_att2 =~ $pattern ]]
	then
		echo "Python 3.10.0 already installed."	
	else
		if [[ ! -e "Python-3.10.0.tar.xz" ]]
		then
			wget https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tar.xz
		else 
			echo "'Python-3.10.0.tar.xz' already exist."
		fi

		{ # try
			tar -xvf Python-3.10.0.tar.xz
		} || { #catch
			echo "There was an error completing the unzip process. see above for an error."
			exit 1
		}
		cd Python-3.10.0
		./configure --enable-optimizations
		sudo make altinstall 
		cd ..
		echo "Install finished."
		echo "Cleaning directory..."
		rm -rf Python-3.10.0
	fi
fi

if [[ ! -d "./venv" ]]
then
	echo "3.10.0 venv doesnt exist. Creating..."
	python3.10 -m venv venv
	echo "Done creating venv."
	echo "Configuring venv..."
	source venv/bin/activate
	pip install -r requirements.txt
	deactivate
	echo "Done configuring venv."
else
	echo "3.10.0 venv already exist."
fi
echo "Run '$ source venv/bin/activate'"
