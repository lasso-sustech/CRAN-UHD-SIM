
all:depends

depends:
	sudo apt install python3-uhd linux-cpupower -y
	pip3 install --user numpy matplotlib

test:
	sudo cpupower monitor -c ""