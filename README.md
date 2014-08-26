TravisTesting
=============

[![Build Status](https://travis-ci.org/quasiben/TravisTesting.svg?branch=master)](https://travis-ci.org/quasiben/TravisTesting)

Testing for Various Travis CI and Services


##MySQL OSX Setup

```
unset TMPDIR
mysql_install_db --verbose --user=`whoami` --basedir="$(brew --prefix mysql)" --datadir=/usr/local/var/mysql --tmpdir=/tmp

mysql.server start

mysqladmin -u root password 'new-password'
mysql_secure_installation

CREATE USER 'quasiben'@'localhost' IDENTIFIED BY '';
GRANT ALL PRIVILEGES ON * . * TO 'quasiben'@'localhost';
FLUSH PRIVILEGES;
```
