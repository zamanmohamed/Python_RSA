according to the intern requirement
in this project, I used
front end (React)
backend(flask)
database (SQL) 
and end points communicate in Jason format

in the project,
•	In front there are 3 types of buttons. they are Generate key, remove key and Encrypt key
•	When you select the Generate key according to RSA algorithm, client private and public keys will be generated and it will be store in local storage
•	When you click the remove key, client private and public keys will be removed in local storage
•	selecting the encrypt button in backend will create a private and public key (key 1). public key 1 will be sent into the front. after that using public key 1, client public key will be encrypted and send to the back end 
•	I have created the table and its name is key_table and it has all 5 rows (as mentioned in intern assignment) 

During the assignment period I couldn’t find the solution for these problems. they are
•	I couldn’t decrypt in flask backend what I had encrypted in react front end 
•	But I could decrypt backend what I had encrypted in backend itself (but there is no problem in vise versa)


--------SQL COMMAND------------ 

CREATE DATABASE key_db

CREATE TABLE key_table(
    id int NOT NULL PRIMARY KEY
    public_key_1 TEXT NOT NULL,
    private_key_1 TEXT NOT NULL,
    public_key_2 TEXT NOT NULL,
    private_key_2 TEXT NOT NULL,
    client_public_key TEXT NOT NULL, 
);
