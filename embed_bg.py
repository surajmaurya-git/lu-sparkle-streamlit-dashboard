import base64
import os

css_path = "css/style.css"
image_path = "images/smart_ro_bg.png"

with open(image_path, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()

css_rule = f'''
/* Background Image with Overlay (Base64 Encoded) */
.stApp {{
    background-image: linear-gradient(rgba(15, 23, 42, 0.85), rgba(15, 23, 42, 0.95)), url("data:image/png;base64,{encoded_string}") !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
}}
'''

with open(css_path, "r") as f:
    css_content = f.read()

# Replace the existing .stApp rule or append if not easily replaceable regex-wise
# For safety, let's just replace the block we wrote earlier
start_marker = "/* Background Image with Overlay */"
end_marker = "background-attachment: fixed !important;\n}"

if start_marker in css_content:
    # Simple replacement if the previous content matches what we expect
    # To be robust, let's just re-write the file with the new rule replacing the old one logic
    pass

# safer approach: Read all lines, remove the .stApp block, append new one
new_lines = []
skip = False
with open(css_path, "r") as f:
    for line in f:
        if "/* Background Image with Overlay */" in line:
            skip = True
        if skip and "}" in line:
            skip = False
            continue
        if not skip:
            new_lines.append(line)

with open(css_path, "w") as f:
    f.writelines(new_lines)
    f.write(css_rule)

print("CSS updated with Base64 background.")
