systemctl() {
    if [ "$1" = "status" ] && { [ "$2" = "ssh" ] || [ "$2" = "ssh.service" ]; }; then
        if pgrep -x sshd >/dev/null 2>&1; then
            printf '%s\n' \
                '● ssh.service - OpenBSD Secure Shell server' \
                '   Loaded: loaded (/etc/init.d/ssh; generated)' \
                '   Active: active (running)'
            return 0
        fi
        printf '%s\n' \
            '● ssh.service - OpenBSD Secure Shell server' \
            '   Loaded: loaded (/etc/init.d/ssh; generated)' \
            '   Active: inactive (dead)'
        return 3
    fi

    if [ "$1" = "is-active" ] && { [ "$2" = "ssh" ] || [ "$2" = "ssh.service" ]; }; then
        if pgrep -x sshd >/dev/null 2>&1; then
            printf 'active\n'
            return 0
        fi
        printf 'inactive\n'
        return 3
    fi

    command systemctl "$@"
}
