#!/bin/bash
# Wrapper: hyperframes mit lokalem Headless-Chrome, ohne Telemetrie
export HYPERFRAMES_TELEMETRY_DISABLED=1 DO_NOT_TRACK=1
[ -x /opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell ] && export HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell
exec "${HF_BIN:-npx hyperframes}" "$@"
