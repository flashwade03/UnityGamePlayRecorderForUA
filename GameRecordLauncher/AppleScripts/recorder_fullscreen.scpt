tell application "QuickTime Player"
    activate
    set doc to new screen recording
    set DisplayWidth to 480
    set DisplayHeight to 640
    tell application "System Events" to tell process "QuickTime Player"
        key code 49
        click at {DisplayWidth div 2, DisplayHeight div 2}
    end tell
    start doc
end tell
