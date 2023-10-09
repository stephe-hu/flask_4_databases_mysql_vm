# flask_4_databases_mysql_vm

## VM and MySQL Setup Process
1. Login into `Azure Portal` and go to `Virtual Machines`. Click on create a new Azure virtual machine.
2. Select existing resource group or create a new one. Change the default configuraton options as needed. Make sure to create a password for the VM. And select the inbound ports `HTTP(80)` and `HTTPS(443)`. Click on `Review + create` and then `Create`.
3. Once the VM is created, click on the VM and go to `Networking`. Click on `Add inbound port rule` and add `MySQL` port `3306` and `Flask` port `5000`. Click on `Add`.
4. Open up the Cloud Shell environement and SSH into the VM using the command `ssh <username>@<public-ip-address>`. Enter the password when prompted. 
5. Update the UBUNTU (OS) SERVER by entering `sudo apt-get update`. Install MySQL by entering `sudo apt-get install mysql-server`. Enter `Y` when prompted.
6. Enter `sudo mysql` to log into MySQL. Enter the following commands to create a new user and grant privileges to the user: `CREATE USER ‘user'@'%' IDENTIFIED BY ‘password’;` and `GRANT ALL PRIVILEGES ON *.* TO ‘user'@'%’ WITH GRANT OPTION;`. Enter `exit` to exit MySQL.
7. Enter `sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf` to edit the MySQL configuration file. Change the `bind-address` to `0.0.0.0`. Save the file and exit.
8. Enter `sudo service mysql restart` to restart MySQL. 
9. Open up MySQL Workbench and create a new connection. Enter the VM's public IP address, username, and password. Click on `Test Connection` and then `OK`. The IP address can be found on the VM's overview page in Azure Portal. And the username and password are the ones created in step 6.

## Database Schema Rationale
My first table is the patients table with the patient_id as the PK. My second table is the medications table with the medication_id as the PK. My third table is the patient_medications table with the patient_medication_id as the PK and the patient_id and medication_id as the FKs. I chose to use a many-to-many relationship because a patient can have many medications and a medication can be taken by many patients. This schema allows me to associate a patient with a medication(s) for a specific prescription.

## Challenges
I did not have any major technical issues with this assignment as I had already solved the major issues in the previous assignment. One thing that I noticed when I was playing around with formatting the html files was that how the data is displayed on the flask app changes depending on  if I included the `{% extends "base.html" %} {% block content %}` and `{% endblock %}` tags. I have included two screenshots of the `patients.html` to display the difference. I think this is because of the tags that are included in the `base.html` file. I decided to use the tags in my final code because I think it looks better for an app and I like the interactions in the app better.