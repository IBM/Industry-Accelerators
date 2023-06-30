#!/bin/bash

#################################################################################################################################################
# Copyright IBM Corp. 2020,2021
# All Rights Reserved
#################################################################################################################################################

# Log handling function

clear


log_msg()
{
        declare l_sev=$1
        declare l_msg=$2
        declare l_logfile=$3
        TIMESTAMP=`date "+%Y-%m-%d-%H:%M:%S"`

        RED='\033[0;31m'
        NC='\033[0m' # No Color
        GREEN='\033[32m'
	YELLOW='\033[33m'

        case $l_sev in
                "ERROR") l_colour=$RED ;;
		"WARNING") l_colour=$YELLOW ;;
                "SUCCESS") l_colour=$GREEN ;;
                *) l_colour=$NC ;;
        esac

        echo -e "${l_colour}[$TIMESTAMP][$l_sev] : $l_msg ${NC}" >> $l_logfile
        echo -e "${l_colour}[$l_sev] : $l_msg ${NC}"
}

#################################################################################################################################################
# Process command line arguments and flag parameters
#################################################################################################################################################

for arg in "$@"
do
	case $arg in
		
                -h|--hostname)
                        CPD_HOST="$2"
                        shift
			shift
                        ;;
                -u|--username)
                        username="$2"
                        shift
			shift
                        ;;
                -p|--password)
                        password="$2"
                        shift
			shift
                        ;;
                -n|--name)
                        analytics_project="$2"
                        shift	
			shift
                        ;;
		#-j|--run_jobs)
		#	run_notebook_jobs="Y"
		#	shift
		#	;;
		-v|--version)
			 echo
			 echo "[INFO] : Industry Accelerator Import Script - Version 3.0"
			 shift
			 exit 0
			 ;;
		--help) 
			            echo
			            echo "Cloud Pak for Data - Industry Accelerator Import"
			            echo 
			            echo
			            echo "Usage: ./import-acclerator-script.sh [flags]"
			            echo
			            echo 
			            echo "Flags :"
			            echo
			
			            echo "       -h, --hostname          :   The host URL of the Cloud Pak for Data cluster e.g. https://<hostname:port>"
			            echo "       -u, --username          :   The username for the Cloud Pak for Data cluster"
			            echo "       -p, --password          :   The password for the Cloud Pak for Data cluster"
			            echo "       -n, --name              :   The name you wish to use for the analytics project"
			            echo "       -v, --version           :   Display version information for this script"
			
			#            echo "       -j, --run_jobs          :   Execute the notebook jobs specified in the analytics project during the import process (optional)"
			            echo "           --help              :   Help for accelerator import process"
			            echo

			            echo "These arguments are optional and can be declared in any order."
			            echo "You can also execute the script without arguments, in which case you will be prompted for the required information."
			            echo
			            echo "Example syntax without arguments..."
			            echo
			            echo "Example syntax Bash Users : ./import-accelerator-script.sh "
			            echo "Example syntax Windows Users : bash -c ./import-accelerator-script.sh "
			            echo
			            echo "Example syntax if you have extracted the .tar.gz file and are executing the import script that was included..."
			            echo "Note that in this scenario the script and the artefacts are in the same path"
			            echo "Example syntax Bash Users : ./import-accelerator-script.sh --hostname https://hostname:port --username username --password password --name name-of-project"
                        echo "Example syntax Windows Users : bash -c ./import-accelerator-script.sh --hostname https://hostname:port --username username --password password --name name-of-project"
			            echo
			            #echo "Example syntax if you are importing an unextracted .tar.gz file (this method can be useful if you have multiple .tar.gz files to process..."
			            #echo "Example syntax Bash Users : ./import-accelerator-script.sh --file accelerator-file-name.tar.gz --hostname https://hostname:port --username username --password password --name name-of-project"
			            #echo "Example syntax Windows Users : bash -c ./import-accelerator-script.sh --file accelerator-file-name.tar.gz --hostname https://hostname:port --username username --password password --name name-of-project"
			            shift
			            exit 0
			            ;;
		        $1)
			            echo "[ERROR] : Invalid parameter(s). User --help argument to get assistance on usage of the parameter(s)."
			            exit 0
			            shift
			            ;;
	    esac
done

echo


##################################################################################################################################
# Notebook Job Run section
##################################################################################################################################
# Set accelerator name & create logfile

