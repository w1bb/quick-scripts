# 📜 Quick Scripts

This repository contains easy-to-use scripts and configuration files for both **Windows** and **Linux**.

The README file is here to present a short description for each script.

## :memo: License

This repository was kindly contributed by **Valentin-Ioan Vintilă** under the MIT License. For more info about the author, check out his [personal website](https://v-vintila.com/) or some of his [other projects](https://github.com/w1bb).

## Content

As you can tell, there are two main directories in this repository:

- `./linux` will contain various scripts and configuration files for the Linux OS. These were mostly tested for Arch, but they should work fine for other distros as well.
- `./windows` currently contains scripts and configurations that work on Windows 10.

## Linux

### Linux config files

The config files can be found in the [.config](./linux/.config) directory. These include:

- [alacritty](./linux/.config/alacritty) - My current Alacritty theme (this could be easily ported to Windows as well).
- [tmux](./linux/.config/tmux) - A sane tmux configuration for all my personal needs.
- [nvim](./linux/.config/nvim) - A modern, simple and efficient NeoVim configuration.

### Linux scripts

All the Linux scripts shall be provided in the [linux](https://github.com/w1bb/quick-scripts/blob/master/linux) directory. The scripts that required sudo privileges are prefixed with the **#** symbol.

The following made it into my collection:

- **#** Yay Installer ([yay.sh](https://github.com/w1bb/quick-scripts/blob/master/linux/yay.sh))

  This script will automatically install the `yay` package manager on your arch system.

- **#** ISO USB Burner

  First, use `lsblk` to figure out what is the name of your USB drive (`sdX`, where `X` could be `a`, `b` etc.). Then, adapt the following one-liner to your needs:

  ```
  # dd bs=4M if=path/to/iso of=/dev/sdX conv=fsync oflag=direct status=progress
  ```

- **$** Tree To File Structure

  This script will convert a file structure given in the form of a `tree` output (or similar) into the files themselves.

## Windows

### Windows config files

Currently, there are no configuration files available for Windows.

### Windows scripts

All the Windows scripts shall be provided in the [windows](https://github.com/w1bb/quick-scripts/blob/master/windows) directory. The scripts that required administrator privileges are prefixed with the **#** symbol.

These made it into my collection:

- **#** Internet Blocker ([internet-blocker.bat](https://github.com/w1bb/quick-scripts/blob/master/windows/internet-blocker.bat))

  This script will quickly block internet access to all the executable files (`(*.exe)`) inside a given folder (`[INSERT PATH HERE]`), recursively (`/R`). Both inbound (`dir=in`) and outbound (`dir=out`) connections will cease to exist.
