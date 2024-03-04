import os
import math

def create_patch_files(patch_folder, ratio_value, scaling_factor, visual_fixes):

    def make_hex(x, r):
        p = math.floor(math.log(x, 2))
        a = round(16*(p-2) + x / 2**(p-4))
        if a<0: a += 128
        a = 2*a + 1
        h = hex(a).lstrip('0x').rjust(2,'0').upper()
        hex_value = f'0{r}' + h[1] + '02' + h[0] + '1E' 
        print(hex_value)
        return hex_value

    visual_fixesa = visual_fixes[0]
    visual_fixesb = visual_fixes[1]
    scaling_factor = float(scaling_factor)
    ratio_value = float(ratio_value)
    print(f"The scaling factor is {scaling_factor}.")
    hex_value = make_hex(ratio_value, 0)
    hex_value2 = make_hex(ratio_value, 3)
    version_variables = ["1.0.0", "1.0.1"]
    for version_variable in version_variables:
        file_name = f"main-{version_variable}.pchtxt"
        file_path = os.path.join(patch_folder, file_name)

        if version_variable == "1.0.0":
            nsobidid = "37CE685A99F0BC0FB72132C40015F101ECB81C46"
            replacement_value = "008FADE0"
            replacement2_value = "009692D0"
            visual_fix = visual_fixesa

        elif version_variable == "1.0.1":
            nsobidid = "43AE51EE9766867DA5F1272CA0D3D8A60AC53296"
            replacement_value = "008FADE0"
            replacement2_value = "009692D0"
            visual_fix = visual_fixesb

        patch_content = f'''@nsobid-{nsobidid}

@flag print_values
@flag offset_shift 0x100

@enabled
0045fd90 CA719C52
0045fd94 0A03A872
00e71c20 1F2003D5
0003ce68 00902F1E
016b10d8 1F2003D5
00e169c8 C8719C52
00e169cc 0803A872
@stop

{visual_fix}

// Generated using MVDK-AAR by Fayaz (github.com/fayaz12g/mvdk-aar)
// Non 21:9 AR coming soon
// Made possible by Fl4sh_#9174'''
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as patch_file:
            patch_file.write(patch_content)
        print(f"Patch file created: {file_path}")
