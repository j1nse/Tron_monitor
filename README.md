# Tron_monitor
## a project to monitor the Tron

There is much room for optimization and improvement

#### requirement

- python3
- tronapi
- mysql.connector
- prettytable
- pysocks(if you need socks proxy)
- base58
- apscheduler

#### how to use

you need write a config file named `setting.conf` by yourself and just follow the `setting_example.conf`to write it. And you'd better use `json.dump`to create it

`python tron_client.py`

PS: If your database doesn't exist, program will help you to create a new database

PS: the **top app monitor** needs you to set by yourself, you need to type all address of it(base58), and its name

1. you need type `1.begin work`
2. and then start a new terminal run program type `2.query`to query what you want to know
3. if you want to monitor a DAPP, you need to know all of its address and name and type`3.set..` to set a DAPP.
4. don't forget to set a proper number for `Max_transfer` and `Max_transfer_token` in `setting.conf`

------

## plan

- [x] Understand the differences between Ether and Tron
- [x] Learn to crawl data from Tron
- [x] Learn to analysis and processing
- [x] Design and Programming
- [ ] ~~Implement the daemon process and improve the rest of the logic~~(no time at the moment)

---------

### target

- [x] TRON large transfer monitoring
- [x] Top DApp balance/etc. Data collection
- [x]  DAU

-----

### time

ends on 12.10(but I have to prepare for the final  examination...)

----

### other

~~Grpc local environment compiled~~(use HTTP)

### mind

school final examination !!!!!!!!!!!!!!!!!!!!!!!!!!!

debug and optimize !!!







