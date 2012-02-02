import deluxe

class dl_switch(deluxe.Utility):
    typeid = 0x00370002
    description = "Switcher"
    
    dl_switch_selectInput_override_0 = deluxe.Float(shortname="sio0", default=-1, message=True, help="")
    dl_switch_selectInput_override_1 = deluxe.Float(shortname="sio1", default=-1, message=True, help="")
    dl_switch_selectInput_override_2 = deluxe.Float(shortname="sio2", default=-1, message=True, help="")
    dl_switch_selectInput_override_3 = deluxe.Float(shortname="sio3", default=-1, message=True, help="")
    dl_switch_selectInput_override_4 = deluxe.Float(shortname="sio4", default=-1, message=True, help="")
    dl_switch_selectInput_override_5 = deluxe.Float(shortname="sio5", default=-1, message=True, help="")
    dl_switch_selectInput_override_6 = deluxe.Float(shortname="sio6", default=-1, message=True, help="")
    dl_switch_selectInput_override_7 = deluxe.Float(shortname="sio7", default=-1, message=True, help="")
    dl_switch_selectInput_override_8 = deluxe.Float(shortname="sio8", default=-1, message=True, help="")
    dl_switch_selectInput_override_9 = deluxe.Float(shortname="sio9", default=-1, message=True, help="")
    colorSet1 = deluxe.Color(shortname="cs1", storage='varying', default=-1, message=True, help="");

    selectInput = deluxe.Enum(default='0',
                              choices=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
                              storage='uniform',
                              help="""
                                The default input color and float that are assigned to outColor and outAlpha.
                                This will be overridden by the rib attr specified in ribAttrOverride;
                                the primvar specified in primvarOverride will override them both.
                                """);   

    primvarOverride = deluxe.Enum(default='None',
                              choices=[
                                'dl_switch_selectInput_override_0',
                                'dl_switch_selectInput_override_1',
                                'dl_switch_selectInput_override_2',
                                'dl_switch_selectInput_override_3',
                                'dl_switch_selectInput_override_4',
                                'dl_switch_selectInput_override_5',
                                'dl_switch_selectInput_override_6',
                                'dl_switch_selectInput_override_7',
                                'dl_switch_selectInput_override_8',
                                'dl_switch_selectInput_override_9',
                                'colorSet1[0]',
                                'None'
                                ],
                              storage='uniform',
                              help="""
                                Specify the name of the primvar that will override the selectInput parameter."
                                """);   

    colorSet1nChoices = deluxe.Integer(shortname="cs1m",
                            help="How many inputs to randomly choose from when primvarOverride = 'colorSet1[0]'")

    ribAttrOverride = deluxe.String(help="""
                                The rib attribute that will override the selectInput parameter.  For example,
                                if you have a user rib attr called "switch_override", enter "user:switch_override".
                                """);

    inputFloat0 = deluxe.Float(shortname="if0", help="This will be assigned to outAlpha if input 0 is selected.")
    inputFloat1 = deluxe.Float(shortname="if1", help="This will be assigned to outAlpha if input 1 is selected.")
    inputFloat2 = deluxe.Float(shortname="if2", help="This will be assigned to outAlpha if input 2 is selected.")
    inputFloat3 = deluxe.Float(shortname="if3", help="This will be assigned to outAlpha if input 3 is selected.")
    inputFloat4 = deluxe.Float(shortname="if4", help="This will be assigned to outAlpha if input 4 is selected.")
    inputFloat5 = deluxe.Float(shortname="if5", help="This will be assigned to outAlpha if input 5 is selected.")
    inputFloat6 = deluxe.Float(shortname="if6", help="This will be assigned to outAlpha if input 6 is selected.")
    inputFloat7 = deluxe.Float(shortname="if7", help="This will be assigned to outAlpha if input 7 is selected.")
    inputFloat8 = deluxe.Float(shortname="if8", help="This will be assigned to outAlpha if input 8 is selected.")
    inputFloat9 = deluxe.Float(shortname="if9", help="This will be assigned to outAlpha if input 9 is selected.")

    inputColor0 = deluxe.Color(shortname="ic0", help="This will be assigned to outColor if input 0 is selected.")
    inputColor1 = deluxe.Color(shortname="ic1", help="This will be assigned to outColor if input 1 is selected.")
    inputColor2 = deluxe.Color(shortname="ic2", help="This will be assigned to outColor if input 2 is selected.")
    inputColor3 = deluxe.Color(shortname="ic3", help="This will be assigned to outColor if input 3 is selected.")
    inputColor4 = deluxe.Color(shortname="ic4", help="This will be assigned to outColor if input 4 is selected.")
    inputColor5 = deluxe.Color(shortname="ic5", help="This will be assigned to outColor if input 5 is selected.")
    inputColor6 = deluxe.Color(shortname="ic6", help="This will be assigned to outColor if input 6 is selected.")
    inputColor7 = deluxe.Color(shortname="ic7", help="This will be assigned to outColor if input 7 is selected.")
    inputColor8 = deluxe.Color(shortname="ic8", help="This will be assigned to outColor if input 8 is selected.")
    inputColor9 = deluxe.Color(shortname="ic9", help="This will be assigned to outColor if input 9 is selected.")

    outColor = deluxe.Color(shortname="oc", output=True)
    outAlpha = deluxe.Float(shortname="oa", output=True)

    rslpost = ""
              
    rsl = """    

        // By default, use i_selectInput for the selected input.
        float selectInput = i_selectInput;

        // Rib attribute override.
        if (i_ribAttrOverride != "") attribute(i_ribAttrOverride, selectInput);

        // Primvar override.

        extern float dl_switch_selectInput_override_0;
        extern float dl_switch_selectInput_override_1;
        extern float dl_switch_selectInput_override_2;
        extern float dl_switch_selectInput_override_3;
        extern float dl_switch_selectInput_override_4;
        extern float dl_switch_selectInput_override_5;
        extern float dl_switch_selectInput_override_6;
        extern float dl_switch_selectInput_override_7;
        extern float dl_switch_selectInput_override_8;
        extern float dl_switch_selectInput_override_9;
        extern color colorSet1;

        if (i_primvarOverride == 0) {
            if (dl_switch_selectInput_override_0 >= 0) selectInput = dl_switch_selectInput_override_0;
        } else if (i_primvarOverride == 1) {
            if (dl_switch_selectInput_override_1 >= 0) selectInput = dl_switch_selectInput_override_1;
        } else if (i_primvarOverride == 2) {
            if (dl_switch_selectInput_override_2 >= 0) selectInput = dl_switch_selectInput_override_2;
        } else if (i_primvarOverride == 3) {
            if (dl_switch_selectInput_override_3 >= 0) selectInput = dl_switch_selectInput_override_3;
        } else if (i_primvarOverride == 4) {
            if (dl_switch_selectInput_override_4 >= 0) selectInput = dl_switch_selectInput_override_4;
        } else if (i_primvarOverride == 5) {
            if (dl_switch_selectInput_override_5 >= 0) selectInput = dl_switch_selectInput_override_5;
        } else if (i_primvarOverride == 6) {
            if (dl_switch_selectInput_override_6 >= 0) selectInput = dl_switch_selectInput_override_6;
        } else if (i_primvarOverride == 7) {
            if (dl_switch_selectInput_override_7 >= 0) selectInput = dl_switch_selectInput_override_7;
        } else if (i_primvarOverride == 8) {
            if (dl_switch_selectInput_override_8 >= 0) selectInput = dl_switch_selectInput_override_8;
        } else if (i_primvarOverride == 9) {
            if (dl_switch_selectInput_override_9 >= 0) selectInput = dl_switch_selectInput_override_9;
        } else if (i_primvarOverride == 10) {
            if (colorSet1[0] >= 0) {
                float rnd = cellnoise(.84 + colorSet1[0] * 140.45 * i_colorSet1nChoices);
                selectInput = floor(rnd*i_colorSet1nChoices);
            }
        }

        // Assign outputs.
        o_outAlpha =
            selectInput == 0 ? i_inputFloat0 :
            selectInput == 1 ? i_inputFloat1 :
            selectInput == 2 ? i_inputFloat2 :
            selectInput == 3 ? i_inputFloat3 :
            selectInput == 4 ? i_inputFloat4 :
            selectInput == 5 ? i_inputFloat5 :
            selectInput == 6 ? i_inputFloat6 :
            selectInput == 7 ? i_inputFloat7 :
            selectInput == 8 ? i_inputFloat8 : i_inputFloat9;

        o_outColor =
            selectInput == 0 ? i_inputColor0 :
            selectInput == 1 ? i_inputColor1 :
            selectInput == 2 ? i_inputColor2 :
            selectInput == 3 ? i_inputColor3 :
            selectInput == 4 ? i_inputColor4 :
            selectInput == 5 ? i_inputColor5 :
            selectInput == 6 ? i_inputColor6 :
            selectInput == 7 ? i_inputColor7 :
            selectInput == 8 ? i_inputColor8 : i_inputColor9;
    """
    
       
def initializePlugin(obj):
    dl_switch.register(obj)

def uninitializePlugin(obj):
    dl_switch.deregister(obj)
