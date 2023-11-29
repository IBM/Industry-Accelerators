DROP VIEW WKCREPORT.V_POLICY_RULE_TERM_ASSET_CLASSIF;

CREATE VIEW WKCREPORT.V_POLICY_RULE_TERM_ASSET_CLASSIF AS
(
SELECT 
policy.name policy_name,
rule.name rule_name,
term.name table_term_name,
gaca_term.assignment_state,
tab.name table_name,
class.name table_classification,
c.NAME container_name
FROM 
wkcreport.governance_artifacts policy 
--JOIN TO RULE
LEFT OUTER JOIN wkcreport.governance_artifact_associations rule_pol_xref 
       ON (policy.artifact_id = rule_pol_xref.end2_artifact_id
           AND rule_pol_xref.END2_ARTIFACT_TYPE = 'policy'
           AND rule_pol_xref.END1_ARTIFACT_TYPE = 'rule')
LEFT OUTER JOIN wkcreport.governance_artifacts rule 
       ON (rule.artifact_id = rule_pol_xref.end1_artifact_id
           AND rule.artifact_type = 'rule')
       OR (rule.artifact_id = rule_pol_xref.end2_artifact_id
           AND rule.artifact_type = 'rule')
--JOIN FROM RULE TO TERM
LEFT OUTER JOIN wkcreport.governance_artifact_associations term_rule_xref
       ON (rule.artifact_id = term_rule_xref.end1_artifact_id
       AND term_rule_xref.END1_ARTIFACT_TYPE = 'rule'
       AND term_rule_xref.END2_ARTIFACT_TYPE = 'glossary_term')
LEFT OUTER JOIN wkcreport.governance_artifacts term
       ON (term.artifact_id = term_rule_xref.end1_artifact_id
           AND term.artifact_type = 'glossary_term')
       OR (term.artifact_id = term_rule_xref.end2_artifact_id
           AND term.artifact_type = 'glossary_term')
-- JOIN FROM TERM TO ASSET
LEFT OUTER JOIN WKCREPORT.GOVERNANCE_ARTIFACT_CONTAINER_ASSOCIATIONS gaca_term
       ON gaca_term.ASSOCIATED_ARTIFACT_ID = term.artifact_id 
           AND term.ARTIFACT_TYPE = gaca_term.ASSOCIATED_ARTIFACT_TYPE
LEFT OUTER JOIN WKCREPORT.CONTAINER_ASSETS tab
       ON gaca_term.ASSET_ID = tab.ASSET_ID
          AND gaca_term.CONTAINER_ID = tab.CONTAINER_ID
          AND gaca_term.ASSOCIATED_ARTIFACT_TYPE = 'glossary_term'
          --AND gaca_term.ASSIGNMENT_STATE = 'ASSIGNED'
-- JOIN FROM ASSET TO CLASSIFICATION
LEFT OUTER JOIN WKCREPORT.GOVERNANCE_ARTIFACT_CONTAINER_ASSOCIATIONS ass_class_xr
       ON ass_class_xr.CONTAINER_ID = tab.CONTAINER_ID
       AND ass_class_xr.ASSET_ID = tab.ASSET_ID
       AND ass_class_xr.ASSOCIATED_ARTIFACT_TYPE = 'classification'
LEFT OUTER JOIN wkcreport.governance_artifacts class 
       ON class.ARTIFACT_ID = ass_class_xr.ASSOCIATED_ARTIFACT_ID
       AND class.ARTIFACT_TYPE = ass_class_xr.ASSOCIATED_ARTIFACT_TYPE
       AND class.ARTIFACT_TYPE = 'classification'          
LEFT OUTER JOIN WKCREPORT.CONTAINERS c
       ON c.CONTAINER_ID = tab.CONTAINER_ID
WHERE policy.ARTIFACT_TYPE = 'policy'
)
;
