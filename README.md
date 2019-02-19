
# web applicartion for saving sport items

Source code for the web application created with flask and sqlalquemy, the server saves sport items for later use.

## Getting Started

Install Vagrant And VirtualBox and
clone this repositore and log into the vagrant machine
### Prerequisites

* Python 3

```
donwload on python.org
```

* Vagrant

```
donwload on vagrantup.com/downloads.html
```
* Virtual box

```
donwload on virtualbox.org/wiki/Downloads
```
### Installing

* clone this repository or download

```
git clone https://github.com/yusefrich/PT--WP--UP--catalog-web-application.git
```
* Run vagrant up to start the vm with the virtual box

```
vagrant up
```

* Log on the vagrant virtual machine

```
vagrant ssh
```

* Open the project directory

```
cd /vagrant/catalog
```

* Run the models.py file

```
python models.py
```
* Populate the database with the db_populate file

```
python db_populate.py
```
* Start the server

```
python views.py
```
* you can see the server running on your localhost by accessing this url

```
http://localhost:5000
```




## Authors

* **udacity team** - *vagrant setup* - check on the CODEOWNERS file

* **yusef richard** - *web application using flask*



# Udacity student data

 *NAME*: Yusef Richard de Oliveira Alves <p>
 *COURSE*: udacity Nanodegree fullstack <p>
 *EMAIL*:yusef.rick@gmail.com <p>
