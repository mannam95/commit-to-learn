# Steps for installing zellij

## Prerequisites
- Make sure the script files are executable
    ```Bash
    chmod +x install-zellij.sh
    chmod +x open-zellij.sh
    ```
- Make sure xclip is installed
    ```Bash
    sudo apt install xclip
    ```
- These instructions are for Linux especially Ubuntu distributions

## Installation
- Install zellij using the `install-zellij.sh` script with sudo
- Restart the terminal or just type `bash` in the current terminal
- Now `zellij` should be recognized as a command

## Enable copy to clipboard in zellij
- Try to open the file `sudo nano ~/.config/zellij/config.kdl`
- If it doesn't exist, the just create a zellij session using `zellij` command in the terminal
- This will open a new zellij session with a default config and the config file will be created
- Now try to open the file `sudo nano ~/.config/zellij/config.kdl` again
- Find a line that looks like below
    ```Bash
    copy_command "xclip -selection clipboard"
    ```
- Normally this would be commented out, so uncomment it and save the file

## Custom layouts
- Create a new layout in the `layouts` directory
- Create your own kdl file in the `layouts` directory
- Create as many layouts as you want

## Usage with open-zellij.sh
- Try to adapt `open-zellij.sh` to your needs
- Run the script `./open-zellij.sh`
- Select the layout you want to use
- Enjoy!