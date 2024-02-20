
def create_visuals(do_screenshot, do_disable_fxaa, do_disable_dynamicres, do_disable_dof, do_disable_bloom):

    screenshot = "disabled"
    disablefxaa = "disabled"
    disabledynamicres = "disabled"
    disabledof = "disabled"
    disablebloom = "disabled"

    do_island = False
    
    visual_fixes = []

    if do_screenshot:
        screenshot = "enabled"
    if do_disable_fxaa:
        disablefxaa = "enabled"
    if do_disable_dynamicres:
        disabledynamicres = "enabled"
    if do_disable_dof:
        disabledof = "enabled"
    if do_disable_bloom:
        disablebloom = "enabled"
        
    visuals1_0_0 = f'''// LOD Increase
@disabled
00927BFC 28008052
00874AC0 29008052
@stop

// Disable FXAA
@disabled
00950CE8 09008052
00950CC0 09008052
@stop

// Disable Dynamic Resolution
@disabled
007FC380 C0035FD6
007FC1E0 C0035FD6
@stop
    
// Disable Bloom Effect
@disabled
008193B0 C0035FD6
@stop

// Disable DOF
@disabled
00888AB0 C0035FD6
@stop
'''


    visuals1_1_0 = f'''// Screenshot Mode Graphics
@disabled
00927BFC 28008052
00874AC0 29008052
@stop

// Disable FXAA
@disabled
00B92318 08000014
@stop

// Disable Dynamic Resolution
@disabled
007FC380 C0035FD6
007FC1E0 C0035FD6
@stop

// Disable Bloom Effect
@disabled
008193B0 C0035FD6
@stop

// Disable DOF
@disabled
00888AB0 C0035FD6
@stop
'''

    visual_fixes.append(visuals1_0_0)
    visual_fixes.append(visuals1_1_0)
    
    return visual_fixes