TIMESTAMP=`date "+%Y-%m-%d-%H:%M:%S"`
logtime=$TIMESTAMP
current_path=$PWD



while [[ -z "$analytics_project" ]]
do 
    
	echo
	echo "[INFO] : Please enter name of the accelerator. "
	echo "[INFO] : Run ./import-accelerator.sh --help for further help."
	echo
	read -t300 -p ' Enter Accelerator Name : ' analytics_project
	
	if [[ $? -gt 300 || -z "$analytics_project" ]]
        then
                echo
                log_msg "ERROR" "No input entered by user for username. Aborting import..." "$logfile"
           	     
                exit 0
        fi
done

accelerator_name=$analytics_project
accelerator=${analytics_project%-industry-accelerator}
project_zipfile="$current_path/$analytics_project.zip"
logfile=$accelerator-$logtime.log

#echo zipfile : $project_zipfile
#echo accelerator name : $accelerator_name
#echo accelerator : $accelerator 


if [[ ! -f $project_zipfile ]]
then
    echo
	log_msg "ERROR" "Aborting as analytics project file does not exist. Download the zip file and try again." "$logfile"
	exit 0

elif [[ -z "$project_zipfile" ]]
then 
	echo
	log_msg "INFO" "Please ensure that the script and the accelerator zip file are in the same directory and try again." "$logfile"
	rm -rf output.txt
	exit 0

elif [[  `stat -c %s $project_zipfile` == 0 ]]
then
	echo
	log_msg "WARNING" "The analytics project is empty. Aborting..." "$logfile"
  	rm -rf output.txt
	exit 0
fi

log_msg "INFO" "$accelerator_name import process" "$logfile"
log_msg "INFO" "Starting script...." "$logfile"

#if [[ $run_notebook_jobs == 'Y' ]]
#then
#        log_msg "WARNING" "Note that the notebook job run duration may vary from 8 to 15 minutes depending on the accelerator and CPD cluster..." "$logfile"

#fi


#################################################################################################################################################
# Config section & argument checks
#################################################################################################################################################
# Check host is reachable

while [[ -z "$CPD_HOST" ]]
do 
	echo
   	# Read Variables from User
	echo "[INFO] : Script parameter Cloud Pak for Data Hostname required." 
	echo "[INFO] : Run ./import-accelerator.sh --help for further help."
   	echo "Enter host URL for your Cloud Pak for Data Cluster in this format : https://<hostname:port> "
	echo
 	read -t300 -p 'Enter Host URL : ' CPD_HOST
	if [[ $? -gt 300 || -z "$CPD_HOST" ]]
        then
                echo
                log_msg "ERROR" "No input entered by user for host URL. Aborting import..." "$logfile"
                exit 0
        fi

done

