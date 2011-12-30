import delight

class dl_brick(delight.Texture2D):
    typeid = 0x00366666
    description = "Makes a wall of bricks. Need more be said?"
      
    brickColor   = delight.Color(default=(0.6,0.1,0.1),help="Brick Color")
    mortarColor =  delight.Color(default=(0.6,0.6,0.6),help="Mortar Color")      
    jagged = delight.Float(default=0.006, softmin=0, max=1,help="How much do bricks deviate from squares?") 
    brickVary =   delight.Float(default=0.3, min=0, max=1,help="How much does the brick color vary from brick to brick?")
    brickWidth =  delight.Float(default=.25, min=0, max=1,help="Width of a brick")
    brickHeight =  delight.Float(default=.08, min=0, max=1,help="Height of a brick")
    mortarThickness =  delight.Float(default= .01, min=0, max=1,help="Thickness of the mortar")
    rowVary =  delight.Float(default=.25, min=0, max=1,help="How much does each row shift")
    
   
    rslpost = ""
    
    
    rsl = """
#define BMWIDTH (i_brickWidth+i_mortarThickness)
#define BMHEIGHT (i_brickHeight+i_mortarThickness)
#define MWF (i_mortarThickness*0.5/BMWIDTH)
#define MHF (i_mortarThickness*0.5/BMHEIGHT)
#define snoise(x) (2 * noise((x)) - 1)
#define boxstep(a,b,x) (clamp(((x)-(a))/((b)-(a)),0,1))
#define MINFILTERWIDTH 1.0e-7
  color bcolor;
  point PP2, Nf;
  float sbrick, tbrick, w, h;
  float scoord, tcoord, sss, ttt;
  float swidth, twidth;
  float Nfactor;
  
  extern varying float du,dv;    

  /* Determine how wide in ss-tt space one pixel projects to */
  swidth = max (abs(Du(ss)*du) + abs(Dv(ss)*dv), MINFILTERWIDTH);
  twidth = max (abs(Du(tt)*du) + abs(Dv(tt)*dv), MINFILTERWIDTH);

  

  /* Make the shapes of the bricks vary just a bit */
  PP2 = point noise (ss/BMWIDTH, tt/BMHEIGHT);
  scoord = ss + i_jagged * xcomp (PP2);
  tcoord = tt + i_jagged * ycomp (PP2);

  sss = scoord / BMWIDTH;   /* Determine which brick the point is in */
  ttt = tcoord / BMHEIGHT;  /*                   "                   */
  swidth /= BMWIDTH;
  twidth /= BMHEIGHT;

  /* shift alternate rows */
  if (mod (ttt*0.5, 1) > 0.5)
      sss += 0.5;

  tbrick = floor (ttt);   /* which brick row? */
  /* Shift the columns randomly by row */
  sss += i_rowVary * (noise (tbrick+0.5) - 0.5);

  sbrick = floor (sss);   /* which brick column? */
  sss -= sbrick;          /* Now sss and ttt are coords within the brick */
  ttt -= tbrick;

  /* Choose a color for the surface */
  if (swidth >= 1)
      w = 1 - 2*MWF;
  else w = clamp (boxstep(MWF-swidth,MWF,sss), max(1-MWF/swidth,0), 1)
     - clamp (boxstep(1-MWF-swidth,1-MWF,sss), 0, 2*MWF/swidth);

  if (twidth >= 1)
      h = 1 - 2*MHF;
  else h = clamp (boxstep(MHF-twidth,MHF,ttt), max(1-MHF/twidth,0),1)
     - clamp (boxstep(1-MHF-twidth,1-MHF,ttt), 0, 2*MHF/twidth);

  /* Choose a brick color that varies from brick to brick */
  bcolor = i_brickColor * (1 + (i_brickVary * snoise (tbrick+(100*sbrick)+0.5)));

  o_outColor = mix(i_mortarColor, bcolor, w*h);
  o_outAlpha = luminance( o_outColor );
    """  
    
def initializePlugin(obj):
    dl_brick.register(obj)

def uninitializePlugin(obj):
    dl_brick.deregister(obj)