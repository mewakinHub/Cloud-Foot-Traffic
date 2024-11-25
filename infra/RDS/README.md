```
CREATE TABLE Config (
  username varchar(255) NOT NULL,
  Monitoring_status tinyint NOT NULL,
  streaming_URL text NOT NULL,
  email varchar(255) DEFAULT NULL,
  PRIMARY KEY (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
```
```
CREATE TABLE Result (
  result_id int NOT NULL AUTO_INCREMENT,
  username varchar(255) NOT NULL,
  DATE_TIME datetime NOT NULL,
  config varchar(255) DEFAULT NULL,
  result int NOT NULL,
  processed_detection_image longtext,
  PRIMARY KEY (result_id),
  KEY username_idx (username),
  CONSTRAINT username FOREIGN KEY (username) REFERENCES Config (username)
) ENGINE=InnoDB AUTO_INCREMENT=209 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
```

NOTE: Single RDS has multiple schemas which contain the the procedure(pre-defined function), trigger(before any action such as delete or insert), table

REPORT:
we create schema as the name of CCTV_service which has 2 tables as Config & Result
we add procedure in schema that control every user to have only 24 row
we add event in schemas that trigger procedure every 1 hour (but demo as 10 second)
