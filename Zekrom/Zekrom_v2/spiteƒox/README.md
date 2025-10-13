### for optimal compatibility, place the spiteƒox folder in your PYTHONPATH.<br>
should look like this:<br>
  - C:/path/to/PYTHONPATH/spiteƒox/spitefox.py<br>
### alternatively just place the spiteƒox folder wherever the project root is<br>
for reshiram it would look like this:<br>
  - C:/path/to/Reshiram/Reshiram.py<br>
  - C:/path/to/Reshiram/spiteƒox/spitefox.py<br>

### setup
the spiteƒox folder ships with additional content like assets, and documentation
run ``setup.bat`` to create neccecary folders
(AppData/Roaming/.spitefox)<br>
(AppData/Local/.spitefox-persistent)<br>
(AppData/Local/.spitefox-persistent/spiteƒox)<br>

provided is also a test script for spiteƒox so you can study and weep :³
(fr tho its helpful i think maybe idk)

the setup script will also copy files from the folder below into .spitefox-persistent/spiteƒox

spiteƒox/data/spiteƒox:
### ``assets``
contains audio and icon files that spitefox uses
### ``defaults``
contains the default config for newly created instances, it is reccomended to not change this
### ``tokens.json``
contains a list of json entries that keeps your discord bot tokens for ease of use (optional)
### ``spitefox.toml
contains the config for spitefox itself(signature, version, etc)

whatever you put in the ``data`` folder will also be copied over, the folders in ``data`` acting as the root directories
so ``data/reshiram/testfile.txt`` -> ``.spitefox-persistent/reshiram/testfile.txt``
