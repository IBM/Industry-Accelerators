DROP VIEW WKCREPORT.V_TABLE_CLASSIF_TERM_RULE_POLICY;

CREATE VIEW WKCREPORT.V_TABLE_CLASSIF_TERM_RULE_POLICY AS
(
SELECT 
c.NAME container_name,
tab.name table_name,
class.name table_classification,
gaca_term.assignment_state,
term.name table_term_name,
rule.name rule_name,
policy.name policy_name
FROM WKCREPORT.CONTAINERS c
INNER JOIN WKCREPORT.CONTAINER_ASSETS tab
   ON c.CONTAINER_ID = tab.CONTAINER_ID
LEFT OUTER JOIN WKCREPORT.GOVERNANCE_ARTIFACT_CONTAINER_ASSOCIATIONS ass_class_xr
       ON ass_class_xr.CONTAINER_ID = tab.CONTAINER_ID
       AND ass_class_xr.ASSET_ID = tab.ASSET_ID
       AND ass_class_xr.ASSOCIATED_ARTIFACT_TYPE = 'classification'
LEFT OUTER JOIN wkcreport.governance_artifacts class 
       ON class.ARTIFACT_ID = ass_class_xr.ASSOCIATED_ARTIFACT_ID
       AND class.ARTIFACT_TYPE = ass_class_xr.ASSOCIATED_ARTIFACT_TYPE
       AND class.ARTIFACT_TYPE = 'classification'
-- joins to asset term
LEFT OUTER JOIN WKCREPORT.GOVERNANCE_ARTIFACT_CONTAINER_ASSOCIATIONS gaca_term
       ON gaca_term.CONTAINER_ID = tab.CONTAINER_ID
       AND gaca_term.ASSET_ID = tab.ASSET_ID
       AND gaca_term.ASSOCIATED_ARTIFACT_TYPE = 'glossary_term'
       AND gaca_term.ASSIGNMENT_STATE = 'ASSIGNED'
LEFT OUTER JOIN wkcreport.governance_artifacts term 
       ON term.ARTIFACT_ID = gaca_term.ASSOCIATED_ARTIFACT_ID
       AND term.ARTIFACT_TYPE = gaca_term.ASSOCIATED_ARTIFACT_TYPE
-- joins to term rule
LEFT OUTER JOIN wkcreport.governance_artifact_associations term_rule_xref
       ON (term.artifact_id = term_rule_xref.end2_artifact_id
       AND term_rule_xref.END2_ARTIFACT_TYPE = 'glossary_term'
       AND term_rule_xref.END1_ARTIFACT_TYPE = 'rule')
LEFT OUTER JOIN wkcreport.governance_artifacts rule 
       ON (rule.artifact_id = term_rule_xref.end1_artifact_id
           AND rule.artifact_type = 'rule')
       OR (rule.artifact_id = term_rule_xref.end2_artifact_id
           AND rule.artifact_type = 'rule')
-- joins to rule policy
LEFT OUTER JOIN wkcreport.governance_artifact_associations rule_pol_xref 
       ON (rule.artifact_id = rule_pol_xref.end2_artifact_id
           AND rule_pol_xref.END2_ARTIFACT_TYPE = 'rule'
           AND rule_pol_xref.END1_ARTIFACT_TYPE = 'policy')
       OR (rule.artifact_id = rule_pol_xref.end1_artifact_id
           AND rule_pol_xref.END1_ARTIFACT_TYPE = 'rule'
           AND rule_pol_xref.END2_ARTIFACT_TYPE = 'policy')
LEFT OUTER JOIN wkcreport.governance_artifacts policy 
       ON (policy.artifact_id = rule_pol_xref.end1_artifact_id
           AND policy.artifact_type = 'policy')
       OR 
          (policy.artifact_id = rule_pol_xref.end2_artifact_id
           AND policy.artifact_type = 'policy')      
WHERE 
tab.asset_type = 'data_asset'
);

