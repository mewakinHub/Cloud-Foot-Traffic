### How to Remote
```
ssh -i bastion.pem -L 3307:des424-g09-db.couuhhmohu3z.us-east-1.rds.amazonaws.com:3306 ubuntu@54.81.57.229
```
NOTE:
local PC port: 3307
-L for local
3306 is port of mysql inside RDS

we open tunnel to RDS via bastian/jenkins server EC2 instance