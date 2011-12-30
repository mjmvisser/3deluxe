import delight

class dl_hextile(delight.Texture2D):
    typeid = 0x00366667
    description = "Makes a pattern of hexagonal tiles"

    tileColor = delight.Color(default=(0.55,0.0,0.0),help="")  
    mortarColor = delight.Color(default=(0.5,0.5,0.5),help="") 
    tileRadius = delight.Float(default=0.2, min=0, max=1,help="")
    mortarWidth = delight.Float(default=0.02, min=0, max=1,help="")
    tileVary =   delight.Float(default=0.15, min=0, max=1,help="")
    tileScuffing = delight.Float(default=0.5, min=0, max=1,help="")
    stains = delight.Float(default=0.4, min=0, max=1,help="")
    stainFrequency = delight.Float(default=2, min=0, softmax=100,help="")
    tileScuffFrequency =delight.Float(default=4, min=0, softmax=100,help="")  
    tileScuffColor =  delight.Color(default=(.05,.05,.05),help="") 
    rslpost = ""
    rsl = """
#define snoise(x) (2*noise(x)-1)
#define snoise2(x,y) (2*noise((x),(y))-1)
  
  
  extern varying float du, dv; 
  point Nf;
  color Ct, Ctile;
  float tilewidth;
  float sss, ttt;
  float ttile, stile;
  float x, y;
  float mortar;
  float swidth, twidth, sfuzz, tfuzz, fuzzmax;
  float mw2;
  float tileindex;
  float stain, scuff;
  float ks;

  /* Determine how wide in ss-tt space one pixel projects to */
  swidth = abs(Du(ss)*du) + abs(Dv(ss)*dv);
  twidth = abs(Du(tt)*du) + abs(Dv(tt)*dv);
  sfuzz = 0.5 * swidth;
  tfuzz = 0.5 * twidth;
  fuzzmax = max (sfuzz, tfuzz);

  tilewidth = i_tileRadius * 1.7320508;  /* sqrt(3) */
  ttt = mod (tt, 1.5*i_tileRadius);
  ttile = floor (tt/(1.5*i_tileRadius));
  if (mod (ttile/2, 1) == 0.5)
       sss = ss + tilewidth/2;
  else sss = ss;
  stile = floor (sss / tilewidth);
  sss = mod (sss, tilewidth);
  mortar = 0;
  mw2 = i_mortarWidth/2;
  if (ttt < i_tileRadius) {
      mortar =  1 - (smoothstep(mw2,mw2+sfuzz,sss) *
             (1 - smoothstep(tilewidth-mw2-sfuzz,tilewidth-mw2,sss)));
    }
  else {
      x = tilewidth/2 - abs (sss - tilewidth/2);
      y = 1.7320508 * (ttt - i_tileRadius);
      if (y > x) {
      if (mod (ttile/2, 1) == 0.5)
          stile -= 1;
      ttile += 1;
      if (sss > tilewidth/2)
          stile += 1;
    }
      mortar = (smoothstep (x-1.73*mw2-tfuzz, x-1.73*mw2, y) *
        (1 - smoothstep (x+1.73*mw2, x+1.73*mw2+tfuzz, y)));
    }

  tileindex = stile+41*ttile;
  Ctile = i_tileColor * (1 + i_tileVary * snoise(tileindex+0.5));

  stain = i_stains * smoothstep (.5,1, noise(ss*i_stainFrequency,tt*i_stainFrequency));

  scuff = i_tileScuffing * smoothstep (.6,1, noise(tt*i_tileScuffFrequency-90.26,
                         ss*i_tileScuffFrequency+123.82));

  
  o_outColor = (1-stain) * mix (mix (Ctile, i_tileScuffColor, scuff), i_mortarColor, mortar);
  o_outAlpha = luminance( o_outColor );
    
    
    """
     
     

        
def initializePlugin(obj):
    dl_hextile.register(obj)

def uninitializePlugin(obj):
    dl_hextile.deregister(obj)