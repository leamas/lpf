#
# Common code sourced by other scripts
#

scriptdir=$( dirname $(readlink -fn $0))

LPF_VAR=${LPF_VAR:-/var/lib/lpf}
LPF_DATA=${LPF_DATA:-/usr/share/lpf}

# test hooks
[ -e $scriptdir/var ] && export LPF_VAR=$scriptdir/var/lib/lpf
[ -e $scriptdir/usr ] && export LPF_DATA=$scriptdir/usr/share/lpf

PKG_DATA_DIR="$LPF_DATA/packages"
LPF_USER='pkg-build'
LPF_GROUP='pkg-build'

if (( UID == 0 )); then
    SUDO=''
else
    SUDO='sudo'
    [ -n "$DISPLAY" ] && SUDO='sudo -A'
fi

function get_logfile()      { echo $LPF_VAR/log/$1.log; }
function get_approve_file() { echo $LPF_VAR/approvals/$1; }
function get_resultdir()    { echo $LPF_VAR/rpms/$1; }
function get_pkg_srcdir()   { echo $LPF_DATA/packages/$1/SOURCES; }
function get_eula_dir()     { echo $LPF_DATA/packages/$1/eula; }
function get_spec()         { echo $LPF_DATA/packages/$1/$1.spec; }
function _get_statefile()   { echo $LPF_VAR/packages/$1/state; }


function _message()
{
    local kind=$1; shift
    if [[ -n "$DISPLAY"  && -z "$LPF_UPDATE" ]]; then
        zenity --$kind --title="lpf: $1" --text "$*"
    else
        echo "$title${1:+:} $*"
    fi
}


function info()     { _message 'info'    "$@"; }
function warning()  { _message 'warning' "$@"; }
function error()    { _message 'error'   "$@"; }


function need_approve_file()
# True if pkg arg needs to be approved
{
    [ -n "$( find $(get_eula_dir $1) -type f)" ]
}


function get_state()
# get_state pkg - return state for given package
{
    [ -e $LPF_VAR/packages/$1 ] ||
        mkdir -p  $LPF_VAR/packages/$1
    cat "$(_get_statefile $1)"  2>/dev/null  || echo 'untriaged'
}




function get_pkg_version()
# get_pkg_version pkg - return version of lpf version
{
    local pkg=$1
    local spec=$PKG_DATA_DIR/$pkg/$pkg.spec
    rpm --specfile $spec -q --qf "%{VERSION}-%{RELEASE}\n" 2>/dev/null | head -1
}


function list_states()
# list_states - formatted list of pkg, state, version.
{
    local pkgdir
    for pkgdir in $( get_arg_pkgdirs "$@" ); do
        local pkg=${pkgdir##*/}
        local state=$( get_state $pkg )
        local spec=$pkgdir/$pkg.spec
        local version=$(get_pkg_version $pkg )
        printf '%-35s%-15s%-20s\n' $pkg $state $version
    done
}


function get_pkgdirs()
# get_pkgdirs - return list of all package directories.
{
     find $PKG_DATA_DIR -maxdepth 1 -mindepth 1 -type d 2>/dev/null
}


function install_rpms()
# install_rpms [rpm file...]: install command.
{
    $scriptdir/lpf-install "$@"
}


function approve_package()
# approve_package <package>: approve command.
{
    $scriptdir/lpf-approve "$@"
}

function scan_packages()
# scan_packages - state command.
{
    $SUDO -u $LPF_USER $scriptdir/lpf-scan "$@"
}


function get_arg_pkgdirs()
# get_arg_pkgdirs [pkg] - return either one existing pkg dir or
# list of all package dirs.
{
    if [ -n "$1" ]; then
        if [ -e $PKG_DATA_DIR/$1 ]; then
            echo $PKG_DATA_DIR/$1
        else
            echo "No such package: \"$1\"" >&2
            exit 2
        fi
    else
        get_pkgdirs
    fi
}


function show_buildlog()
# buildlog command
{
    if [ -n "$1" ]; then
        local pkg=$1
        local logfile=$( get_logfile $pkg )
    else
        local logfile=$( ls -t  $LPF_VAR/log | head -1 )
        logfile=$LPF_VAR/log/$logfile
    fi
    if [ ! -e "$logfile" ]; then
        info "Buildlog error" "No buildlog found" >&2
        exit 3
    elif [ -n "$DISPLAY" ]; then
        zenity --text-info --filename="$logfile" \
            --width 600 --height 500 --title="$( basename $logfile )"
    else
        cat $logfile
    fi
}

function do_trap()
# Handle standard traps: kill all processes in group.
{
    rc=${1:-80}
    trap '' EXIT ERR SIGINT
    $scriptdir/lpf-kill-pgroup
    exit $rc
}

