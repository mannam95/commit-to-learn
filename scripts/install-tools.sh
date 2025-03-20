#!/bin/bash

# Function to install Google Chrome
install_chrome() {
    echo "Installing Google Chrome..."
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo gpg --dearmour -o /usr/share/keyrings/chrome-keyring.gpg 
    sudo sh -c 'echo "deb [arch=amd64 signed-by=/usr/share/keyrings/chrome-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list' 
    sudo apt update
    sudo apt install -y google-chrome-stable
    sudo sed -i '3s/^/#/' /etc/apt/sources.list.d/google-chrome.list
    echo "Google Chrome installed."
}

# Function to install Brave Browser
install_brave() {
    echo "Installing Brave Browser..."
    sudo apt install -y curl
    sudo curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg
    echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main"|sudo tee /etc/apt/sources.list.d/brave-browser-release.list
    sudo apt update
    sudo apt install brave-browser
    echo "Brave Browser installed."
}

# Function to install Docker
install_docker() {
    echo "Installing Docker..."
    sudo apt-get update
    sudo apt-get install -y ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    sudo groupadd docker
    sudo usermod -aG docker $USER
    newgrp docker
    echo "Docker installed."
}

# Function to install Visual Studio Code
install_vscode() {
    echo "Installing Visual Studio Code..."
    wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
    sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
    sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
    rm -f packages.microsoft.gpg
    sudo apt install -y apt-transport-https
    sudo apt update
    sudo apt install -y code
    echo "Visual Studio Code installed."
}

# Function to install Azure CLI
install_azure_cli() {
    echo "Installing Azure CLI..."

    sudo apt install apt-transport-https ca-certificates curl gnupg lsb-release
    
    wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
    sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg

    AZ_DIST=$(lsb_release -cs)

    # Proper way to handle newlines
    sudo tee /etc/apt/sources.list.d/azure-cli.sources > /dev/null <<EOF
        Types: deb
        URIs: https://packages.microsoft.com/repos/azure-cli/
        Suites: ${AZ_DIST}
        Components: main
        Architectures: $(dpkg --print-architecture)
        Signed-by: /etc/apt/keyrings/packages.microsoft.gpg
EOF

    rm -f packages.microsoft.gpg
    sudo apt update
    sudo apt install -y azure-cli

    echo "Azure CLI installed."
}

# Function to install terraform
install_terraform() {
    echo "Installing Terraform..."
    sudo apt-get update && sudo apt-get install -y gnupg software-properties-common
    wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
    sudo apt update
    sudo apt install terraform
    echo "Terraform installed."
}

# Function to install GitHub Desktop
install_github_desktop() {
    echo "Installing GitHub Desktop..."
    wget -qO - https://apt.packages.shiftkey.dev/gpg.key | gpg --dearmor | sudo tee /usr/share/keyrings/shiftkey-packages.gpg > /dev/null
    sudo sh -c 'echo "deb [arch=amd64 signed-by=/usr/share/keyrings/shiftkey-packages.gpg] https://apt.packages.shiftkey.dev/ubuntu/ any main" > /etc/apt/sources.list.d/shiftkey-packages.list'
    sudo apt update
    sudo apt install -y github-desktop
    echo "GitHub Desktop installed."
}

# Menu for user to select installation
show_menu() {
    echo "Select an option to install:"
    echo "1) Google Chrome"
    echo "2) Brave Browser"
    echo "3) Docker"
    echo "4) Visual Studio Code"
    echo "5) Azure CLI"
    echo "6) Terraform"
    echo "7) GitHub Desktop"
    echo "8) Install All"
    echo "9) Exit"
    read -p "Enter your choice: " choice

    case $choice in
        1)
            install_chrome
            ;;
        2)
            install_brave
            ;;
        3)
            install_docker
            ;;
        4)
            install_vscode
            ;;
        5)
            install_azure_cli
            ;;
        6)
            install_terraform
            ;;
        7)
            install_github_desktop
            ;;
        8)
            install_chrome
            install_brave
            install_docker
            install_vscode
            install_azure_cli
            install_terraform
            install_github_desktop
            ;;
        9)
            echo "Exiting."
            exit 0
            ;;
        *)
            echo "Invalid choice."
            ;;
    esac
}

# Main script
show_menu
