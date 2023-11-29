--Function that takes a cat_id and returns the IAV category from the hierarchy. 
--Parent_cat_name can be used to "stop" at a certain level in the hierarchy e.g. stop under the IAV parent

drop FUNCTION wkcreport.getIAV;

CREATE FUNCTION wkcreport.getIAV (cat_id varchar(64), parent_cat_name varchar(1024))
    RETURNS varchar(1024)   
   
LANGUAGE SQL
    READS SQL DATA
   
NO EXTERNAL ACTION
    DETERMINISTIC

BEGIN ATOMIC

DECLARE v_path VARCHAR(1024) DEFAULT '';
DECLARE part1 VARCHAR(1024) DEFAULT '';
DECLARE part2 VARCHAR(1024) DEFAULT '';
DECLARE part3 VARCHAR(1024) DEFAULT '';
DECLARE iav bigint DEFAULT 0;

SET v_path = (
SELECT
    CONCAT ('/',
   listagg(name,
   '/')) AS PATH
FROM     (
   SELECT
       c.NAME name,
       LEVEL
   FROM        WKCREPORT.CATEGORY_ASSOCIATIONS ca
   INNER JOIN WKCREPORT.CATEGORIES c  
	      ON
       ca.END1_CATEGORY_ID = c.CATEGORY_ID
       AND 
	         ca.RELATIONSHIP_TYPE = 'parent_category'
   START WITH
       ca.END2_CATEGORY_ID = cat_id
   CONNECT BY
       NOCYCLE PRIOR ca.END1_CATEGORY_ID = ca.END2_CATEGORY_ID
   ORDER BY
       LEVEL DESC 
    )
    );

SET iav = locate(parent_cat_name, v_path);
IF iav > 0 THEN
--    SET part3 = v_path;
	SET part1 = substr(v_path, iav);
	SET iav = locate('/', part1) + 1;
	IF iav > 1 THEN
		SET part2 = substr(part1, iav);
	ELSE
		SET part2 = part1;
	END IF;
	SET iav = locate('/', part2) - 1;
	IF iav > 0 THEN
	    SET part3 = substr(part2, 1, iav);
	ELSE
		SET part3 = part2;
	END IF;
ELSE
    SET part3 = 'not an IAV';
END IF;
IF part3 = parent_cat_name THEN
    SET part3 = (SELECT c.NAME name FROM WKCREPORT.CATEGORIES c WHERE c.category_id = cat_id);
END IF;

RETURN part3;
END
