#!/bin/bash

# Ensure an argument is passed
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <infrastructure_desc_filename>"
  exit 1
fi

# Set input argument
input_filename=$1

# Generate dynamic filenames
benchmark_if_prompt="${input_filename}"
benchmark_if_output="${input_filename}_IF_Output"
benchmark_audit_payload="${input_filename}_Audit_Payload"
benchmark_audit_userinput="${input_filename}_Audit_UserInput"
benchmark_audit_output="${input_filename}_Audit_Output"

# Global variable for benchmark_Audit_Prompt (can be set/modified elsewhere)
benchmark_audit_prompt="benchmark_Audit_Prompt"

# Navigate to agents directory
cd ~/agents/

# Run IFAgent.py with dynamic input and output filenames
python3 IFAgent.py "${benchmark_if_output}" < "${benchmark_if_prompt}"

# Process benchmark_IF_Output with ejf.sh and create the audit payload
cat "${benchmark_if_output}" | ~/tools/ejf.sh ~/agents/"${benchmark_audit_payload}"

# Combine Audit Prompt and Payload, remove newlines and create user input
cat "${benchmark_audit_prompt}" "${benchmark_audit_payload}" | ~/tools/removenewlines.sh "${benchmark_audit_userinput}"

# Run IFAuditor.py with the dynamic user input and output filenames
python3 IFAuditor.py "${benchmark_audit_output}" < "${benchmark_audit_userinput}"

# Display the final audit output
cat "${benchmark_audit_output}"

