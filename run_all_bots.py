import time
import subprocess

# Specify the path to your shell script
script_path = "/Users/ussdiscovery/Scrap/saga.sh"

# Wait for 10 minutes
wait_time = 30  # 10 minutes in seconds



def start():
                # Disable Terminal window restoration
        defaults_command = '''
        defaults write com.apple.Terminal NSQuitAlwaysKeepsWindows -bool false
        '''
        subprocess.run(["/bin/bash", "-c", defaults_command])


        # Run the shell script again
        subprocess.run(["bash", script_path])
        time.sleep(wait_time)
        # Close all terminal windows using AppleScript

          #Force kill the Terminal application
        subprocess.run(["pkill", "-f", "Terminal"])

        # Close all Terminal windows without saving state using AppleScript
        applescript_code = '''
        tell application "Terminal"
            close every window saving no
        end tell
        '''
        subprocess.run(["osascript", "-e", applescript_code])
        time.sleep(10)
        start()



start()
