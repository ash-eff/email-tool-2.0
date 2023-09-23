import re

def format_customer_information(customer_info):
    remove_all_before_name = re.sub(r'.*Close', 'Name:', customer_info, flags=re.DOTALL)
    remove_create_date_and_beyond = re.sub(r'Create Date:.+', 'Case Creation Date:', remove_all_before_name, flags=re.DOTALL)
    remove_customer_id = re.sub(r'\[(.*?)Voice:', 'Voice:', remove_create_date_and_beyond, flags=re.DOTALL)
    remove_alternative = re.sub(r'Alternative:(.*?)Project State:', 'Project State:', remove_customer_id, flags=re.DOTALL)
    remove_region_code = re.sub(r'Region Code:(.*?)Region:', 'Region:', remove_alternative, flags=re.DOTALL)
    remove_fax = re.sub(r'\bFax:\s*', '', remove_region_code)
    clean_results = remove_fax

    customer_info_lines = clean_results.split('\n')
    filtered_lines = [line for line in customer_info_lines if line.strip()]
    words_to_check = ["Name", "Voice", "Email", "Company", "Project State", "Region", "District Code", "District", "School Code", "Case Creation Date:"]
    formatted_customer_info = []
    skip_next = False
    for i in range(len(filtered_lines)):
        if skip_next:
            skip_next = False
            continue

        line = filtered_lines[i].strip()
        if i + 1 < len(filtered_lines) and not any(filtered_lines[i + 1].strip().startswith(word + ':') for word in words_to_check):
            formatted_customer_info.append(f'{line} {filtered_lines[i + 1].strip()}')
            skip_next = True
        else:
            formatted_customer_info.append(line)

    block_of_customer_info = '\n'.join(formatted_customer_info)
    print(block_of_customer_info)

customer_info_str ="""

 	 
  
 
 
 
 
 
 
 
Edit
 
Close
 
 
 
 
Last, First
[00000000]
 
 
 
 
Voice: 	
15555555555
Email: 	
email@email
Fax: 	
Company: 	
School Name
Alternative: 	
18175478800
Project State: 	
TX
Region Code: 	
11
Region: 	
Region 11 ESC
District Code: 	
000000
District: 	
District Name
School Code: 	
0000
Create Date: 	
03/03/2023 11:17:41
Last Activity: 	
09/08/2023 12:43:57
Comments: 	
 
 
 
EXT 08559
Second Alternative: 15555555555
DTC/DTA/CTC in TIDE 9/8/23
 
 
 
 
Addresses
 
 
 
 
 
Case
 
 
New Case
Switch to unitary view
 
 
Case 1 - 5 of 52
 
1
 
 
 
 
  
#
Open Date
Status
Subject
 
1216608
09/22/2023 10:23:03
REF:RPT
EMail Subject
  
1216576
09/22/2023 09:27:19
Resolved
EMail Subject
  
1212340
09/08/2023 13:13:23
Resolved
EMail Subject
  
1206217
08/22/2023 16:48:26
Resolved
EMail Subject
  
1205952
08/22/2023 11:27:20
Resolved
EMail Subject
  
 
 
 
 
Task
 
 
 
 
 
 
History
 
 
"""

format_customer_information(customer_info_str)