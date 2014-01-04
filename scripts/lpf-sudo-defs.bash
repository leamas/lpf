#
# Common code sourced by scripts running as root - be careful.
#

if (( UID == 0 )); then
    SUDO=''
elif [ "$DISPLAY" ]; then
    SUDO='sudo -A'
else
    SUDO='sudo'
fi

function has_meta()
# Return True if args contains a shell meta character, including space.
{
    local metachars='&;|~<>^()[]{}'
    local word="$*"
    word=${word/\ /|}
    word=${word/\`/|}
    word=${word/\'/|}
    word=${word/\"/|}
    word=${word/\*/|}
    word=${word/\?/|}
    word=${word/\[/|}
    word=${word/\$/|}
    for (( i = 0; i < ${#metachars}; i += 1 )); do
        if [[ "$word" == *${metachars:$i:1}* ]]; then
            return 0
        fi
    done
    return 1
}


# vim: set expandtab ts=4 sw=4:
