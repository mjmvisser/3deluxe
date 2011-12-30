import delight

class dl_screen(delight.Texture2D):
    typeid = 0x00366668
    description = " Makes a surface that looks like a metal screen."   
    density = delight.Float(default=0.25,max=1)    
    frequency = delight.Float(default=20,softmax=100);
  
    rslpost = ""
    rsl = """

#define boxstep(a,b,x) (clamp(((x)-(a))/((b)-(a)),0,1))
#define MINFILTERWIDTH 1.0e-7

  extern varying float du, dv; 
  normal Nf;    /* Forward facing Normal vector */
  vector IN;    /* normalized incident vector */
  float d;      /* Density at the sample point */
  float sss, ttt; /* s,t, parameters in phase */
  float swidth, twidth, GWF, w, h;

  /* Determine how wide in s-t space one pixel projects to */
  swidth = max (abs(Du(ss)*du) + abs(Dv(ss)*dv), MINFILTERWIDTH) * i_frequency;
  twidth = max (abs(Du(tt)*du) + abs(Dv(tt)*dv), MINFILTERWIDTH) * i_frequency;

  /* Figure out where in the pattern we are */
  sss = mod (i_frequency * ss, 1);
  ttt = mod (i_frequency * tt, 1);

  /* Figure out where the strips are. Do some simple antialiasing. */
  GWF = i_density*0.5;
  if (swidth >= 1)
      w = 1 - 2*GWF;
  else w = clamp (boxstep(GWF-swidth,GWF,sss), max(1-GWF/swidth,0), 1)
	 - clamp (boxstep(1-GWF-swidth,1-GWF,sss), 0, 2*GWF/swidth);
  if (twidth >= 1)
      h = 1 - 2*GWF;
  else h = clamp (boxstep(GWF-twidth,GWF,ttt), max(1-GWF/twidth,0),1)
	 - clamp (boxstep(1-GWF-twidth,1-GWF,ttt), 0, 2*GWF/twidth); 
  d = 1 - w*h;
  o_outColor = d;  
  o_outAlpha = d;  
"""
def initializePlugin(obj):
    dl_screen.register(obj)

def uninitializePlugin(obj):
    dl_screen.deregister(obj)