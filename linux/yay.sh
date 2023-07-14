#!/bin/bash

# Update everything
pacman -Syu --noconfirm

# Install yay
pacman -S --noconfirm git
cd /opt
sudo git clone https://aur.archlinux.org/yay-git.git
chown -R wi ./yay-git/
cd yay-git/
makepkg -si
cd ~
