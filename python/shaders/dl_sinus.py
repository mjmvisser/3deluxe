import delight

class dl_sinus(delight.Texture2D):
    typeid = 0x00350001
    description = "2d sine texture"
    symmetric = delight.Boolean(help="allow negative values,disabling power")
    normalized = delight.Boolean(help="remap symmetric to 0-1")       
    power = delight.Float(default=1,softmax=10,help="scaling factor non-symmetric curves")   
      
    rslpost = ""     
    rsl = \
    """
    
    
    ss *=2*PI;
    tt *=2*PI;             
    if(i_symmetric)
    {
        o_outColor = sin(ss) * sin(tt);
        if (i_normalized)
        {
            o_outColor *=.5;
            o_outColor +=.5;
        }      
    }
    else
    {
        o_outColor = pow(abs(sin(ss)),i_power) *  pow(abs(sin(tt)),i_power);
    }
    o_outAlpha = luminance(o_outColor);  
    """
     
     
def initializePlugin(obj):
    dl_sinus.register(obj)

def uninitializePlugin(obj):
    dl_sinus.deregister(obj)