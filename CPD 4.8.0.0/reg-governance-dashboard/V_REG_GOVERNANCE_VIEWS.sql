DROP VIEW WKCREPORT.V_TERM2ASSET_JOIN;
DROP VIEW WKCREPORT.V_FINREP_TERMS_WITH_ASSETS;
DROP VIEW WKCREPORT.V_FINREP_TABLES_WITH_ASSETS;

CREATE VIEW WKCREPORT.V_TERM2ASSET_JOIN AS (
SELECT
    c.NAME container_name,
    c.CONTAINER_TYPE container_type,
    tab.name table_name,
    col.name col_name,
    gov.ARTIFACT_ID gov_artifact_id,
    gov.name gov_artifact_name,
    gov.artifact_type,
    col_artifact_xref.assignment_state
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
)
;

-- Get dimensions, their associated domains, related business terms, assets mapped to the business terms
CREATE VIEW WKCREPORT.V_FINREP_TERMS_WITH_ASSETS AS
(
SELECT 
dim.name dimension_name,
dim.DESCRIPTION dimension_description,
dom.name domain_name,
dom.description domain_description,
ka_dim.name ka_term_name,
ka_dim.DESCRIPTION ka_term_description,
v.TABLE_NAME,
v.COL_NAME,
v.ASSIGNMENT_STATE
FROM 
WKCREPORT.GOVERNANCE_ARTIFACTS dim
LEFT OUTER JOIN WKCREPORT.BUSINESS_TERM_ASSOCIATIONS dim_ka_xref
     ON (dim.ARTIFACT_ID = dim_ka_xref.END1_ARTIFACT_ID AND dim_ka_xref.RELATIONSHIP_TYPE = 'Assigned To')
LEFT outer JOIN WKCREPORT.GOVERNANCE_ARTIFACTS ka_dim
     ON (ka_dim.ARTIFACT_ID = dim_ka_xref.END2_ARTIFACT_ID AND dim_ka_xref.RELATIONSHIP_TYPE = 'Assigned To') 
LEFT OUTER JOIN WKCREPORT.BUSINESS_TERM_ASSOCIATIONS dom_xref
     ON (dim.ARTIFACT_ID = dom_xref.END1_ARTIFACT_ID AND dom_xref.RELATIONSHIP_TYPE = 'is_type_of')
INNER JOIN WKCREPORT.GOVERNANCE_ARTIFACTS dom
     ON (dom.ARTIFACT_ID = dom_xref.END2_ARTIFACT_ID AND dom_xref.RELATIONSHIP_TYPE = 'is_type_of') 
LEFT OUTER JOIN WKCREPORT.V_TERM2ASSET_JOIN v
     ON ka_dim.artifact_id = v.gov_artifact_id
WHERE 
dim.PRIMARY_CATEGORY_ID = '338c1f23-a524-4d9f-a3b3-e4715ea6625d'
)
;

