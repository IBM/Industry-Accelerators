-- SQL to create data privacy view in wkc reporting database (tested on DB2)
-- If using a schema other than WKCREPORT, search/replace all instances of WKCREPORT with your schema name

CREATE VIEW WKCREPORT.V_PRIVACY_REPORT AS (
SELECT
    c.NAME container_name,
    c.CONTAINER_TYPE container_type,
    tab.name table_name,
    col.name col_name,
    gov.name gov_artifact_name,
    gov.artifact_type,
    col_artifact_xref.assignment_state,
    classif.name classification,
    er.NAME rule_name,
    er.ACTION_NAME rule_action,
    at2.TAG_NAME
FROM
    WKCREPORT.CONTAINERS c
INNER JOIN wkcreport.container_assets tab 
       ON c.CONTAINER_ID = tab.CONTAINER_ID
INNER JOIN wkcreport.container_data_asset_columns col 
       ON col.asset_id = tab.asset_id AND col.container_id = tab.container_id
INNER JOIN wkcreport.data_asset_column_artifact_associations col_artifact_xref 
       ON col_artifact_xref.asset_id = col.asset_id AND col_artifact_xref.container_id = col.container_id
       AND col_artifact_xref.name = col.name
    -- AND col_artifact_xref.assignment_state = 'ASSIGNED'
INNER JOIN wkcreport.governance_artifacts gov 
       ON col_artifact_xref.associated_artifact_id = gov.artifact_id
LEFT OUTER JOIN wkcreport.governance_artifact_associations gov_gov_xref 
       ON (gov.artifact_id = gov_gov_xref.end2_artifact_id
           AND GOV_GOV_XREF.END2_ARTIFACT_TYPE = 'glossary_term'
           AND GOV_GOV_XREF.END1_ARTIFACT_TYPE = 'classification')
          OR
           (gov.artifact_id = gov_gov_xref.end1_artifact_id
            AND GOV_GOV_XREF.END1_ARTIFACT_TYPE = 'data_class'
            AND GOV_GOV_XREF.END2_ARTIFACT_TYPE = 'classification')
LEFT OUTER JOIN wkcreport.governance_artifacts classif 
       ON (classif.artifact_id = gov_gov_xref.end1_artifact_id
           AND classif.artifact_type = 'classification'
           AND classif.name LIKE '%Personal%')
          OR 
           (classif.artifact_id = gov_gov_xref.end2_artifact_id
            AND classif.artifact_type = 'classification'
            AND classif.name LIKE '%Personal%')
LEFT OUTER JOIN WKCREPORT.ARTIFACT_ENFORCEMENT_RULE_ASSOCIATIONS aera
       ON aera.ARTIFACT_ID = gov.ARTIFACT_ID
LEFT OUTER JOIN WKCREPORT.ENFORCEMENT_RULES er 
       ON ER.RULE_ID = aera.RULE_ID
LEFT OUTER JOIN WKCREPORT.ARTIFACT_TAGS at2 
       ON gov.ARTIFACT_ID = at2.ARTIFACT_ID AND at2.TAG_NAME IN ('gdpr', 'ccpa')
);
