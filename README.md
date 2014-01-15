 lpf - Local Package Factory
lpf is designed to handle two separate problems:

 - Packages built from sources which does not allow redistribution
 - Packages requiring user to accept EULA-like terms.

It works by downloading sources, possibly requiring a user to accept
license terms and then building and installing a rpm package locally.

A lpf package is really about two packages. The target packet is the
real package doing useful work. The lpf package contains what's needed
to build the target package.

The envisioned usage is that a user

 - Installs the lpf packet as normal
 - Is prompted when a update/rebuild is needed
 - When pushing the "Update" button, gets a guided tour
   handling EULA acceptance, building and installing the target package.

## Installation

First clone the sources, create a fresh rpm and install it:

    $ git clone https://github.com/leamas/lpf.git
    $ cd lpf/
    $ tools/make_rpm
    $ sudo rpm -U --force dist/lpf-*.noarch.rpm

Install the required dependencies: look into lpf.spec and install all
packages mentioned as Requires: or BuildRequires:

Then install your first lpf bootstrap package:

    $  cd examples/msttcore-fonts
    $  sudo rpm -U --force lpf-msttcore-fonts-2.2-1.fc20.noarch.rpm

To use lpf you need to be member of the pkg-build group. On the first run you will
be prompted about adding this group to your user. These prompts disappear after
logging out and in again (or rebooting).

Check that the /etc/sudodoers file contains the following line (default
in recent Fedora versions):

    #includedir /etc/sudoers.d


## Getting started

At this point, your lpf package is installed and ready to approve, build
and install the msttcore-fonts package. Check the situation using lpf state:

    $ lpf state
    msttcore-fonts                     approve-wait   2.2-1

which tells you that the package needs to be approved, built and installed.
Do that using

    $ lpf update

This will first present a dialog (text or gui) where you can read and accept
the license. Depending on your sudo configuration you might also be prompted
for a password when a yum install is needed.

After running above, check status again

    $ lpf state
    msttcore-fonts                     OK             2.2-1


## The GUI way

An alternative way without using any CLI magic:
   - Install lpf-msttcore-fonts.
   - Start the lpf-gui program (under "System Tools" or so in old-fashioned
     menus).
   - Push "Build all" and watch the package being built and installed
     after some dialogs (see screenshots).


## lpf package licecycle


                                  ------------------>-------------
    lpf package                   |                              |
    installation                  |   -------------          ----------
                 -------------    |   | approve-  | approve  | build- |
    ---->--------| untriaged |------>-| wait      |---->-----| wait   |
                 -------------  scan  -------------          ----------
                   |     |             |      |                   |
                   |     |     rebuild ^      v cancel            |
                   |     |             |      |                   |
                   |     |            ------------                |           )
             scan  ^     |            | not-     |    build       v
                   |     |  lpf pkg   | approved |    (pkg-build) |
                   |     ^  update    ------------                |
                   |     |  (root)                                |
                   |     |            -------------               |
                   |     ---------    | failed    |------<--------|
                   |             |    -------------               |
              ------------       |      |    |                    |
              | removing |       |      |    v  rebuild           v
              ------------       |      |    |                    |
                   |             |      --<---------->--------    |
    Target pkg     |             |                           |    |
    remove (root)  ^           --------                     ----------
                   |           |      |                     |install- |
                   ------------|  OK  |------------<--------|wait     |
                               |      |        install      -----------
                               --------        (root)


 - After installation an lpf package is untriaged. Normally, the %post
   scriptlet will invoke ```lpf scan```.
 - After running ```lpf scan``` the package is waiting for user approving
   the eula or if this is not required submitted for building directly.
 - Running ```lpf approve``` submits packages for building after user
   accepting the eula.
 - Running ```lpf build``` builds target package.  The lpf
   package enter state install-wait or failed.
 - Running ```lpf install``` installs package which enter state OK.
 - After updating the lpf package , the target package will have a
   different version than the lpf package and state is untriaged
 - Likewise, the state is untriaged if target package is not installed.
 - A failed package can be rebuilt.
 - The ```lpf update``` command is indeed a shortcut for
   approve-build-install.

