import os
import math
from functions import *

def create_patch_files(patch_folder, ratio_value, scaling_factor, visual_fixes):

    visual_fixesa = visual_fixes[0]
    visual_fixesb = visual_fixes[1]
    scaling_factor = float(scaling_factor)
    ratio_value = float(ratio_value)
    print(f"The scaling factor is {scaling_factor}.")
    hex_value = make_hex(1.75, 0)
    hex_value1, hex_value2, hex_value3, hex_value4 = mvdk_hex23(ratio_value)
    version_variables = ["1.0.0", "1.0.1"]
    for version_variable in version_variables:
        file_name = f"main-{version_variable}.pchtxt"
        file_path = os.path.join(patch_folder, file_name)

        if version_variable == "1.0.0":
            nsobidid = "37CE685A99F0BC0FB72132C40015F101ECB81C46"
            visual_fix = visual_fixesa

        elif version_variable == "1.0.1":
            nsobidid = "43AE51EE9766867DA5F1272CA0D3D8A60AC53296"
            visual_fix = visual_fixesb

        patch_content = f'''@nsobid-{nsobidid}

@flag print_values
@flag offset_shift 0x100

@enabled
0045fd90 {hex_value1}
0045fd94 {hex_value2}
00e71c20 1F2003D5
0003ce68 {hex_value}
016b10d8 1F2003D5
00e169c8 {hex_value3}
00e169cc {hex_value4}
@stop

{visual_fix}

// Generated using MVDK-AAR by Fayaz (github.com/fayaz12g/mvdk-aar)
// Made possible by Fl4sh_#9174'''
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as patch_file:
            patch_file.write(patch_content)
        print(f"Patch file created: {file_path}")
