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
    version_variables = ["1.0.0", "1.1.0"]
    for version_variable in version_variables:
        file_name = f"main-{version_variable}.pchtxt"
        file_path = os.path.join(patch_folder, file_name)

        if version_variable == "1.0.0":
            nsobidid = "9F7EFC2FB9653E5CDE03030478F23EDA7D18EF44"
            replacement_value = "008FADE0"
            replacement2_value = "009692D0"
            visual_fix = visual_fixesa

        elif version_variable == "1.1.0":
            nsobidid = "9F7EFC2FB9653E5CDE03030478F23EDA7D18EF44"
            replacement_value = "008FADE0"
            replacement2_value = "009692D0"
            visual_fix = visual_fixesb

        patch_content = f'''@nsobid-{nsobidid}

@flag print_values
@flag offset_shift 0x100

@enabled
{replacement_value} {hex_value}
{replacement2_value} {hex_value2}
0091CFC8 A9AA8AD2
0091CFCC A902A8F2
008B6C1C A8AA8A52
008B6C20 A802A872
@stop

{visual_fix}

// Generated using SMO-AAR by Fayaz (github.com/fayaz12g/sm3dw-aar)'''
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as patch_file:
            patch_file.write(patch_content)
        print(f"Patch file created: {file_path}")
