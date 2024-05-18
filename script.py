import os
import struct
from functions import *

def patch_blarc(aspect_ratio, HUD_pos, unpacked_folder):
    unpacked_folder = str(unpacked_folder)
    aspect_ratio = float(aspect_ratio)
    print(f"Aspect ratio is {aspect_ratio}")
    HUD_pos = str(HUD_pos)

    file_paths = {}

    def patch_blyt(filename, pane, operation, value):
        if operation == "scale_x" or operation == "scale_y":
            if value < 1:
                command = "Squishing"
            if value > 1:
                command = "Stretching"
            if value == 1:
                command = "Ignoring"
        if operation == "shift_x" or operation == "shift_y":
            command = "Shifting"

        print(f"{command} {pane} of {filename}")
        offset_dict = {'shift_x': 0x40, 'shift_y': 0x48, 'scale_x': 0x70, 'scale_y': 0x78} 
        modified_name = filename + "_name"
        full_path_of_file = file_paths.get(modified_name)
        with open(full_path_of_file, 'rb') as f:
            content = f.read().hex()
        start_rootpane = content.index(b'RootPane'.hex())
        pane_hex = str(pane).encode('utf-8').hex()
        start_pane = content.index(pane_hex, start_rootpane)
        idx = start_pane + offset_dict[operation]
        content_new = content[:idx] + float2hex(value) + content[idx+8:]
        with open(full_path_of_file, 'wb') as f:
            f.write(bytes.fromhex(content_new))


    def patch_anim(folder, filename, offset, value):
        full_path = os.path.join(unpacked_folder, 'romfs', 'LayoutData', folder, 'layout', 'anim', f'{filename}.bflan') 
        with open(full_path, 'rb') as f:
            content = f.read().hex()
        idx = offset
        content_new = content[:idx] + float2hex(value) + content[idx+8:]
        with open(full_path, 'wb') as f:
            f.write(bytes.fromhex(content_new))  
            
    blyt_folder = os.path.abspath(os.path.join(unpacked_folder))
    file_names_stripped = []
    
    do_not_scale_rootpane = ["Loading_00", "Saving_00", "Pa_LoadingBlocks_00", "SceneChangeFade_00", "MenuBackground_00", "Pa_BlurBackground"]
   
    rootpane_by_y = ["MenuBackground_00"]

    for root, dirs, files in os.walk(blyt_folder):
        for file_name in files:
            if file_name.endswith(".bflyt"):
                file_names_stripped.append(file_name.strip(".bflyt"))
                stripped_name = file_name.strip(".bflyt")
                full_path = os.path.join(root, file_name)
                modified_name = stripped_name + "_name"
                file_paths[modified_name] = full_path

    
    if aspect_ratio >= 16/9:
        s1 = (16/9)  / aspect_ratio
        print(f"Scaling factor is set to {s1}")
        s2 = 1-s1
        s3 = s2/s1
        s4 = (16/10) / aspect_ratio
        
        for name in file_names_stripped:
            if name in do_not_scale_rootpane:
                    print(f"Skipping RootPane scaling of {name}")
            if name not in do_not_scale_rootpane:
                patch_blyt(name, 'RootPane', 'scale_x', s1)
            if name in rootpane_by_y:
                patch_blyt(name, 'RootPane', 'scale_y', 1/s1)
                patch_blyt(name, 'RootPane', 'scale_x', 1)

        patch_blyt('Pa_CongratsWorldClearBanner', 'P_Banner', 'scale_x', 1/s1)
        patch_blyt('GameLevelWin_00', 'L_World', 'scale_x', 1/s1)
        patch_blyt('GameOver_00', 'P_BG', 'scale_x', 1/s1)
        patch_blyt('GameModeChoice_00', 'P_BG', 'scale_x', 1/s1)
        patch_blyt('GameModeChoice_00', 'P_Background', 'scale_x', 1/s1)
        patch_blyt('GameModeChoice_00', 'L_Blur', 'scale_x', 1/s1)
        patch_blyt('GameLevelSelect_00', 'N_Background', 'scale_x', 1/s1)
        patch_blyt('GameLevelSelect_00', 'P_Cutout', 'scale_x', 1/s1)
        patch_blyt('GameLevelSelect_00', 'P_Cutout', 'scale_y', 1/s1)
        patch_blyt('GameLevelSelect_00', 'P_HeaderBG_01', 'scale_x', 1/s1)
        patch_blyt('GameLevelSelect_00', 'P_HeaderBG_02', 'scale_x', 1/s1)
        patch_blyt('GameLevelSelect_00', 'P_HeaderBGShadow_00', 'scale_x', 1/s1)
        patch_blyt('GameLevelSelect_00', 'L_GameMode', 'shift_x', do_some_math(1520, aspect_ratio))
        patch_blyt('GameLevelSelect_00', 'L_StarScore', 'shift_x', do_some_math(799, aspect_ratio))
        patch_blyt('GameLevelSelect_00', 'L_Lives', 'shift_x', do_some_math(651, aspect_ratio))
        # patch_blyt('GameLevelSelect_00', 'L_2P_Header', 'shift_x', do_some_math(710, aspect_ratio))
        patch_blyt('GameLevelSelect_00', 'P_Icon', 'shift_x', do_some_math(-802, aspect_ratio))
        patch_blyt('GameLevelSelect_00', 'T_WorldName_00', 'shift_x', do_some_math(-794, aspect_ratio))
        patch_blyt('GameLevelHUD_00', 'P_BorderL', 'shift_x', -2500)
        patch_blyt('GameLevelHUD_00', 'P_BorderR', 'shift_x', 2500)
        patch_blyt('GameLevelHUD_00', 'L_Lives', 'shift_x', do_some_math(112, aspect_ratio))
        patch_blyt('GameLevelHUD_00', 'N_Block_T', 'shift_x', do_some_math(-90, aspect_ratio))
        patch_blyt('GameLevelHUD_00', 'N_Block_Y', 'shift_x', do_some_math(90, aspect_ratio))
        patch_blyt('GameLevelHUD_00', 'N_DK', 'shift_x', do_some_math(-165, aspect_ratio))
        patch_blyt('GameLevelHUD_00', 'N_TimeAttack', 'scale_x', 1/s1)
        patch_blyt('GameLevelHUD_00', 'N_TA_Timer', 'scale_x', s1)
        patch_blyt('GameLevelHUD_00', 'N_TA_Timer', 'shift_x', do_some_math(487, aspect_ratio))
        patch_blyt('GameLevelHUD_00', 'N_Time', 'shift_x', do_some_math(-20, aspect_ratio))
        patch_blyt('GameLevelHUD_00', 'N_Collectible', 'shift_x', do_some_math(165, aspect_ratio))
        patch_blyt('GameLevelPauseMenu_00', 'L_Blur', 'scale_x', 1/s1)
        patch_blyt('Cutscene_Skip', 'L_Skip_00', 'shift_x', do_some_math(710, aspect_ratio))
        patch_blyt('CongratsScreen', 'P_Logo', 'shift_x', do_some_math(840, aspect_ratio))
        patch_blyt('GameMainMenu_00', 'P_BlackPanel', 'scale_x', 1/s1)
        patch_blyt('GameSplashScreen_00', 'P_BG_Gray', 'scale_x', 1/s1)
        patch_blyt('GameSplashScreen_00', 'P_pict_Mario', 'shift_x', do_some_math(-480, aspect_ratio))
        patch_blyt('GameSplashScreen_00', 'P_pict_DK', 'shift_x', do_some_math(480, aspect_ratio))
        patch_blyt('PaFooter_00', 'P_Backing', 'scale_x', 1/s1)
        patch_blyt('PaFooter_00', 'P_Shadow', 'scale_x', 1/s1)
        patch_blyt('WorldIntro', 'P_BorderBot', 'scale_x', 1/s1)
        patch_blyt('WorldIntro', 'P_BorderTop', 'scale_x', 1/s1)
        patch_blyt('WorldIntro', 'P_Fade', 'scale_x', 1/s1)
        patch_blyt('WorldIntro', 'P_Icon_00', 'shift_x', do_some_math(-802, aspect_ratio))
        patch_blyt('WorldIntro', 'T_WorldName_00', 'shift_x', do_some_math(-794, aspect_ratio))
        patch_blyt('PaMenu_Btn_Slot', 'P_Highlight', 'scale_x', 1/s1)

        # patch_blyt('PlayerIndicator_00', 'RootPane', 'scale_x', 1/s1) #Mario Bubble
        # patch_blyt('PlayerIndicator_01', 'RootPane', 'scale_x', 1/s1) #Toad Bubble
        

        if HUD_pos == 'corner':
            print("Shifitng elements for corner HUD")


        # To mirror an object, do -x scale, and 180 roate y. For example, if we want to mirror something that is 

    else:
        s1 = aspect_ratio / (16/9)
        s2 = 1-s1
        s3 = s2/s1
        
        for name in file_names_stripped:
            if name in do_not_scale_rootpane:
                print(f"Skipping root pane scaling of {name}")
            if name not in do_not_scale_rootpane:
                print(f"Scaling root pane vertically for {name}")
                patch_blyt(name, 'RootPane', 'scale_y', s1)
             
        patch_blyt('Pa_CongratsWorldClearBanner', 'P_Banner', 'scale_y', 1/s1)
        patch_blyt('GameLevelWin_00', 'L_World', 'scale_y', 1/s1)
        patch_blyt('GameLevelWin_00', 'N_null_00', 'scale_y', do_some_math(-495, aspect_ratio))
        patch_blyt('GameOver_00', 'P_BG', 'scale_y', 1/s1)
        patch_blyt('GameModeChoice_00', 'P_BG', 'scale_y', 1/s1)
        patch_blyt('GameModeChoice_00', 'P_Background', 'scale_y', 1/s1)
        patch_blyt('GameModeChoice_00', 'L_Blur', 'scale_y', 1/s1)
        patch_blyt('GameLevelSelect_00', 'N_Background', 'scale_y', 1/s1)
        patch_blyt('GameLevelSelect_00', 'P_Cutout', 'scale_y', 1/s1)
        patch_blyt('GameLevelSelect_00', 'P_Cutout', 'scale_y', 1/s1)
        patch_blyt('GameLevelSelect_00', 'P_HeaderBG_01', 'scale_y', do_some_math(433, aspect_ratio))
        patch_blyt('GameLevelSelect_00', 'P_HeaderBG_02', 'scale_y', do_some_math(431, aspect_ratio))
        patch_blyt('GameLevelSelect_00', 'P_HeaderBGShadow_00', 'scale_y', do_some_math(433, aspect_ratio))
        patch_blyt('GameLevelSelect_00', 'L_GameMode', 'shift_y', do_some_math(-130, aspect_ratio))
        patch_blyt('GameLevelSelect_00', 'L_StarScore', 'shift_y', do_some_math(440, aspect_ratio))
        patch_blyt('GameLevelSelect_00', 'L_Lives', 'shift_y', do_some_math(440, aspect_ratio))
        # patch_blyt('GameLevelSelect_00', 'L_2P_Header', 'shift_y', do_some_math(710, aspect_ratio))
        patch_blyt('GameLevelSelect_00', 'P_Icon', 'shift_y', do_some_math(425, aspect_ratio))
        patch_blyt('GameLevelSelect_00', 'T_WorldName_00', 'shift_y', do_some_math(415, aspect_ratio))
        patch_blyt('GameLevelHUD_00', 'P_BorderL', 'shift_y', -2500)
        patch_blyt('GameLevelHUD_00', 'P_BorderR', 'shift_y', 2500)
        patch_blyt('GameLevelHUD_00', 'L_Lives', 'shift_y', do_some_math(-60, aspect_ratio))
        patch_blyt('GameLevelHUD_00', 'N_Blocks', 'shift_y', do_some_math(-64, aspect_ratio))
        patch_blyt('GameLevelHUD_00', 'N_DK', 'shift_y', do_some_math(-130, aspect_ratio))
        patch_blyt('GameLevelHUD_00', 'N_TimeAttack', 'scale_y', 1/s1)
        patch_blyt('GameLevelHUD_00', 'N_TA_Timer', 'scale_y', s1)
        patch_blyt('GameLevelHUD_00', 'N_TA_Timer', 'shift_y', do_some_math(305, aspect_ratio))
        patch_blyt('GameLevelHUD_00', 'N_Time', 'shift_y', do_some_math(-60, aspect_ratio))
        patch_blyt('GameLevelHUD_00', 'N_Collectible', 'shift_y', do_some_math(-130, aspect_ratio))
        patch_blyt('GameLevelPauseMenu_00', 'L_Blur', 'scale_y', 1/s1)
        patch_blyt('Cutscene_Skip', 'L_Skip_00', 'shift_y', do_some_math(-480, aspect_ratio))
        patch_blyt('CongratsScreen', 'P_Logo', 'shift_y', do_some_math(-480, aspect_ratio))
        patch_blyt('GameMainMenu_00', 'P_BlackPanel', 'scale_y', 1/s1)
        patch_blyt('GameSplashScreen_00', 'P_BG_Gray', 'scale_y', 1/s1)
        patch_blyt('GameSplashScreen_00', 'P_pict_Mario', 'shift_y', do_some_math(-480, aspect_ratio))
        patch_blyt('GameSplashScreen_00', 'P_pict_DK', 'shift_y', do_some_math(480, aspect_ratio))
        patch_blyt('GameSplashScreen_00', 'T_Notes', 'shift_y', do_some_math(-490, aspect_ratio))
        patch_blyt('GameSplashScreen_00', 'A_Align', 'shift_y', do_some_math(-320, aspect_ratio))
        patch_blyt('PaFooter_00', 'P_Backing', 'scale_y', 1/s1)
        patch_blyt('PaFooter_00', 'P_Shadow', 'scale_y', 1/s1)
        patch_blyt('WorldIntro', 'P_Fade', 'scale_y', 1/s1)
        patch_blyt('WorldIntro', 'S_Graphics', 'scale_y', 1/s1)
        patch_blyt('WorldIntro', 'P_BorderBot', 'scale_y', do_some_math(-445, aspect_ratio))
        patch_blyt('WorldIntro', 'N_TopArea', 'scale_y', do_some_math(20, aspect_ratio))
        patch_blyt('WorldIntro', 'L_Zipper_00', 'scale_y', do_some_math(-420, aspect_ratio))
        patch_blyt('WorldIntro', 'P_Icon_00', 'shift_y', do_some_math(-802, aspect_ratio))
        patch_blyt('PaMenu_Btn_Slot', 'P_Highlight', 'scale_y', 1/s1)

        # if HUD_pos == 'corner':
        #     print("Shifitng elements for corner HUD")
