import os
import struct

def patch_blarc(aspect_ratio, HUD_pos, unpacked_folder):
    unpacked_folder = str(unpacked_folder)
    aspect_ratio = float(aspect_ratio)
    print(f"Aspect ratio is {aspect_ratio}")
    HUD_pos = str(HUD_pos)
     
    def float2hex(f):
        return hex(struct.unpack('>I', struct.pack('<f', f))[0]).lstrip('0x').rjust(8,'0').upper()

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
        if operation == "shift_x":
            full_path_of_file = os.path.join(unpacked_folder, 'romfs', 'LayoutData', filename, 'layout', 'blyt', f'{filename}.bflyt')
        else:
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
        full_path = os.path.join(unpacked_folder, 'romfs', 'LayoutData', folder, 'layout', 'anim', f'{filename}.bflan') # update this to work with layout.lyarc structure
        with open(full_path, 'rb') as f:
            content = f.read().hex()
        idx = offset
        content_new = content[:idx] + float2hex(value) + content[idx+8:]
        with open(full_path, 'wb') as f:
            f.write(bytes.fromhex(content_new))  

    file_paths = {}

    blyt_folder = os.path.abspath(os.path.join(unpacked_folder))
    file_names_stripped = []
    
    do_not_scale_rootpane = ['WipeFadeBlack', 'WipeFadeWhite', 'WipeMystery', 'WipeMiss', "WipeNetwork", "WipeCurtainStart", "WipeCurtainResult", 'WipeCurtainRanking', 'WipeCurtainRankingParts', 'WipeCasino', 'WipeFairy', 'WipeKnoko', "WipeMissSingleMode", 'WipeNetwork', 'WipeCurtainDemo']
   
    rootpane_by_y = ['WipeCircle']

    for root, dirs, files in os.walk(blyt_folder):
        for file_name in files:
            if file_name.endswith(".bflyt"):
                file_names_stripped.append(file_name.strip(".bflyt"))
                stripped_name = file_name.strip(".bflyt")
                full_path = os.path.join(root, file_name)
                modified_name = stripped_name + "_name"
                file_paths[modified_name] = full_path

    
    if aspect_ratio >= 16/9:
        s1 = (((((aspect_ratio * 9) - 16) / 2) + 16) / 9)  / aspect_ratio
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

        patch_blyt('TitleLogo', 'ParControlGuideBar', 'scale_x', 1/s1)
        # patch_blyt('TalkMessageOver', 'RootPane', 'scale_x', 1/s4)
        # patch_blyt('TalkMessage', 'Message', 'scale_x', s4)
        # patch_blyt('TalkMessageOver', 'Message', 'scale_x', s4)
        # patch_blyt('PlayGuide', 'PicBase', 'scale_x', 1/s4)
        # patch_blyt('PlayGuideMovie', 'PicMovie', 'scale_x', 1/s4)
        # # patch_blyt('CinemaCaption', 'All', 'scale_x', s1)
        # # patch_blyt('CinemaCaption', 'PicCaptureUse', 'scale_x', 1/s1)
        # # patch_blyt('BootLoading', 'ParBG', 'scale_x', s1) # joycon boot screen
        # # patch_blyt('ContinueLoading', 'PicFooter', 'scale_x', 1/s1)
        # # patch_blyt('ContinueLoading', 'PicFooterBar', 'scale_x', 1/s1)
        # # patch_blyt('ContinueLoading', 'PicProgressBar', 'scale_x', 1/s1)
        # # patch_blyt('ContinueLoading', 'ParBG', 'scale_x', 1/s1)
        # # patch_blyt('ContinueLoading', 'ParBG', 'scale_y', 1/s1)
        # # patch_blyt('Menu', 'Capture', 'scale_x', s1) DNW
        # # patch_anim('Menu', 'Capture', 'scale_x', 1/s1) DNW
        # patch_blyt('Menu', 'ParLogo', 'scale_x', s1) 
        # patch_blyt('Menu', 'List', 'scale_x', s1) 
        # # patch_blyt('OptionSelect', 'Capture', 'scale_x', 1/s1) DNW
        # # patch_blyt('OptionMode', 'Capture', 'scale_x', s1)
        # # patch_blyt('OptionData', 'Capture', 'scale_x', s1)
        # # patch_blyt('OptionLanguage', 'Capture', 'scale_x', s1)
        # # patch_blyt('OptionConfig', 'Capture', 'scale_x', s1)
        # # patch_blyt('OptionProcess', 'Capture', 'scale_x', s1)
        # # patch_blyt('WorldSelect', 'PicBase', 'scale_x', 1/s1) DNW
        # # patch_blyt('StaffRoll', 'PicBG', 'scale_x', 1/s1) DNW
        # # patch_blyt('CommonBgParts', 'PicMapCap', 'scale_x', 1/s1)
        # patch_blyt('Menu', 'ParBG', 'scale_x', 1/s1)
        # # patch_anim('Menu', 'Menu_Wait', 416, 285 + 540*s3)
        # # patch_anim('Menu', 'Menu_Boot', 416, 285 + 540*s3)
        # # patch_anim('Menu', 'Menu_SelectPause', 416, 285 + 540*s3)
        # # patch_anim('Menu', 'Menu_Appear', 416, 285 + 540*s3)
        # # patch_anim('Menu', 'Menu_End', 416, 285 + 540*s3)
        # # patch_anim('Menu', 'Menu_SelectTitle', 416, 285 + 540*s3)
        # patch_blyt('CounterLifeUp', 'RootPane', 'scale_x', s1) 
        # patch_blyt('KidsMode', 'RootPane', 'scale_x', s1) 
        # patch_blyt('CounterLifeKids', 'RootPane', 'scale_x', s1) 
        # patch_blyt('MapMini', 'RootPane', 'scale_x', s1) 
        # patch_blyt('CounterLife', 'RootPane', 'scale_x', s1) 
        # patch_blyt('CounterCoin', 'RootPane', 'scale_x', s1) 
        # patch_blyt('CounterCollectCoin', 'RootPane', 'scale_x', s1) 
        # patch_blyt('CounterPiece', 'RootPane', 'scale_x', s1) 
        # patch_blyt('CounterMiss', 'RootPane', 'scale_x', s1) 
        # patch_blyt('CounterShine', 'RootPane', 'scale_x', s1) 

        if HUD_pos == 'corner':
            print("Shifitng elements for corner HUD")
            patch_blyt('SingleModeSceneLayout', 'CounterCoin', 'shift_x', 660*s2) 
            patch_blyt('SingleModeSceneLayout', 'CounterGoalItem', 'shift_x', 660*s2) 
            patch_blyt('SingleModeSceneLayout', 'CounterScenarioShine', 'shift_x', 660*s2) 
            patch_blyt('SingleModeSceneLayout', 'ChallengeTimer', 'shift_x', 660*s2) 
            patch_blyt('SingleModeSceneLayout', 'Menu', 'shift_x', -660*s2) 
            patch_blyt('CourseSelectSceneLayout', 'Menu', 'shift_x', -660*s2) 
            patch_blyt('CourseSelectSceneLayout', 'World', 'shift_x', 660*s2) 
            patch_blyt('CourseSelectSceneLayout', 'Counters', 'shift_x', 660*s2) 
            patch_blyt('CourseSelectSceneLayout', 'CounterGreenStarTotal', 'shift_x', 660*s2) 
            patch_blyt('StageSceneLayout', 'CounterCoin', 'shift_x', 660*s2) 
            patch_blyt('StageSceneLayout', 'CounterPlayer', 'shift_x', 660*s2) 
            patch_blyt('StageSceneLayout', 'CounterGreenStar', 'shift_x', 660*s2) 
            patch_blyt('StageSceneLayout', 'ItemStock', 'shift_x', 660*s2) 
            patch_blyt('StageSceneLayout', 'CounterTime', 'shift_x', -660*s2) 
            patch_blyt('StageSceneLayout', 'CounterScore', 'shift_x', -660*s2) 
            patch_blyt('StageSceneLayout', 'NetworkQuality', 'shift_x', -660*s2) 

            
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
             
        # # patch_blyt('TalkMessage', 'PicBase', 'scale_y', 1/s1)
        # patch_blyt('PlayGuide', 'PicBase', 'scale_y', 1/s1)
        # patch_blyt('PlayGuideMovie', 'PicMovie', 'scale_y', 1/s1)
        # patch_blyt('PlayGuide', 'PicBase', 'scale_y', 1/s1)
        # patch_blyt('CinemaCaption', 'All', 'scale_y', s1)
        # patch_blyt('CinemaCaption', 'PicCaptureUse', 'scale_y', 1/s1)
        # patch_blyt('BootLoading', 'ParBG', 'scale_y', 1/s1) # joycon boot screen
        # patch_blyt('ContinueLoading', 'PicFooter', 'scale_y', 1/s1)
        # patch_blyt('ContinueLoading', 'PicFooterBar', 'scale_y', 1/s1)
        # patch_blyt('ContinueLoading', 'PicProgressBar', 'scale_y', 1/s1)
        # patch_blyt('ContinueLoading', 'ParBG', 'scale_y', 1/s1)
        # patch_blyt('ContinueLoading', 'ParBG', 'scale_x', 1/s1)
        # patch_blyt('Menu', 'Capture', 'scale_y', 1/s1)
        # # patch_anim('Menu', 'Capture', 'scale_x', 1/s1)
        # # patch_blyt('OptionSelect', 'Capture', 'scale_y', 1/s1)
        # patch_blyt('OptionMode', 'Capture', 'scale_y', 1/s1)
        # patch_blyt('OptionData', 'Capture', 'scale_y', 1/s1)
        # patch_blyt('OptionLanguage', 'Capture', 'scale_y', 1/s1)
        # patch_blyt('OptionConfig', 'Capture', 'scale_y', 1/s1)
        # patch_blyt('OptionProcess', 'Capture', 'scale_y', 1/s1)
        # patch_blyt('TalkMessage', 'PicBase', 'scale_y', 1/s1)
        # patch_blyt('TalkMessageOver', 'PicBase', 'scale_y', 1/s1)
        # patch_blyt('WorldSelect', 'PicBase', 'scale_y', 1/s1)
        # patch_blyt('StaffRoll', 'PicBG', 'scale_y', 1/s1)
        # patch_blyt('CommonBgParts', 'PicMapCap', 'scale_y', s1)

        # if HUD_pos == 'corner':
        #     print("Shifitng elements for corner HUD")
        #     patch_blyt('TalkMessage', 'PicBase', 'shift_y', -540*s2)
        #     patch_blyt('MapMini', 'RootPane', 'shift_y', 540*s2) 
        #     patch_blyt('CounterLife', 'RootPane', 'shift_y', 540*s2) 
        #     patch_blyt('CounterCoin', 'RootPane', 'shift_y', 540*s2) 
        #     patch_blyt('SaveMessage', 'All', 'shift_y', -540*s2) 
        #     patch_blyt('CounterCollectCoin', 'RootPane', 'shift_y', 540*s2) 
        #     patch_blyt('Menu', 'ParLogo', 'shift_y', 540*s2) 
        #     patch_blyt('CounterLifeUp', 'RootPane', 'shift_y', 540*s2) 
        #     patch_blyt('KidsMode', 'RootPane', 'shift_y', 540*s2) 
        #     patch_blyt('CounterLifeKids', 'RootPane', 'shift_y', 540*s2) 
        #     patch_blyt('WorldSelect', 'ParCounter', 'shift_y', 540*s2) 
        #     patch_blyt('ContinueLoading', 'HomeIcon', 'shift_y', 540*s2) 
        #     patch_blyt('ContinueLoading', 'ParLogo', 'shift_y', 540*s2) 
        #     patch_blyt('Shop', 'ParFooter', 'shift_y', -540*s2) 