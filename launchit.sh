#!/usr/bin/env bash

source ~/.config/clamitrc

GTERM_CONF=gnome-terminal-conf.xml
GTERM_CONF_BAK=${CLAMIT_TMP}/${GTERM_CONF}


function set_terminal {
    [ ! -f "$GTERM_CONF_BAK" ] && \
	gconftool-2 --dump '/apps/gnome-terminal' > $GTERM_CONF_BAK
    gconftool-2 --load ${CLAMIT_SKEL}/${GTERM_CONF}
}

function reset_terminal {
    [ ! -f "$GTERM_CONF_BAK" ] && echo "Backup '${GTERM_CONF}' not found." && return
    gconftool-2 --load $GTERM_CONF_BAK
    rm $GTERM_CONF_BAK
}

function run_cmd {
    set_terminal
    gnome-terminal --window-with-profile=KeepOpen -x bash -l -c "$subcmd"
    reset_terminal
}


### 'MAIN' function ###

if [[ "$#" < "1" ]]; then
    exit
fi

subcmd=${@}
echo "$subcmd"

run_cmd $subcmd

exit