## The lpf package
To create an lpf package you first create a target package. My example
is spotify-client. There is nothing specific about the target
package besides the fact that it cannot be in public repositories
for legal reasons. The spotify-client spec is in examples/spotify-client.

Since you cannot distribute this package you create an lpf package,
in this case lpf-spotify-client (in examples). This package is used to build
the target locally. This package contains the spec file, extra sources
such as desktop files, patches etc.,  and the eula agreement user should
accept before building. The directory structure is

    /usr/share/lpf/packages/spotify-client
                                spotify-client.spec
                                CONFIG
                                SOURCES
                                    patch-1
                                    desktop-file
                                    ...
                                eula
                                    license.txt

The optional CONFIG file is used to tweak how lpf builds the package.
Typical usage is in packages only built for i686 even on x86\_64 hosts.

Writing the lpf spec should be simple using the examples as a
starting point. There is also info the annotated lpf-pkg-example.spec file.
When doing this the internal structure as described here is handled by the
lpf-setup-package script which constructs it given a target specfile,
possible eula terms and extra sources. See comments in lpf-setup-package

When the lpf package is installed, it will enter the 'approve-wait' state
and can be handled as described under Getting Started.

## The lpf-gui tool.

lpf-gui provides a graphical interface to the basic lpf administration. Using
this one can get an overview on lpf package states, update packages, view logs,
handle notifications etc. See the first two screenshots and the lpf-gui manpage.

## The lpf tool

The lpf command is the complete tool for handling lpf packages, and also
the underpinnings for lpf-gui.  For now, here is the help (-h) output:

Usage: lpf <command> [args]

    commands:
	list 	List all packages.
	update [package]
		    Interactive approve, build and install of given package or
		    all packages.
	state [package]
		    List package state or state of all packages.
	scan [package]
		    Triage a given package or all packages  and
		    update their status.
	approve <package>
		    Approve a package in state approve-wait.
	build [package]
		    Build given package or all packages in state
		    build-wait
	rebuild <package>
		    Force re-install of a package where previous installation
		    failed.
	install <package>
		    Install rpms for given package.
	log [package]
		    Display logs from last build for package, or just
		    last build.
	mute <package>
		    Mute (i. e., disable) notification messages for given package
                    until it's state changes.

    See the manpage for more commands and other info.

In a desktop environment lpf will pop up various GUI windows (see
screenshots).  To make it work as a pure cli application unset $DISPLAY.

## Notifications

There is a notifications system which can be used both from the command
line and the GUI. A notification is created when a lpf package enters
any state besides 'OK'. It's cleared when it eventually becomes 'OK' again.

At the command line, ```lpf notify``` writes a message if there are lpf
packages which need to be built. It's intended to be included e. g., in
.bashlogin.  Notifications for a specific package can be muted, basically
blocking this message until the package enters state 'OK' using
```lpf mute```.

In the GUI, the basic tool is the lpf-notify user daemon. This is installed
by the lpf-gui when selecting "Enable notifications" in the Notifications
menu. The daemon listens for package state changes and pops up a message
using the ```lpf notify-watch``` command.

There are locks for the GUI notifications to avoid multiple messages e. g.,
when actually updating the lpf package.

## Security, users and such

Target packages are built by a dedicated user pkg-build who owns all files
related to lpf. Users need to te able to run as pkg-build and also as root
to install target packages. See the lpf manpage (PRIVILEGED COMMANDS) for
more.

## Tests

The test directory contains some unit tests. To work, the package to test
must be installed. BEWARE: tests remove all lpf packages on your machine!
See TESTING for more.

## License
This is open software licensed under the MIT license, see the LICENSE file.

## TODO

lots...
 - Dozens of bugs...
 - python3 port.
 - Rewrite the notitification code with a proper daemon and using the
   notification interface - i. e., using python.
 - Sooner or later write this in a proper language (python?).