-- This one includes secondary categories, so can filter by finrep table
CREATE VIEW WKCREPORT.V_FINREP_TABLES_WITH_ASSETS AS
(
SELECT 
dim.name dimension_name,
dim.DESCRIPTION dimension_description,
dom.name domain_name,
dom.description domain_description,
ka_dim.name ka_term_name,
ka_dim.DESCRIPTION ka_term_description,
v.TABLE_NAME,
v.COL_NAME,
v.ASSIGNMENT_STATE,
c.name category_name,
c.description category_description
FROM 
WKCREPORT.GOVERNANCE_ARTIFACTS dim
INNER JOIN WKCREPORT.SECONDARY_CATEGORY_ASSOCIATIONS sca
     ON sca.artifact_id = dim.artifact_id
INNER JOIN WKCREPORT.CATEGORIES c
     ON c.category_id = sca.category_id AND c.name LIKE 'F %'
LEFT OUTER JOIN WKCREPORT.BUSINESS_TERM_ASSOCIATIONS dim_ka_xref
     ON (dim.ARTIFACT_ID = dim_ka_xref.END1_ARTIFACT_ID AND dim_ka_xref.RELATIONSHIP_TYPE = 'Assigned To')
LEFT outer JOIN WKCREPORT.GOVERNANCE_ARTIFACTS ka_dim
     ON (ka_dim.ARTIFACT_ID = dim_ka_xref.END2_ARTIFACT_ID AND dim_ka_xref.RELATIONSHIP_TYPE = 'Assigned To') 
LEFT OUTER JOIN WKCREPORT.BUSINESS_TERM_ASSOCIATIONS dom_xref
     ON (dim.ARTIFACT_ID = dom_xref.END1_ARTIFACT_ID AND dom_xref.RELATIONSHIP_TYPE = 'is_type_of')
INNER JOIN WKCREPORT.GOVERNANCE_ARTIFACTS dom
     ON (dom.ARTIFACT_ID = dom_xref.END2_ARTIFACT_ID AND dom_xref.RELATIONSHIP_TYPE = 'is_type_of') 
LEFT OUTER JOIN WKCREPORT.V_TERM2ASSET_JOIN v
     ON ka_dim.artifact_id = v.gov_artifact_id
WHERE dim.PRIMARY_CATEGORY_ID = '338c1f23-a524-4d9f-a3b3-e4715ea6625d'
);

DROP VIEW WKCREPORT.V_FIN_REG_GOVERNANCE;

