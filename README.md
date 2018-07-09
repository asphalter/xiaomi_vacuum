# Home Assistant integration: Xiaomi Vacuum v1

If you're here probably you want to integrate Xiaomi Vacuum v1 with Home Assistant without loosing some useful functions such as live maps.


## On the Vacuum

###### Root the vacuum

If you don't know how to gain SSH access to your vacuum please read [the article](https://github.com/dgiese/dustcloud/wiki/VacuumRobots-manual-update-root-Howto) on dustcloud:


###### Install on the vacuum

- Create SSH keypair with the command: **ssh-keygen**

- Copy the SSH public key to the Home Assistant host with the command: **ssh-copy-id homeassistant@##HOMEASSISTANT_ADDRESS##**

- Copy the file vacuum/etc/rc.local to your vacuum, replacing the existing /etc/rc.local.

- Copy the file vacuum/opt/rockrobo/scripts/maps_to_ha.sh to your vacuum, at the destination /opt/rockrobo/scripts/maps_to_ha.sh.

- Make sure to give to the file the right permissions with the command: **chown 755 /opt/rockrobo/scripts/maps_to_ha.sh**.

###### Install on Home Assistant

We can assume that you're executing your Home Assistant istance using the user **homeassistant** in the directory **/home/homeassistant**.
If not please fix the directories specified to the top of the given scripts.

We can assume you're using a RedHat like system (CentOS, Fedora, RedHat, SuSe, ...) as destination host.

- Ensure that you've installed **python-pillow** package. On RedHat like systems you can issue the command **yum install python-pillow**

- Ensure that you've installed **incrond** package. On RedHat like systems you can issue the command **yum install incron**

- Copy vacuum/etc/incron.d/vacuum_maps to /etc/incron.d/vacuum_maps.

- Create the directories **/home/homeassistant/scripts**, **/home/homeassistant/www**, **/home/homeassistant/vacuum** if not exist.

- Make sure to fix the ownership of these directories to the user **homeassistant**.

- Copy the script homeassistant/home/homeassistant/scripts/build_maps.py to /home/homeassistant/scripts/build_maps.py.

- Copy the script homeassistant/home/homeassistant/scripts/incrond_vacuum_maps.sh to /home/homeassistant/scripts/incrond_vacuum_maps.sh.

- Make sure to give to the file the right permissions with the command: **chown 755 /home/homeassistant/scripts/incrond_vacuum_maps.sh**.


###### Show the map on Home Assistant

Add the following component to your HA configuration file:

```
camera:
  - platform: generic
    name: Vacuum Map
    still_image_url: http://127.0.0.1:8123/local/navmap.png
    content_type: image/png
    framerate: 1
```
