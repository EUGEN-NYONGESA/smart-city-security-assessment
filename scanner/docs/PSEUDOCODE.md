# Pseudocode — AutoVAS Logic

This document describes the complete logic of the program in plain English.
It is the blueprint the actual Python code follows. No syntax — just the
thinking, step by step.

---

## Main Program Flow

START PROGRAM
PRINT welcome banner and disclaimer
---- STEP 1: COLLECT INPUTS ----
ASK user for target IP address

VALIDATE the IP address format

IF invalid THEN

PRINT error and ASK again
ASK user for SSH username

ASK user for SSH password (hidden input)

ASK user for Nessus API access key

ASK user for Nessus API secret key

ASK user for Nessus server URL (default: https://localhost:8834)
CONFIRM all inputs with the user before proceeding
CREATE a unique folder for this assessment's evidence

(named using the target IP and current timestamp)
---- STEP 2: RECONNAISSANCE ----
PRINT "Starting Nmap scan..."

RUN nmap scan against target IP

PARSE the results into a list of open ports and services

CATEGORIZE each service by risk level (Critical/High/Medium/Low)

SAVE the full nmap output as evidence file

SAVE the categorized asset list as evidence file
---- STEP 3: NESSUS SCAN ----
PRINT "Connecting to Nessus..."

AUTHENTICATE with Nessus using API keys

IF authentication fails THEN

PRINT error and EXIT gracefully
CREATE a new scan targeting the IP

LAUNCH the scan
WHILE scan is not finished

WAIT 30 seconds

CHECK scan status

PRINT progress update
ONCE complete:

DOWNLOAD all vulnerability findings

ORGANIZE findings by severity

SAVE the full findings as evidence file
---- STEP 4: MANUAL VALIDATION ----
PRINT "Running manual validation checks..."
TRY anonymous FTP login

RECORD whether it succeeded
TRY SSH connection with provided credentials

RECORD whether it succeeded
TRY PostgreSQL connection with default credentials

RECORD whether it succeeded
CHECK NFS exports

RECORD what is exported
SAVE all validation results as evidence file
---- STEP 5: LOGGING & FIREWALL REVIEW ----
PRINT "Reviewing logging and firewall..."

CONNECT to target over SSH using provided credentials
READ the authentication log

EXTRACT failed login attempts
READ the firewall rules (iptables)
SAVE the logging and firewall findings as evidence file

DISCONNECT from SSH
---- STEP 6: GENERATE REPORT ----
PRINT "Generating report..."

GATHER all collected data:

- asset list

- nessus findings

- validation results

- logging/firewall review
BUILD the report following the 8-section structure

SAVE the report as a .txt file

SAVE the report as a .docx file
---- DONE ----
PRINT "Assessment complete!"

PRINT location of evidence folder

PRINT location of generated reports
END PROGRAM

---

## Module Logic Breakdown

### inputs.py

FUNCTION collect_inputs():

GET target IP, validate format

GET SSH username

GET SSH password (hidden)

GET Nessus keys and URL

RETURN all inputs as a structured object
FUNCTION validate_ip(ip):

CHECK ip matches the pattern X.X.X.X

CHECK each number is between 0 and 255

RETURN true or false

### recon.py

FUNCTION run_nmap(target_ip):

EXECUTE nmap with version and OS detection

RETURN raw output
FUNCTION parse_services(nmap_output):

FOR each line in output:

EXTRACT port, service name, version

RETURN list of services
FUNCTION categorize_assets(services):

FOR each service:

LOOK UP its known risk level

ASSIGN it to a category

RETURN categorized dictionary

### nessus.py
FUNCTION authenticate(url, access_key, secret_key):

BUILD authentication headers

TEST connection

RETURN headers or raise error
FUNCTION create_scan(headers, url, target):

FIND the "Basic Network Scan" template

CREATE scan with target IP

RETURN scan ID
FUNCTION launch_and_wait(headers, url, scan_id):

LAUNCH the scan

LOOP until status is "completed":

WAIT and re-check

RETURN when done
FUNCTION get_findings(headers, url, scan_id):

REQUEST the scan results

PARSE vulnerabilities by severity

RETURN organized findings

### validation.py

FUNCTION test_anonymous_ftp(target):

ATTEMPT ftp login as "anonymous"

RETURN success or failure with details
FUNCTION test_ssh(target, username, password):

ATTEMPT ssh login

RETURN success or failure with details
FUNCTION test_postgres(target):

ATTEMPT connection with default credentials

RETURN success or failure with details
FUNCTION check_nfs(target):

RUN showmount to list exports

RETURN what is exported

### logging_review.py

FUNCTION review_system(target, username, password):

CONNECT over SSH

READ auth log, extract failed logins

READ iptables rules

DISCONNECT

RETURN logging and firewall findings

### evidence.py

FUNCTION save_evidence(folder, filename, content):

WRITE content to a .txt file in the evidence folder

PRINT confirmation


### report.py

FUNCTION generate_txt_report(all_data, output_path):

BUILD the 8-section report as text

WRITE to .txt file
FUNCTION generate_docx_report(all_data, output_path):

BUILD the 8-section report as a Word document

WRITE to .docx file

---

## Error Handling Philosophy

At every step, the program should:

- **Fail gracefully** — never crash with a confusing error
- **Inform the user** — explain what went wrong in plain language
- **Save what it can** — if one step fails, preserve earlier evidence
- **Continue where safe** — a failed validation check shouldn't stop
  the whole assessment

---

## Why This Order?

The steps follow the same logical flow as a real manual assessment:

1. **Recon first** — you must know what's there before scanning deeply
2. **Nessus next** — automated deep scan of discovered services
3. **Validation** — confirm the automated findings are real
4. **Logging review** — check detection and response capabilities
5. **Report last** — synthesize everything into a deliverable

This mirrors the exact process documented in the main repository
walkthrough, making the program a direct automation of the manual lab.

