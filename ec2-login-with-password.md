### Allow user to login to EC2 instance with password (not ssh key)

For Ubuntu 12.04:
* `sudo adduser abc`
* `sudo su - abc`
* Password authentication is disabled by default in ssd configuration. To enable, modify sshd config file (at /etc/ssh/sshd_config) and change 

`PasswordAuthentication no` to `PasswordAuthentication yes`

* restart ssh service: `sudo service ssh restart` 

* You can now ssh into the EC2 instance as use `abc` with password set while creating user