CREATE VIEW WKCREPORT.V_FIN_REG_GOVERNANCE AS (
SELECT
wkcreport.getIAV(iavPrimeCat.category_id, 'Industry Alignment Vocabularies') Reg_Topic,
wkcreport.getCatPath(iavPrimeCat.CATEGORY_ID) Reg_Category_Path,
iavPrimeCat.NAME Reg_Category,
iavUser.USER_NAME Reg_User, 
iavCatCollab.ROLE Reg_User_Role,
iavTerm.NAME Reg_Term,
kaTerm.NAME KA_Term,
kaTag.TAG_NAME Tag,
kaPrimeCat.NAME KA_Category,
kaUser.USER_NAME KA_User,
kaCatCollab.ROLE KA_Role,
kaSecondCat.NAME Business_Scope,
'not extracted' KA_Secondary_Category_Owner,
'not extracted' KA_Assigned_IAV_Term,
'not extracted' KA_Assigned_IAV_Term_Primary_Category,
'not extracted' KA_Assigned_IAV_Term_Primary_Category_Owner,
assetAssoc.NAME Column,
asset.NAME Table,
contDataAssets.TABLE_SCHEMA Schema,
assetContainer.NAME Catalog,
'not extracted' Connection,
contDataAssets.QUALITY_SCORE Table_Quality_Score,
contDataAssets.NUM_COLUMNS Number_columns,
contDataAssets.NUM_ROWS_ANALYSED Rows_Analysed,
contDataAssets.LAST_PROFILE_TIME Last_Profiled,
column.NAME column_name,
column.QUALITY_SCORE quality_score,
column.REVIEWED_ON reviewed_date,
column.SOURCE_DATA_TYPE source_type,
column.DISTINCT_COUNT distinct_count,
column.UNIQUE_COUNT unique_count,
column.NULL_COUNT null_count,
column.EMPTY_COUNT empty_count,
column.MEAN_LENGTH mean_length,
column.STD_DEVIATION standard_deviation
FROM
WKCREPORT.GOVERNANCE_ARTIFACTS iavTerm
INNER JOIN WKCREPORT.CATEGORIES iavPrimeCat
     ON iavTerm.PRIMARY_CATEGORY_ID = iavPrimeCat.CATEGORY_ID
LEFT OUTER JOIN WKCREPORT.CATEGORY_COLLABORATORS iavCatCollab
     ON iavCatCollab.CATEGORY_ID = iavPrimeCat.Category_ID
LEFT OUTER JOIN WKCREPORT.USER_PROFILES iavUser ON iavUser.USER_ID = iavCatCollab.USER_ID
LEFT OUTER JOIN WKCREPORT.BUSINESS_TERM_ASSOCIATIONS btAssoc
    ON (btAssoc.END1_ARTIFACT_ID = iavTerm.ARTIFACT_ID AND btAssoc.RELATIONSHIP_TYPE = 'Assigned To')
        OR (btAssoc.END2_ARTIFACT_ID = iavTerm.ARTIFACT_ID AND btAssoc.RELATIONSHIP_TYPE = 'Assigned From')
LEFT OUTER JOIN WKCREPORT.GOVERNANCE_ARTIFACTS kaTerm
    ON (btAssoc.END2_ARTIFACT_ID = kaTerm.ARTIFACT_ID AND btAssoc.RELATIONSHIP_TYPE = 'Assigned To')
        OR (btAssoc.END1_ARTIFACT_ID = kaTerm.ARTIFACT_ID AND btAssoc.RELATIONSHIP_TYPE = 'Assigned From')
LEFT OUTER JOIN WKCREPORT.CATEGORIES kaPrimeCat
     ON kaTerm.PRIMARY_CATEGORY_ID = kaPrimeCat.CATEGORY_ID
LEFT OUTER JOIN WKCREPORT.CATEGORY_COLLABORATORS kaCatCollab
     ON kaCatCollab.CATEGORY_ID = kaPrimeCat.Category_ID
LEFT OUTER JOIN WKCREPORT.USER_PROFILES kaUser
     ON kaUser.USER_ID = kaCatCollab.USER_ID
LEFT OUTER JOIN WKCREPORT.SECONDARY_CATEGORY_ASSOCIATIONS kaSecondCatAssoc
    ON kaTerm.ARTIFACT_ID = kaSecondCatAssoc.ARTIFACT_ID
LEFT OUTER JOIN WKCREPORT.CATEGORIES kaSecondCat
    ON kaSecondCatAssoc.CATEGORY_ID = kaSecondCat.CATEGORY_ID
LEFT OUTER JOIN WKCREPORT.DATA_ASSET_COLUMN_ARTIFACT_ASSOCIATIONS assetAssoc
     ON kaTerm.ARTIFACT_ID = assetAssoc.ASSOCIATED_ARTIFACT_ID
LEFT OUTER JOIN WKCREPORT.CONTAINER_DATA_ASSET_COLUMNS column
     ON column.ASSET_ID = assetAssoc.ASSET_ID AND column.CONTAINER_ID = assetAssoc.CONTAINER_ID AND COLUMN.NAME = assetAssoc.NAME
LEFT OUTER JOIN WKCREPORT.CONTAINER_ASSETS asset
     ON assetAssoc.ASSET_ID = asset.ASSET_ID
     AND assetAssoc.CONTAINER_ID = asset.CONTAINER_ID
LEFT OUTER JOIN WKCREPORT.CONTAINER_DATA_ASSETS contDataAsset
     ON contDataAsset.ASSET_ID = asset.ASSET_ID
LEFT OUTER JOIN WKCREPORT.CONTAINER_DATA_ASSETS contDataAssets
     ON contDataAssets.ASSET_ID = asset.ASSET_ID AND contDataAssets.CONTAINER_ID = asset.CONTAINER_ID
LEFT OUTER JOIN WKCREPORT.CONTAINERS assetContainer
     ON assetContainer.CONTAINER_ID = asset.CONTAINER_ID
LEFT OUTER JOIN WKCREPORT.ARTIFACT_TAGS kaTag
   ON kaTag.ARTIFACT_ID = kaTerm.ARTIFACT_ID
LEFT OUTER JOIN WKCREPORT.ARTIFACT_TAGS iavTag     
   ON iavTag.ARTIFACT_ID = iavTerm.ARTIFACT_ID
WHERE
iavTerm.ARTIFACT_TYPE = 'glossary_term'
AND iavTag.TAG_NAME = 'alignment term' 
)
;


DROP VIEW WKCREPORT.V_IAV_OVERLAP_WITH_TOPIC;
DROP VIEW WKCREPORT.V_IAV_OVERLAP;