if [[ $CPD_HOST != https://* ]]
then
	CPD_HOST=https://$CPD_HOST
fi

if [[ $CPD_HOST == */ ]] 
then
 	CPD_HOST=${CPD_HOST%?}
fi

# Cluster Sanity Check 

if curl -k --output /dev/null --silent --head --fail "$CPD_HOST"; then
	echo
	log_msg "INFO" "Cloud Pak for Data cluster exists and is reachable... " "$logfile" 
else
	echo
	log_msg "ERROR" "Cannot reach Cloud Pak for Data cluster..." "$logfile"
	exit 0
fi

# Endpoint & headers for authentication

declare -a authURL="${CPD_HOST}/icp4d-api/v1/authorize"

declare -a curlArgs1=('-H' "Content-Type: application/json" \
        '-H' "cache-control: no-cache")


#################################################################################################################################################
# Gather host and credentials
#################################################################################################################################################

while [[ -z "$username" ]]
do 
	echo
	echo "[INFO] : Script parameter Username required. "
	echo "[INFO] : Run ./import-accelerator.sh --help for further help."
	read -t300 -p 'Enter USERNAME : ' username
	if [[ $? -gt 300 || -z "$username" ]]
        then
                echo
                log_msg "ERROR" "No input entered by user for username. Aborting import..." "$logfile"
                exit 0
        fi
done

while [[ -z "$password" ]]
do
	echo
	echo "[INFO] : Script parameter Password required. "
	echo "[INFO] : Run ./import-accelerator.sh --help for further help."
    	read -t300 -sp 'Enter PASSWORD : ' password
	if [[ $? -gt 300 || -z "$password" ]]
        then
                echo
                log_msg "ERROR" "No input entered by user for password. Aborting import..." "$logfile"
                exit 0
        fi

done


#################################################################################################################################################
# Check authentication is successful
#################################################################################################################################################

credentials='{"username":"'$username'","password":"'$password'"}'

HTTP_CODE=$(curl -s --write-out "%{http_code}\n" -k -X POST "${curlArgs1[@]}" \
                -d "$credentials" \
                 ${authURL} \
		--output output.txt) 


if [[ $HTTP_CODE == 200 ]]
then
	echo
	log_msg "SUCCESS" "Authentication completed and successful..." "$logfile"

else
	echo
	log_msg "ERROR" "Authentication check returned error... $HTTP_CODE" "$logfile"
	log_msg "ERROR" "Please check your username/password. Please also check your Cloud Pak for Data Host URL." "$logfile"
	rm -rf output.txt
	exit 0 
fi

#################################################################################################################################################
# Check if user has required permissions to import the accelerator
#################################################################################################################################################

echo
json=$(curl -s -k "$authURL" \
            -X POST "${curlArgs1[@]}" \
            -d "$credentials") \
   		&& token=$(echo $json | sed "s/{.*\"token\":\"\([^\"]*\).*}/\1/g") \
	

log_msg "INFO" "Checking for user permissions...." "$logfile"

user_permissions=$(curl -s -k -X GET -H "Authorization: Bearer $token" \
        	-H "cache-control: no-cache" "${CPD_HOST}/icp4d-api/v1/users/$username")

#if echo $user_permissions | grep -q  -e "Administrator" -e "Data Steward" -e "Data Engineer" -e "Data Quality Analyst" -e "zen_administrator_role" -e "wkc_data_steward_role" -e "wkc_data_scientist_role" -e "zen_data_engineer_role" 
if echo $user_permissions | grep -q -e "Developer" -e "Business Analyst" -e "Data Scientist" -e "zen_developer_role" -e "wkc_business_analyst_role" -e "wkc_data_scientist_role" 
then
	echo
   	log_msg "INFO" "User has necessary privileges for project import and execution." "$logfile"
	project_import_flag=1

else
	log_msg "ERROR" "Aborting as Permissions not sufficient to import or execute a project." "$logfile"
	project_import_flag=0
	rm -rf output.txt
        exit 0
fi

#################################################################################################################################################
# Provide name for project and start import of project
#################################################################################################################################################

if [[ $project_import_flag == 1 ]]
then
	echo
	log_msg "INFO" "Starting accelerator import process..." "$logfile"

	
	#if [[ -z "$analytics_project" ]]
 	#then
  	#	echo "[INFO] : Optional script parameter project name required."
	#	echo "[INFO] : Run ./import-accelerator.sh --help for further help."
  	#	read -t 30 -p 'Enter a name for the analytics project. If no name is entered, the script will auto-generate a name : ' project
		
	#	if [[ ! -z "$project" ]]
 	#	then
   	#		analytics_project=$project
  	#	else
   	#		analytics_project=$accelerator_name
  	#	fi
 	#fi
	#echo $analytics_project
	#exit 0
	if [[ ${#analytics_project} -gt 95 ]]
	then 
		log_msg "WARNING" "Project name too large." "$logfile"
		analytics_project=`echo ${analytics_project:0:95}`
		log_msg "INFO" "Project name has been trimmed down to $analytics_project" "$logfile"
	fi 
 	

	# analytics project metadata
 	METADATA='metadata={
  		"name": "'${analytics_project}'",
  		"description": "Industry Accelerator.",
  		"generator": "IndAcc-Projects",
  		"public": false,
  		"tags": [
    			"string"
  			],
  		"storage": {
    			"type": "assetfiles",
    			"guid": "d0e410a0-b358-42fc-b402-dba83316413b"
   			}
 		}'


 	if [[ -z "${METADATA}" ]]; then
    		log_msg "ERROR" "Metadata generation failed." "$logfile"
    		rm -rf output.txt
    		exit 0 
 	else 
		log_msg "INFO" "Metadata created for project." "$logfile"
 	fi

 	declare -a metadata="${METADATA}"
	
 	# endpoint and headers for analytics project import
 	if [ $HTTP_CODE == 200 ]
 	then
  		declare -a curlArgs2=('-H' "Authorization: Bearer $token" \
 			'-H' "content-type:multipart/form-data")

  		log_msg "INFO" "Importing the analytics project..." "$logfile"
		

  		http_proj=$(curl -s --write-out "%{http_code}\n" -X POST -k \
    			"${CPD_HOST}/transactional/v2/projects" \
    			"${curlArgs2[@]}" \
    			-F file=@$project_zipfile \
    			-F "$metadata" \
    				--output output.txt )

    		echo "$TIMESTAMP">>$logfile
		cat output.txt>>$logfile
	
  		if [[ $http_proj == 202 ]]
  		then
			log_msg "INFO" "Importing Project Artefacts..." "$logfile"
			guid=$(cat output.txt | grep -Po '"location":"\K[^"]*' | awk -F / '{print $4}')	
			trans_id=$(cat output.txt | sed "s/{.*\"id\":\"\([^\"]*\).*}/\1/g")	
        
 	 	elif [[ $http_proj == 400 ]]
  		then 
			echo
   			log_msg "WARNING" "Project with this name already exists.... $http_proj" "$logfile"
			log_msg "WARNING" "Attempting to import with unique name..." "$logfile"

   			while [[ $http_proj == 400 ]]
   			do 	
				current_version=$analytics_project
				n=${current_version##*[!0-9]}; p=${current_version%%$n}
				analytics_project=$p$((n+1))
				METADATA='metadata={
  					"name": "'${analytics_project}'",
			  		"description": "Industry Accelerator.",
  					"generator": "IndAcc-Projects",
  					"public": false,
					"tags": [
    						"string"
  						],
					"storage": {
				    		"type": "assetfiles",
				    		"guid": "d0e410a0-b358-42fc-b402-dba83316413b"
				 	 	}
					}'
				declare -a metadata="${METADATA}"

				http_proj=$(curl -s --write-out "%{http_code}\n" -X POST -k \
	  				"${CPD_HOST}/transactional/v2/projects" \
	  				"${curlArgs2[@]}" \
	  				-F file=@$project_zipfile \
	  				-F "$metadata" \
   	     					--output output.txt )
				echo "$TIMESTAMP">>$logfile
				
				if [[ $http_proj == 202 ]]
				then 
	        			cat output.txt>>$logfile
					guid=$(cat output.txt | grep -Po '"location":"\K[^"]*' | awk -F / '{print $4}')
				fi
				trans_id=$(cat output.txt | sed "s/{.*\"id\":\"\([^\"]*\).*}/\1/g")
				
	   		done
			  
			log_msg "INFO" "Project with this name created : $analytics_project" "$logfile"	
	
  		else 
			echo
   			log_msg "ERROR" "Aborting Import... failed to create $http_proj" "$logfile"
   			rm -rf output.txt
   			exit 0 
  		fi 

 	else
		echo
  		log_msg "ERROR" "Aborting Import... incorrect details/cluster unreachable. $HTTP_CODE " "$logfile"
  		rm -rf output.txt
  		exit 0 
 	fi
	
	echo
 	log_msg "SUCCESS" "Analytics project imported...." "$logfile"
	
 	
fi


################## END OF NOTEBOOK JOB SECTION #####################

rm -rf output.txt
echo
echo 
######################################################################################################################################
#			SUMMARY SECTION FOR IMPORT PROCESS
######################################################################################################################################

log_msg "INFO" "INDUSTRY ACCELERATOR IMPORT PROCESS SUMMARY" "$logfile"
echo

log_msg "INFO" "Host Cluster URL : $CPD_HOST" "$logfile"
log_msg "INFO" "Cloud Pak for Data username : $username" "$logfile"

if [[ $project_import_flag == 1 ]]
then 
	log_msg "INFO" "Imported analytics project name : $analytics_project" "$logfile"
	log_msg "INFO" "Project Link : $CPD_HOST/projects/$guid" "$logfile" 
fi


#if [[ $run_all_notebook_jobs == 1 && $notebook_status != "Failed" && $dashboard_link != "" && $notebook_exe != 99 ]]
#then
#	log_msg "INFO" "All notebook jobs have run successfully." "$logfile"
#	log_msg "INFO" "Dashboard link : $dashboard_link" "$logfile"
#fi

echo
echo "[INFO] : Please visit the Cloud Pak for Data cluster above to access all the imported artefacts. View "$logfile" to view the import process log."
echo
