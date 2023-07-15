# 📜 Quick Scripts
This repository will contain easy-to-use Windows &amp; Linux scripts. This README file will be responsible for a short description of each script.

## :memo: License

This repository was contributed by **Valentin-Ioan Vintilă** and it is provided under
the MIT License. For more info about the author, check out his
[personal website](https://v-vintila.com/) or his
[other projects](https://github.com/w1bb).

## :poop: Windows scripts

All the Windows scripts shall be provided in the [windows](https://github.com/w1bb/quick-scripts/blob/master/windows) directory.

These made it into my collection:

- :globe_with_meridians: Internet Blocker ([internet-blocker.bat](https://github.com/w1bb/quick-scripts/blob/master/windows/internet-blocker.bat))

  This script will quickly block internet access to all the executable files (`(*.exe)`) inside a given folder (`[INSERT PATH HERE]`), recursively (`/R`). Both inbound (`dir=in`) and outbound (`dir=out`) connections will cease to exist.

  ⚠️ **Admin privileges required**

## 🐧 Linux scripts

All the Linux scripts shall be provided in the [linux](https://github.com/w1bb/quick-scripts/blob/master/linux) directory.

The following made it into my collection:

- 🎉 Yay Installer ([yay.sh](https://github.com/w1bb/quick-scripts/blob/master/linux/yay.sh))

  This script will automatically install the `yay` package manager on your arch system.

  ⚠️ **sudo privileges required**

- 🔧 ISO USB Burner

  First, use `lsblk` to figure out what is the name of your USB drive (`sdX`, where `X` could be `a`, `b` etc.). Then, adapt the following one-liner to your needs:

  ```
  # dd bs=4M if=path/to/iso of=/dev/sdX conv=fsync oflag=direct status=progress
  ```
  ⚠️ **sudo privileges required**