CREATE VIEW WKCREPORT.V_IAV_OVERLAP AS (
SELECT 
iavTerm1.name Reg1_Term,
iavTerm1.primary_category_id Reg1_primary_category_id,
kaTerm.name KA_Term,
kaCat.name KA_Category,
kaTag.TAG_NAME KA_Tag,
iavTerm2.name Reg2_Term,
iavTerm2.primary_category_id Reg2_primary_category_id
FROM 
wkcreport.GOVERNANCE_ARTIFACTS iavTerm1
-- join to BCV
INNER JOIN WKCREPORT.BUSINESS_TERM_ASSOCIATIONS iavTerm1_bcv_xr
    ON (iavTerm1_bcv_xr.END1_ARTIFACT_ID = iavTerm1.ARTIFACT_ID AND iavTerm1_bcv_xr.RELATIONSHIP_TYPE = 'Assigned To')
        OR (iavTerm1_bcv_xr.END2_ARTIFACT_ID = iavTerm1.ARTIFACT_ID AND iavTerm1_bcv_xr.RELATIONSHIP_TYPE = 'Assigned From')
INNER JOIN WKCREPORT.GOVERNANCE_ARTIFACTS kaTerm
    ON (iavTerm1_bcv_xr.END2_ARTIFACT_ID = kaTerm.ARTIFACT_ID AND iavTerm1_bcv_xr.RELATIONSHIP_TYPE = 'Assigned To' AND kaTerm.ARTIFACT_TYPE = 'glossary_term')
        OR (iavTerm1_bcv_xr.END1_ARTIFACT_ID = kaTerm.ARTIFACT_ID AND iavTerm1_bcv_xr.RELATIONSHIP_TYPE = 'Assigned From' AND kaTerm.ARTIFACT_TYPE = 'glossary_term')
-- join to IAV2
INNER JOIN WKCREPORT.BUSINESS_TERM_ASSOCIATIONS iavTerm2_bcv_xr
    ON (iavTerm2_bcv_xr.END2_ARTIFACT_ID = kaTerm.ARTIFACT_ID AND iavTerm2_bcv_xr.RELATIONSHIP_TYPE = 'Assigned To')
        OR (iavTerm2_bcv_xr.END2_ARTIFACT_ID = kaTerm.ARTIFACT_ID AND iavTerm2_bcv_xr.RELATIONSHIP_TYPE = 'Assigned From')
INNER JOIN WKCREPORT.GOVERNANCE_ARTIFACTS iavTerm2
    ON (iavTerm2_bcv_xr.END1_ARTIFACT_ID = iavTerm2.ARTIFACT_ID AND iavTerm2_bcv_xr.RELATIONSHIP_TYPE = 'Assigned To' AND iavTerm2.ARTIFACT_TYPE = 'glossary_term')
        OR (iavTerm2_bcv_xr.END1_ARTIFACT_ID = iavTerm2.ARTIFACT_ID AND iavTerm2_bcv_xr.RELATIONSHIP_TYPE = 'Assigned From' AND iavTerm2.ARTIFACT_TYPE = 'glossary_term')
INNER JOIN WKCREPORT.CATEGORIES kaCat ON kaCat.CATEGORY_ID = kaTerm.PRIMARY_CATEGORY_ID 
INNER JOIN WKCREPORT.ARTIFACT_TAGS kaTag ON kaTag.ARTIFACT_ID = kaTerm.ARTIFACT_ID
WHERE 
iavTerm1.ARTIFACT_TYPE = 'glossary_term' 
);

CREATE VIEW WKCREPORT.V_IAV_OVERLAP_WITH_TOPIC AS (
SELECT 
o.Reg1_Term,
wkcreport.getIAV(REG1_primary_category_id, 'Industry Alignment Vocabularies') Reg1_Topic, 
o.KA_Term,
o.KA_Tag,
o.KA_Category,
o.Reg2_Term,
wkcreport.getIAV(REG2_primary_category_id, 'Industry Alignment Vocabularies') Reg2_Topic
FROM WKCREPORT.V_IAV_OVERLAP o
)
;