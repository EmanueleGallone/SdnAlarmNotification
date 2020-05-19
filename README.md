# SDN Alarm Notifier

SDN Alarm Notifier is a multi-threaded application that will retrieve alarms from your SDN devices using NETCONF.

## Getting Started

Just clone or download the repository somewhere on your PC. <br>

### Prerequisites

Python >= 3.8 required. We recommend Anaconda or [Miniconda](https://docs.conda.io/en/latest/miniconda.html).
 
If you don't want to install packages on your main environment, open an Anaconda prompt and create a new environment
```
conda create --name yourenv python=3.8
```
activate it
```
conda activate yourenv
```

### Installing

with your new virtual environment activated,
change the Anaconda prompt's directory to the one where you cloned or downloaded this repository 
and then run the following command to install all the python packages required to run this application
``` 
pip install -r requirements.txt
```

Make sure that all the packages are correctly installed.

## Running the application

open the *config.json* file and change the parameters to your liking inside the *Notification_config*. <br>
Set the *DEBUG_MODE* to "False" to make the application use your parameters

Start main.py to start only the service

``` 
python main.py
```

If you want to start the GUI /TODO

## Under the hood
The following image shows an overview of the underlying software architecture:

![alt text](docu/img/project.png?raw=true)

In the *config.json* file, under the "Network" key, there's a list of devices:
this allows you to specify as many devices as you want to be monitored by our application. <br>
Each device will be managed by a separated thread (denoted as *Worker Thread* inside the picture),
in charge of parsing the alarms received through NETCONF and deliver them to the database manager.

**Database Manager**:<br>
As you can see, the DB is abstracted from the rest of the application. This allows the interchangeability of databases' technologies, SQL or NOSQL
(for instance if we want to connect to a mongoDB instance we just have to edit the *database_manager.py* file and nothing else).

To keep the things as simple as we could, we opted for sqlite, that is a DB on file, even though sqlite is not suited for a multi-threading environment like ours.

**Notification Manager:** <br>
The **notification manager** is the object responsible of notifying the users about the alarms that are coming from the SDN devices.
Inside the notification manager there's a thread that every second queries the DB to see if there are new alarms to be notified.<br>
We could've avoided this approach if we could've used the *SQL Trigger* mechanism but
after experiencing sqlite's performances we opted for the thread that repeatedly queries the Database.

**NB**: Only the alarms with severity greater or equal than the '*Severity_notification_threshold*' (specified inside the config.json) will be notified to the users! <br>
The severities are mapped inside the config.json under *Severity_levels*.


## Running the tests

Sorry, no formal tests so far. We know that TDD is the best approach for software development 
but with just 4 weeks we preferred focusing on the project itself rather than tests.

## Versioning

We use [SemVer](http://semver.org/) for versioning.

## Authors

* **Emanuele Gallone [Github](https://github.com/EmanueleGallone/)** - *Development Team Leader* - *Initial work, architecture design, logic implementation*
* **Fabio Carminati [Github](https://github.com/fabiocarminati)** - *GUI Developer, Matplotlib guy, Tester* - *GUI Implementation and testing*
* **Andrés Felipe Rodriguez Vanegas [Github](https://github.com/andresrodriv)** - *GUI Developer and designer, Tester* - *GUI Implementation and testing*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thanks to Stefan Zimmermann aka @purplezimmermann for providing the code of policonf and
solving all of our issues on gitlab. Vielen dank for your patience! :)
* Hat tip to my colleagues Fabio and Andrés that kept on writing
 code even tough I pressured them to learn to use new libraries and
 assigning them a lot of tasks. I hope you learned a lot while doing this project together!
 * Thanks to [Alexhuszagh](https://github.com/Alexhuszagh) for providing the [style sheets](https://github.com/Alexhuszagh/BreezeStyleSheets) to improve the *look & feel* of our GUI.
* etc
