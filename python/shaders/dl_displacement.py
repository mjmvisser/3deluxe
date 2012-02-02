import deluxe

class dl_displacement(deluxe.Displacement):
    typeid = 0x00320000
    includes = ["displacement_utils.h"]
    
    globalScale = deluxe.Float(min=0, max=1, default=1, storage='uniform')
    globalOffset = deluxe.Float(softmin=-1, softmax=1, default=0, storage='uniform')
    
    useShadingNormals = deluxe.Boolean(default=False,
                                        help="""When a displacement map is used, this shader calls
                                                calculatenormal().  This causes polygonal data to
                                                appear faceted.  This parameter causes the original
                                                shading normal offset to be added to the calculated
                                                normal, generally re-smoothing polygonal data.""")
    
    useNormalMap = deluxe.Boolean(default=False, storage='uniform',
        help="If on, the normal is set by an input to the normalMap parameter, typically a texture.")
    normalMap = deluxe.Color(default=0, storage='varying',
        help="""If the useNormalMap parameter is on, this sets the normal.
        Typically you would input a colour texture of a worldspace normal map.
        """)
    
    # per input parameters
    name = deluxe.String(default="input",help="Name of this displacement layer.", norsl=True)
    enable = deluxe.Boolean(default=True,  help="Enable/disable this layer of displacement.")
    alpha = deluxe.Float(shortname="alpha", default=1, min=0, max=1, help="Alpha for this layer of displacement.")
    scale = deluxe.Float(default=1, softmin=-1, softmax=1, help="Scale this layer of displacement.")
    offset = deluxe.Float(default=0, softmin=-1, softmax=1, help="Offset this layer of displacement.")
    bumpOrDisplace = deluxe.Float(default=1, min=0, max=1, help="Only modifies the normal if 0, displaces at 1, blends between.")
    recalculateNormal = deluxe.Float(default=1, min=0, max=1, help="Recalculates the normal if 1, does not if 0, blends between.")
    amount = deluxe.Float(min=0, max=1, help="Plug utility nodes in here to displace.")
    lip = deluxe.Float(shortname="lip", min=0, max=1, help="it's a lip.")
    lipRimSharp = deluxe.Float(shortname="liprs", min=0, max=1, help="it's a lip.")
    
    inputs = deluxe.Compound([name,enable,alpha,scale,offset,bumpOrDisplace,recalculateNormal,amount,lip, lipRimSharp],array=True)
    selectedInput = deluxe.Integer(hidden = True)
    
    # notes:
    # need
    # - some kind of list representation for displacement layers
    # - way to add and remove layers
    # - way to move layers up and down
    # - per-input parameters must be connected to array attributes when a layer is selected
    
    
    template = \
    r"""
    

eval("source \"dl_dgLib.mel\";");

    
     
    proc rebuildList(string $inputs)
    {    
        textScrollList -edit -deselectAll inputsList; 
        textScrollList -edit -removeAll  -deselectAll inputsList;        
        int $ix[] = dl_dgPlugArrayGetIndices($inputs);
        int $i;
        for ($i in $ix)
        {
            textScrollList -edit -append `getAttr  ($inputs +"[" + $i + "].name")` inputsList;
        }                                          
    }   
    proc addNewInput(string $inputs)
    {
        int $new_index = dl_dgPlugArrayAddNew($inputs);               
        string $plugName = $inputs + "[" + $new_index + "]";                          
        setAttr -type "string" ($plugName + ".name")  ("input" + ($new_index +1) );
        if ($new_index>0)
        {
            int $i= getSelectedIndex($inputs);
            rebuildList($inputs);
            setSelectedIndex($inputs,$i);  
        }                       
    }
    
    proc int getSelectedScrollIndex(string $inputs)
    {
        
        int $selectedScrollIndexArray[] = `textScrollList   -query -selectIndexedItem inputsList`;        
        return  $selectedScrollIndexArray[0];               
    } 
    proc setSelectedScrollIndex(string $inputs,int $index)
    {       
         textScrollList -edit -selectIndexedItem $index inputsList;
         selectInput ($inputs);           
    }
    
    proc int getSelectedIndex(string $inputs)
    {
        int $indexList[] = dl_dgPlugArrayGetIndices($inputs);        
        int $selectedScrollIndex =  getSelectedScrollIndex($inputs);        
        if (!$selectedScrollIndex)
        {            
            return -1;
        }        
        $selectedScrollIndex--;
        return $indexList[$selectedScrollIndex];    
    }
    proc setSelectedIndex(string $inputs,int $index )
    {
        
        int $scrollIndex = 1;           
        int $indexList[] = dl_dgPlugArrayGetIndices($inputs);
        int $i;
        for ($i in $indexList)
        {
            if ($index == $i)
            {
                break;
            }
            else
            {
                $scrollIndex++;
            }            
        }        
        setSelectedScrollIndex($inputs,$scrollIndex);
                
    }



    proc deleteSelectedInput(string $inputs)
    {    
        if (size(dl_dgPlugArrayGetIndices($inputs)) > 1)
        {
            
            int $i= getSelectedIndex($inputs);
            textScrollList -edit -deselectAll inputsList; 
            if ($i>=0)
            {
                removeMultiInstance -b true ($inputs+"["+$i+"]");
                rebuildList($inputs); 
            } 
        }       
    }
    
    proc moveUp(string $inputs)
    {
        int $i= getSelectedIndex($inputs);
        if ($i>=0)
        {
            int $ix =dl_dgPlugArraySwapWithPrev($inputs,$i);
            rebuildList($inputs);
            setSelectedIndex($inputs,$ix); 
        }   
    }
    proc moveDown(string $inputs)
    {
        int $i= getSelectedIndex($inputs);
        if ($i>=0)
        {
            int $ix = dl_dgPlugArraySwapWithNext($inputs,$i);
            rebuildList($inputs);
            setSelectedIndex($inputs,$ix); 
        }   
    }     
    proc selectInput (string $inputs)
    {     
        int $i= getSelectedIndex($inputs);       
        if ($i<0)
        {
            return;
        }
                      
        AEreplaceString  nameGrp ($inputs+"["+$i+"].name") "";                                                    
        attrFieldSliderGrp -e 
                           -at ($inputs+"["+$i+"].alpha")
                            alphaGrp;
        attrFieldSliderGrp -e 
                           -at ($inputs+"["+$i+"].scale")
                            scaleGrp;
        attrFieldSliderGrp -e
                           -at ($inputs+"["+$i+"].offset")
                            offsetGrp;                       
        attrFieldSliderGrp -e
                           -attribute ($inputs+"["+$i+"].bumpOrDisplace")
                           bumpOrdisplaceGrp;
        attrFieldSliderGrp -e
                           -at ($inputs+"["+$i+"].recalculateNormal")
                            recalculateNormalGrp;
        attrFieldSliderGrp -e
                           -at ($inputs+"["+$i+"].amount")
                            amountGrp;                        
        attrFieldSliderGrp -e
                           -at ($inputs+"["+$i+"].lip") 
                            lipGrp;                        
        attrFieldSliderGrp -e
                           -at ($inputs+"["+$i+"].lipRimSharp")
                            lipRimSharpGrp;                        
    }
    

    

    
    
      
    global proc AEdl_displacement_inputs_New(string $inputs)
    {
      
        
        if (!size(dl_dgPlugArrayGetIndices($inputs)))
        {
            addNewInput($inputs);
        }   
        columnLayout -adj true -cal "center"; 

            rowLayout -nc 2 -adj 1 -cw 2 80;
                textScrollList  -sc ("selectInput \""+ $inputs + "\"")
                                -height 150 
                                inputsList;
                rebuildList($inputs); 
                textScrollList  -e
                            -selectIndexedItem 1
                            inputsList;
             
             columnLayout  -cal "center" ;
                    button  -label " up "
                            -command ("moveUp \""+ $inputs + "\"")    
                            upBtn;
                    button  -label "down"
                            -command ("moveDown \""+ $inputs + "\"")
                            downBtn; 
             setParent..;
                            
            setParent..;
            
            button -label "Add new input" 
                   -command ("addNewInput \""+ $inputs + "\"") 
                    addBtn;
                           
            button -label "Delete selected input" 
                   -command ("deleteSelectedInput \""+ $inputs + "\"")
                    delBtn;               
                           
                                                        
            textFieldGrp   -label "Name"
                           -cc ("rebuildList " + $inputs)
                           nameGrp;
                           
            
            connectControl -index 2 nameGrp ($inputs+"[0].name");
                                       
            attrFieldSliderGrp -label "Alpha"
                               -attribute ($inputs+"[0].alpha")
                               -hideMapButton false
                                alphaGrp;
            attrFieldSliderGrp -label "Scale"
                               -attribute ($inputs+"[0].scale")
                               -hideMapButton false
                                scaleGrp;
            attrFieldSliderGrp -label "Offset"
                               -attribute ($inputs+"[0].offset")
                               -hideMapButton false                                                               
                               offsetGrp;                       
            attrFieldSliderGrp -label "Bump or Displace" 
                               -attribute ($inputs+"[0].bumpOrDisplace")
                               -hideMapButton false                               
                                bumpOrdisplaceGrp;
            attrFieldSliderGrp -label "Recalculate Normal"
                               -attribute ($inputs+"[0].recalculateNormal")
                               -hideMapButton false                              
                               recalculateNormalGrp;
            attrFieldSliderGrp -label "Amount"
                               -attribute ($inputs+"[0].amount")
                               -hideMapButton false                            
                                amountGrp;
            attrFieldSliderGrp -label "Lip"
                               -attribute ($inputs+"[0].lip")
                               -hideMapButton false                            
                                lipGrp;
            attrFieldSliderGrp -label "LipRimSharp"
                               -attribute ($inputs+"[0].lipRimSharp")
                               -hideMapButton false                            
                                lipRimSharpGrp;
       
        setParent..;
        
    }

     
    global proc AEdl_displacement_inputs_Replace(string $inputs)
    {    
        
        
        int  $selectedIndex = getSelectedIndex($inputs);
        int $indexList[] = dl_dgPlugArrayGetIndices($inputs);
             
        if (!size($indexList))
        {
            addNewInput($inputs);
        } 
        rebuildList($inputs); 
        
        textScrollList  -e
                        -sc ("selectInput \""+ $inputs + "\"")
                        inputsList;
        button  -e
                -command ("moveUp \""+ $inputs + "\"")    
                upBtn;
        button  -e
                -command ("moveDown \""+ $inputs + "\"")
                downBtn; 
                        
        button -e 
               -command ("addNewInput \""+ $inputs + "\"") 
               addBtn;
                           
        button -e 
               -command ("deleteSelectedInput \""+ $inputs + "\"")
               delBtn;
        textFieldGrp  -e
                       -cc ("rebuildList " + $inputs)
                        nameGrp;
        
        
        int $i;
        
        
        if ($selectedIndex>=0)
        {
            $i = $selectedIndex;
        }
        else
        {
             
             $i = $indexList[0];
        }
        setSelectedIndex($inputs,$i);                
        connectControl -index 2 nameGrp ($inputs+"["+$i+"].name");
        
                                     
        attrFieldSliderGrp -e
                           -attribute ($inputs+"["+$i+"].alpha")
                            alphaGrp;
        attrFieldSliderGrp -e
                           -attribute ($inputs+"["+$i+"].scale")
                            scaleGrp;
        attrFieldSliderGrp -e
                           -attribute ($inputs+"["+$i+"].offset")
                            offsetGrp;                       
        attrFieldSliderGrp -e 
                           -attribute ($inputs+"["+$i+"].bumpOrDisplace")
                            bumpOrdisplaceGrp;
        attrFieldSliderGrp -e
                           -attribute ($inputs+"["+$i+"].recalculateNormal")
                            recalculateNormalGrp;
        attrFieldSliderGrp -e
                           -attribute ($inputs+"["+$i+"].amount")
                            amountGrp;
        attrFieldSliderGrp -e
                           -attribute ($inputs+"["+$i+"].lip")
                            lipGrp;
        attrFieldSliderGrp -e
                           -attribute ($inputs+"["+$i+"].lipRimSharp")
                            lipRimSharpGrp;
                         
    } 
    
    
    
    
    global proc AEdl_displacementTemplate(string $node)
    {
    
        
        AEswatchDisplay $node;               
        editorTemplate -beginScrollLayout;
            
            editorTemplate -beginLayout "Displacement Attributes" -collapse 0;
                editorTemplate -addControl "globalScale";
                editorTemplate -addControl "globalOffset";
                editorTemplate -addControl "useShadingNormals";
                editorTemplate -addControl "useNormalMap";
                editorTemplate -addControl "normalMap";
            
                editorTemplate -beginLayout "Inputs" -collapse 0;
                                   
                    editorTemplate -callCustom 
                                "AEdl_displacement_inputs_New"
                                "AEdl_displacement_inputs_Replace"
                                "inputs";
                editorTemplate -endLayout;                
                            
            editorTemplate -endLayout;

  
            // include/call base class/node attributes
            AEdependNodeTemplate $node;
    
            editorTemplate -addExtraControls;
        editorTemplate -endScrollLayout;
    }
    """
    
    rsl = \
    r"""
    extern point P;
    extern normal N;
    extern normal Ng;
    extern point __Porig;
    extern normal __Norig;

    // save P and N for use when raytracing without displacements
    __Porig = P;
    __Norig = N;

    normal Nn = normalize(N);
    normal deltaN = Nn - normalize(Ng);
    
    point Pnew = P + Nn * i_globalOffset;
    normal Nnew = Nn;
    
    uniform float num_inputs = arraylength(i_enable);

    
    float i;
    for (i = 0; i < num_inputs; i += 1)
    {
        if (i_enable[i] != 0)
        {
            float amount = i_amount[i];
            float lip = i_lip[i];

            if (lip > 0) {
                float lipDisp = -amount;
                float noLipDisp = amount - 2*lip;
                float mixer = smoothstep(.5 * i_lipRimSharp[i],
                    1 - .5 * i_lipRimSharp[i], amount/(lip * 2));
                amount = mix(lipDisp, noLipDisp, mixer);
                //amount = amount > lip ? amount - 2*lip : - amount;
            }

            amount = (amount * i_scale[i] * i_globalScale + i_offset[i]) * i_alpha[i];

            point Pold = Pnew;
            normal Nold = Nnew;
            getDisplacement(
                    amount,
                    i_bumpOrDisplace[i],
                    i_recalculateNormal[i],
                    i_useShadingNormals,
                    Pold,
                    Nold,
                    deltaN,
                    Pnew,
                    Nnew);
        }
    }
    
    if (i_useNormalMap == 1) {
        normal NmapWorld = normal i_normalMap;
        normal Nmap = ntransform("world", "current", NmapWorld);
        Nnew = Nmap + (Nnew-__Norig);
    }

    N = Nnew;
    P = Pnew;
    """
    
def initializePlugin(obj):
    dl_displacement.register(obj)

def uninitializePlugin(obj):
    dl_displacement.deregister(obj)
