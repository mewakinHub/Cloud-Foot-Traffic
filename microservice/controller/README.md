## Manual
1. zip folder and CICD to Lambda
2. add Trigger (EventBridge)
- create a new rule
- Schedule expression
    ```
    cron(0/1 * * * ? *) # 1 minute
    cron(0 0/1 * * ? *) # 1 hour
    cron(0 0 * * ? *)   # 1 day
    ```
- Monitor tabs -> view cloudwatch log

## Local Access
1. open tunnel for access in local device
ssh -i bastionG9.pem -L 3307:mysql-rds-g09.cbk2ewumyiw9.ap-southeast-1.rds.amazonaws.com:3306 ubuntu@54.169.55.224
2. download workbench for manipulate db with UI-based

