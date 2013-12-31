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

First, clone the sources, create a fresh rpm (your rpm will have
a different name, look in the rpmbuild output) and install it:

    $ git clone https://github.com/leamas/lpf.git
    $ cd lpf/
    $ tools/make_rpm
    $ sudo rpm -U /home/al/rpmbuild/RPMS/noarch/lpf-0-2.77d58d7.fc18.noarch.rpm

Then, go to the examples/msttcore-fonts directory to create your first
lpf bootstrap package and install it:

    $ cd examples/msttcore-fonts
    $ cp License.txt msttcore-fonts-fontconfig.conf msttcore-fonts.spec \
      $(rpm --eval %_sourcedir)
    $ rpmbuild -bb lpf-msttcore-fonts.spec
    $ rpm -U --force /home/al/rpmbuild/RPMS/noarch/lpf-msttcore-fonts-2.2-1.fc18.noarch.rpm

To use lpf you need to be member of the pkg-build group. On the first run you will be prompted
about adding this group to your user. These prompts disappear after logging out and in again
(or rebooting).

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
for a password when a yum-builddep or yum install is needed

After running above, check status again

    $ lpf state
    msttcore-fonts                     OK             2.2-1


## The GUI way

An alternative way without using any CLI magic:
   - Install lpf-msttcore-fonts
   - Locate the lpf factory icon (eg g., search usng gnome3) and click on it.
     Select "Build all" and watch the package being built and installed
     after some dialogs (see screenshots)


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
   scriptlet will invoke lpf scan.
 - After running lpf scan the package is waiting for user approving the
   eula or if this is not required submitted for building directly.
 - Running lpf-approve submits packages for building after user
   accepting the eula.
 - Running lpf-build builds target package.  The lpf
   package enter state install-wait or failed.
 - Running lpf-install installs package which enter state OK.
 - After updating the lpf package , the target package will have a
   different version than the lpf package and state is untriaged
 - Likewise, the state is untriaged if target package is not installed.
 - A failed package can be rebuilt.
 - The update command is indeed a shortcut for approve-build-install.

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

Writing the lpf spec should be simple using the examples as a
starting point.  When the lpf package is installed, it will enter the
'approve-wait' state and can be handled as described under Getting
Started.

The optional CONFIG file is used to tweak how lpf builds the package.
Typical usage is in packages only built for i686 even on x86\_64 hosts.
Look into /usr/share/lpg/CONFIG for more.


## The lpf tool

The lpf command is the primary tool for handling lpf packages.
For now, here is the help (-h) output.

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
        install [package]
                    Install rpms for given package or all packages in state
                    install-wait
        log [package]
                    Display logs from last build for package, or just
                    last build.

In a desktop environment lpf will pop up various GUI windows. To make
it work as a pure cli application unset the DISPLAY environment variable.

## Notifications

There is a notifications system which can be used both from the command
line and the GUI.

At the command line, 'lpf notify' writes a message if there are lpf packages
which need to be built. It's intended to be included e. g., in .bashlogin.
Notifications can be hidden, basically blocking this message until the
package enters a new state.

In the GUI, the basic tool is the lpf-notify user daemon. This is installed
by the lpf-gui when selecting "Enable notifications" in the Notifications
menu. The daemon listens for package state changes and pops up a message
using the 'lpf notify-watch' command.

There is a locking system for the GUI notifications to avoid multiple messages
e. g., when actually updating the lpf package.

## Security, users and such

Target packages are built by a dedicated user pkg-build who owns all files
related to lpf. Users need to access some files e. g., to change state. This
is done using group permissions. See the manpage (PRIVILEGED COMMANDS) for
more.

## Tests
The test directory contains some unit tests. To work, the package to test
must be installed. BEWARE: tests remove all lpf packages on your machine!

To run the tests:

    $ tools/make_rpm
    $ sudo rpm -U --force /path/to/created/rpm
    $ cd test
    $ python -m unittest discover # [-vf]

Adding -vf stops at first failure and prints more info.


## License
This is open software licensed under the MIT license, see the LICENSE file.

## TODO

lots...
 - Dozens of bugs...
 - Sooner or later write this in a proper language (python?).
