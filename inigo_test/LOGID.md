
# linux : 
https://cambiatealinux.com/instalar-google-drive-en-ubuntu


# computer optimization: 
minirobbin@minirobbin:~$ sudo systemctl restart logid
minirobbin@minirobbin:~$ sudo nano /etc/logid.cfg

## Main repository
https://github.com/PixlOne/logiops

### Guide
https://medium.com/@jeromedecinco/configuring-logiops-for-logitech-mx-master-3s-on-rhel-based-systems-d3971101c324

### example
https://github.com/menuRivera/logiops/blob/master/logid.cfg

# commands
sudo systemctl enable --now logid
sudo systemctl restart logid


# CAMARA: 
iriunwebcam


# elementos extraer claves 
wmic memorychip get manufacturer, partnumber, speed, capacity

Get-CimInstance Win32_PhysicalMemory | Select-Object Manufacturer, PartNumber, Speed, Capacity, SerialNumber


Clave de producto de Windows:PowerShell
(Get-WmiObject -query 'select * from SoftwareLicensingService').OA3xOriginalProductKey
