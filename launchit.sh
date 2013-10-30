#!/usr/bin/env bash

function run_cmd {
    gnome-terminal --window-with-profile=KeepOpen -x bash -l -c "$subcmd"
}

#cmd="gnome-terminal --window-with-profile=KeepOpen"

if [[ "$#" < "1" ]]; then
    exit
fi

subcmd=${@}
echo "$subcmd"

run_cmd $subcmd

exit