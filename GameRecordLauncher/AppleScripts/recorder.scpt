tell application "QuickTime Player"
                activate
                set doc to new screen recording
                tell application "System Events" to tell process "QuickTime Player"
                        # delay 5
                        key code 49
                end tell
                # recording begins here
                doc
end tell

