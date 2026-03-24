import re
import xml.etree.ElementTree as ET
import os

try:
    base_path = os.path.dirname(os.path.abspath(__file__))

    config_path = os.path.join(base_path, "config.xml")
    log_path = os.path.join(base_path, "logdata.txt")
    output_path = os.path.join(base_path, "output.txt")

    tree = ET.parse(config_path)
    root = tree.getroot()

    with open(log_path, "r", encoding="utf-8") as f:
        log_data = f.read()

    main_patterns = {}
    for main in root.findall("mainRE"):
        main_patterns[main.get("name")] = main.text.strip()

    sub_patterns = {}
    for sub in root.findall("subRE"):
        sub_patterns[sub.get("name")] = sub.text.strip()

    output_lines = []

    for server_name, server_pattern in main_patterns.items():

        matches = list(re.finditer(server_pattern, log_data))

        for match in matches:
            start = match.end()
            block = log_data[start:start + 9000]

            output_lines.append(f"\n===== {server_name} =====")

            for sub_name, sub_pattern in sub_patterns.items():
                sub_match = re.search(sub_pattern, block, re.IGNORECASE)
                if sub_match:
                    output_lines.append(f"{sub_name}: {sub_match.group(1).strip()}")
                else:
                    output_lines.append(f"{sub_name}: Not Found")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

    print(" Extraction Completed Successfully!")
    print(" Output file created at:", output_path)

except PermissionError:
    print(" Close output.txt if open and run again.")

except Exception as e:
    print(" Error:", str(e))

