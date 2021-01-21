# remote_screen_server_snap

Currently snapcraft can only handle snaps from within the HOMEDir
https://forum.snapcraft.io/t/after-upgraded-multipass-to-1-3-0-snapcraft-cannot-work-any-more/18089/3

cd ~/Documents/snaps/screen_server

snapcraft clean
snapcraft
sudo snap install --dangerous --devmode remotescreens_0.1_amd64.snap

remotescreens.register
remotescreens.help

snap stop remotescreens
