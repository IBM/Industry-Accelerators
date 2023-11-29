drop VIEW WKCREPORT.V_MDLUC_JOINS;

CREATE VIEW WKCREPORT.V_MDLUC_JOINS AS (
SELECT
mdluc.ASSET_ID model_usecase_asset_id,
mdluc.NAME model_usecase_name,
mdluc.ASSET_TYPE model_usecase_type,
mdluc_custom_prop.PROPERTY_TEXT_VALUE model_usecase_risk_level,
mdl_class.NAME model_usecase_classification,
mdluc_tracks.asset_type model_asset_type,
mdluc_term.NAME model_usecase_term,
mdluc_policy.NAME model_usecase_policy,
mdluc_tracks.NAME model_name,
mdluc_table.ASSET_ID table_asset_id,
mdluc_table.NAME table_name,
mdluc_column.NAME column_name,
column_term.NAME column_term_name,
classif.NAME column_classification,
term_rule.NAME rule_name,
rule_policy.NAME policy_name
FROM
WKCREPORT.CONTAINER_ASSETS mdluc
-- join to get classification of the model use case
INNER JOIN WKCREPORT.GOVERNANCE_ARTIFACT_CONTAINER_ASSOCIATIONS gaca
   ON gaca.ASSET_ID = mdluc.ASSET_ID AND gaca.CONTAINER_ID = mdluc.CONTAINER_ID AND gaca.associated_artifact_type = 'classification'
INNER JOIN WKCREPORT.GOVERNANCE_ARTIFACTS mdl_class 
  ON mdl_class.artifact_id = gaca.associated_artifact_id AND mdl_class.name LIKE '%Personal%'
-- join from model use case to custom properties for risk level
LEFT OUTER JOIN WKCREPORT.ASSET_CUSTOM_PROP_VALUES mdluc_custom_prop
   ON mdluc_custom_prop.CONTAINER_ID = mdluc.CONTAINER_ID AND mdluc_custom_prop.ASSET_ID = mdluc.ASSET_ID AND mdluc_custom_prop.PROPERTY_ID = 'risk_level'
-- join from model use case to container_assets_associations to get 'tracks' relationship
LEFT OUTER JOIN WKCREPORT.CONTAINER_ASSETS_ASSOCIATIONS mdluc_tracks_xr
   ON mdluc_tracks_xr.END1_CONTAINER_ID = mdluc.CONTAINER_ID AND mdluc_tracks_xr.END1_ASSET_ID = mdluc.ASSET_ID AND mdluc_tracks_xr.END1_RELATIONSHIP_TYPE = 'tracks'
LEFT OUTER JOIN WKCREPORT.CONTAINER_ASSETS mdluc_tracks
   ON mdluc_tracks.CONTAINER_ID = mdluc_tracks_xr.END2_CONTAINER_ID AND mdluc_tracks.ASSET_ID = mdluc_tracks_xr.END2_ASSET_ID       
-- join from model use case to associated business term (if one exists)   
LEFT OUTER JOIN WKCREPORT.GOVERNANCE_ARTIFACT_CONTAINER_ASSOCIATIONS mdluc_mdlterm_xr
   ON mdluc_mdlterm_xr.ASSET_ID = mdluc.ASSET_ID AND mdluc_mdlterm_xr.CONTAINER_ID = mdluc.CONTAINER_ID AND mdluc_mdlterm_xr.ASSOCIATED_ARTIFACT_TYPE ='glossary_term'
LEFT OUTER JOIN WKCREPORT.GOVERNANCE_ARTIFACTS mdluc_term
   ON mdluc_term.ARTIFACT_ID = mdluc_mdlterm_xr.ASSOCIATED_ARTIFACT_ID
-- join from model use case to associated policy (if one exists)
LEFT OUTER JOIN WKCREPORT.ASSET_ARTIFACT_RELATIONS mdluc_mdlpolicy_xr
   ON mdluc_mdlpolicy_xr.END1_ASSET_ID = mdluc.ASSET_ID AND mdluc_mdlpolicy_xr.END1_CONTAINER_ID = mdluc.CONTAINER_ID AND mdluc_mdlpolicy_xr.END2_ARTIFACT_TYPE ='policy'
LEFT OUTER JOIN WKCREPORT.GOVERNANCE_ARTIFACTS mdluc_policy
   ON mdluc_policy.ARTIFACT_ID = mdluc_mdlpolicy_xr.END2_ARTIFACT_ID
-- join from model use case to associated data asset (table)
LEFT OUTER JOIN WKCREPORT.CONTAINER_ASSETS_ASSOCIATIONS mdluc_table_xr
   ON mdluc_table_xr.END1_CONTAINER_ID = mdluc.CONTAINER_ID AND mdluc_table_xr.END1_ASSET_ID = mdluc.ASSET_ID --AND mdluc_table_xr.END1_RELATIONSHIP_TYPE = 'governs'
LEFT OUTER JOIN WKCREPORT.CONTAINER_ASSETS mdluc_table
   ON mdluc_table.CONTAINER_ID = mdluc_table_xr.END2_CONTAINER_ID AND mdluc_table.ASSET_ID = mdluc_table_xr.END2_ASSET_ID AND mdluc_table.ASSET_TYPE = 'data_asset'
-- join from table to column
LEFT OUTER JOIN WKCREPORT.CONTAINER_DATA_ASSET_COLUMNS mdluc_column
   ON mdluc_column.ASSET_ID = mdluc_table.ASSET_ID AND mdluc_column.CONTAINER_ID = mdluc_table.CONTAINER_ID
-- join from column to associated term   
LEFT OUTER JOIN WKCREPORT.DATA_ASSET_COLUMN_ARTIFACT_ASSOCIATIONS col_artifact_xref
       ON col_artifact_xref.asset_id = mdluc_column.asset_id AND col_artifact_xref.container_id = mdluc_column.container_id
       AND col_artifact_xref.name = mdluc_column.name AND col_artifact_xref.ASSOCIATED_ARTIFACT_TYPE ='glossary_term'
LEFT OUTER JOIN WKCREPORT.GOVERNANCE_ARTIFACTS column_term
   ON column_term.ARTIFACT_ID = col_artifact_xref.ASSOCIATED_ARTIFACT_ID
-- join from term to classification
LEFT OUTER JOIN wkcreport.governance_artifact_associations gov_gov_xref
       ON (column_term.artifact_id = gov_gov_xref.end2_artifact_id
           AND GOV_GOV_XREF.END2_ARTIFACT_TYPE = 'glossary_term'
           AND GOV_GOV_XREF.END1_ARTIFACT_TYPE = 'classification')
          OR
           (column_term.artifact_id = gov_gov_xref.end1_artifact_id
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
-- join from term to rule
LEFT OUTER JOIN wkcreport.governance_artifact_associations term_rule_xref
       ON (column_term.artifact_id = term_rule_xref.end2_artifact_id
           AND term_rule_xref.END2_ARTIFACT_TYPE = 'glossary_term'
           AND term_rule_xref.END1_ARTIFACT_TYPE = 'rule')
LEFT OUTER JOIN wkcreport.governance_artifacts term_rule
       ON (term_rule.artifact_id = term_rule_xref.end1_artifact_id
           AND term_rule.artifact_type = 'rule')
-- join from rule to policy
LEFT OUTER JOIN wkcreport.governance_artifact_associations rule_policy_xref
       ON (term_rule.artifact_id = rule_policy_xref.end1_artifact_id
           AND rule_policy_xref.END1_ARTIFACT_TYPE = 'rule'
           AND rule_policy_xref.END2_ARTIFACT_TYPE = 'policy')
LEFT OUTER JOIN wkcreport.governance_artifacts rule_policy
       ON (rule_policy.artifact_id = rule_policy_xref.end2_artifact_id
           AND rule_policy.artifact_type = 'policy')
WHERE mdluc.ASSET_TYPE = 'model_entry'
--AND gaca.ASSIGNMENT_STATE like 'ASSIGNED' AND mdluc_mdlterm_xr.ASSIGNMENT_STATE like 'ASSIGNED'
AND col_artifact_xref.ASSIGNMENT_STATE like 'ASSIGNED' -- do not include suggested assignments
)
;

SELECT * FROM WKCREPORT.V_MDLUC_JOINS;