#!/bin/bash

# Update everything
sudo pacman -Syu --noconfirm

# Install git
sudo pacman -S --noconfirm git

# Clone the repository and make sure it belongs to the current user
cd /opt
sudo git clone https://aur.archlinux.org/yay-git.git
current_user=$(whoami)
sudo chown -R $current_user ./yay-git/

# Finally, install yay
cd ./yay-git/
makepkg -si
cd ~

