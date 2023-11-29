------------------------------------------------------------------------
-- Create the getCatPath function, which returns a path (concatenation
-- of parent categories in hierarchy). This is difficult to do in SQL
-- so best handled in a function
------------------------------------------------------------------------

--DROP FUNCTION wkcreport.getCatPath;

CREATE FUNCTION wkcreport.getCatPath (cat_id varchar(64))
     RETURNS varchar(300)
     LANGUAGE SQL
     READS SQL DATA
     NO EXTERNAL ACTION
     DETERMINISTIC
     RETURN SELECT
     concat ('/', listagg(name, '/')) as PATH FROM
     (
     SELECT  
 	 c.NAME name,
	 LEVEL 
	 FROM 
	 WKCREPORT.CATEGORY_ASSOCIATIONS ca
	 INNER JOIN WKCREPORT.CATEGORIES c  
	      ON ca.END1_CATEGORY_ID = c.CATEGORY_ID AND 
	         ca.RELATIONSHIP_TYPE = 'parent_category'
	 START WITH ca.END2_CATEGORY_ID = cat_id
	 CONNECT BY NOCYCLE PRIOR ca.END1_CATEGORY_ID = ca.END2_CATEGORY_ID 
 	 ORDER BY LEVEL DESC 
     )
;

grant execute on function wkcreport.getCatPath to public;
