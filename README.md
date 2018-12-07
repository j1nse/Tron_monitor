# Tron_monitor
## a project to monitor the Tron

基本功都能用了，不过还有很大的优化空间

#### requirement

- python3
- tronapi
- mysql.connector
- prettytable
- pysocks(if you need socks proxy)

#### how to use

you need write a config file named `setting.conf` by yourself or just follow the program to write it. 

```json
{"full_node": "https://api.trongrid.io", "solidity_node": "https://api.trongrid.io", "event_server": "https://api.trongrid.io", "database": "tron", "user": "root", "host": "localhost", "password": "root"}
```

you'd better use `json.dump`to create it

`python tron_client.py`

PS: If your database doesn't exist, program will help you to create a new database

PS: the **top app monitor** needs you to set by yourself, you need to type all address of it(base58), and its name

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

final examination !!!!!!!!!!!!!!!!!!!!!!!!!!!

debug and optimize !!!







