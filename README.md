ClamIt
======

Simple commandline utility script to make [ClamAV](http://clamav.net) antivirus software for Linux-based mailservers easier to use
from a LiveCD or USB drive. Intended for Windows OS virus removal.

Installation
------------

Boot the target computer to a Linux LiveCD (or better yet, Ubuntu-based persisent USB). 

Install 'git', clone 'clamit' from GitHub, and make the shell script executable:

    $ git clone https://github.com/joseph8th/clamit
    $ cd clamit
    $ sudo chmod 0755 clamit
    
You can use ClamIt to install ClamAV if you use either `aptitude` (Debian, Ubuntu, etc.), or `pacman` (Arch)
package managers, as follows (otherwise install `clamav` using your package manager or from source):

    $ ./clamit get [apt | pac]
    
Usage
-----

    $ ./clamit {get [apt | pac], fresh, scan, clean}

Commands
--------

    -h, --help        print a help screen

    get [apt | pac]   install 'clamav' package using either `aptitude` or `pacman`

    fresh             update virus definitions

    scan              mount and scan chosen device and all its partitions; generates a `clam.log` file

    clean             process the log file generated by `scan` command (remove, quarantine or ignore)

Tips for Windoze LUsers
-----------------------

I wrote this script for my employer, an old-school Windoze man who has been fairly amazed at the way I use Linux to cure
many of our clients' more serious infections, but didn't want to learn everything you need to know to use ClamAV. 

You will have to figure out how to: (a) make a Linux LiveCD/USB, and (b) open a terminal (`cmd.exe` on steroids). 
After that you can just use the installation instructions.

When you use the `scan` command, ClamIt will list all the available drives, and ask which *device* you want to use.
These are listed in *Linux* format: `/dev/sdX`, where 'X' is a letter 'a-z'. If the machine you booted has only one
drive, this will always be `/dev/sda`. If it has two, the second one will be `/dev/sdb`, etc. If the machine has any
card readers, these will be listed also, so some machines may have a lot of devices.

(If you doubt which device to scan, you can quit the program at any time by typing `^-C`. Then run the `lsblk` command
to get a tree view of all block devices connected to the machine, as well as all their partitions with sizes, filesystem
types, and even mountpoints. This is enough info to determine which is the correct device to choose.)

ClamIt will then mount all primary partitions of the chosen device in a single tree under `/mnt/clamit` and recursively
scan the data for viruses *including all Windows system files*. It tells ClamAV to store a log file containing the 
locations of all the infected files at the top of this tree. 

Then, when you run `clean`, it processes this log and asks if you want to remove, quarantine, or ignore each infected 
file. If you quarantine a file, ClamIt moves the infected files into a `clam-quarantine` directory in the root of the 
*target* machine's filesystem (i.e., 'C:\clam-quarantine'). If you want to restore the file, you will have to do so 
manually, as this feature has not yet been added to ClamIt.
