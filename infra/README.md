### How to Remote
```
ssh -i bastion.pem -L 3307:des424-g09-rds.cpqayo04ersh.ap-southeast-1.rds.amazonaws.com:3306 ubuntu@13.213.77.92
```
NOTE:
local PC port: 3307
-L for local
3306 is port of mysql inside RDS

we open tunnel to RDS via bastian/jenkins server EC2 instance



### RDS
NOTE: Single RDS has multiple schemas which contain the the procedure(pre-defined function), trigger(before any action such as delete or insert), table

we create schema as the name of CCTV_service which has 2 tables as Config & Result
we add procedure in schema that control every user to have only 24 row
we add event in schemas that trigger procedure every 1 hour (but demo as 10 second)

name: des424-g09-rds
PASSWORD: group9login


### S3
we do not have the life-cycle

