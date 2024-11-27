CREATE DEFINER=`admin`@`%` PROCEDURE `delete_oldest_result_per_user`()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE current_user_id INT;
    DECLARE user_cursor CURSOR FOR
    SELECT `user_id`
    FROM `Result`
    GROUP BY `user_id`
    HAVING COUNT(*) > 24;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    
    OPEN user_cursor;
    
    user_loop: LOOP
        FETCH user_cursor INTO current_user_id;
        IF done THEN
            LEAVE user_loop;
        END IF;
        
        DELETE FROM `Result`
        WHERE `result_id` = (
            SELECT result_id_to_delete
            FROM (
                SELECT `result_id` AS result_id_to_delete
                FROM `Result`
                WHERE `user_id` = current_user_id
                ORDER BY `result_id` ASC
                LIMIT 1
            ) AS oldest_row
        );
    END LOOP;
    
    CLOSE user_cursor;
END
