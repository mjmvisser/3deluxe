import string

class Channel(object):
        
    def __init__(self, longname, shortname=None, apitype='Color', lightset=False,  component=True, auxiliary=False,code=None, group=None, defined=False):
        
        # OpenExr has a max of 32 chars
        # A typical exr channel goes like this: aovname.000.r
        # At least 6 chars are reserved for ".000.r"
        # We are also adding lighset index using this convension: "_ls1" : aovname_ls1.000.r
        # At least 4 chars should be reserved for this, but more could be needed if more than 10 lighsets...
        # At least 10 chars need to be reserved
        if len(longname) > 22:
            raise Exception('Channel name too long, it will not fit in openExr channel name.', longname)
        
        #   
        self.longname = longname
        
        self.shortname = shortname
        if self.shortname == None:
            self.shortname = self.longname
            
        self.apitype = apitype
        self.lightset = lightset
        self.component = component
        self.auxiliary = auxiliary
        if self.auxiliary:
            self.component=False
        self.code = code
        self.group = group
        
        #
        self.array = lightset
        self.type = apitype + ['', 'Array'][self.array]
        self.rsltype = self.apitype.lower()
        
        self.defined = defined
        
    #
    def getLightsetSuffix(self, lightsetindex=None):
        lightsetSuffix = '_ls'
        if lightsetindex is not None and lightsetindex >= 0:
            lightsetSuffix += str(lightsetindex)
        return lightsetSuffix
        
    #
    def getName(self, lightsetindex=None):
        aovname = self.longname
        if self.lightset:
            aovname += self.getLightsetSuffix(lightsetindex)
        return aovname

#
lightsetcount = 6

#
channels = [
                
                # The total result of any shading component, used for beauty only
                Channel(longname='beauty',                          shortname='bty'),
                
                #                
                Channel(longname='light',                           shortname='lig',    lightset=True),
                
                #
                Channel(longname='diffuse_unocc',                   shortname='duo',    lightset=True,  group='LS'),
                Channel(longname='diffuse_shad',                    shortname='dsh',    lightset=True,  group='LS'),
                Channel(longname='specular_unocc',                  shortname='suo',    lightset=True,  group='LS'),
                Channel(longname='specular_shad',                   shortname='ssh',    lightset=True,  group='LS'),
                Channel(longname='translucence_unocc',              shortname='tuo',    lightset=True,  group='LS'),
                Channel(longname='translucence_shad',               shortname='tsh',    lightset=True,  group='LS'),
                Channel(longname='diffuse_unocc_sc',                shortname='duos',   lightset=True,  group='LS'),
                Channel(longname='diffuse_shad_sc',                 shortname='dshs',   lightset=True,  group='LS'),
                Channel(longname='specular_unocc_sc',               shortname='suos',   lightset=True,  group='LS'),
                Channel(longname='specular_shad_sc',                shortname='sshs',   lightset=True,  group='LS'),
                Channel(longname='translucence_unocc_sc',           shortname='tuos',   lightset=True,  group='LS'),
                Channel(longname='translucence_shad_sc',            shortname='tshs',   lightset=True,  group='LS'),
                
                #
                Channel(longname='diffuse_surf',                    shortname='dsu',    group='SURF'),
                Channel(longname='specular_surf',                   shortname='ssu',    group='SURF'),
                Channel(longname='incandescence',                   shortname='inc',    group='SURF'),
                
                #
                Channel(longname='ambient',                         shortname='amb',    group='ENV'),
                Channel(longname='indirect_unocc',                  shortname='iuo',    group='ENV'),
                Channel(longname='indirect_shad',                   shortname='ish',    group='ENV'),
                Channel(longname='indirect_unocc_sc',               shortname='iuos',    group='ENV'),
                Channel(longname='indirect_shad_sc',                shortname='ishs',    group='ENV'),                
                Channel(longname='reflection_env',                  shortname='rfle',    group='ENV' ),
                Channel(longname='occlusion',                       shortname='occ',    group='ENV'),
                Channel(longname='bentnormal',                      shortname='bnl',    group='ENV'),

                #
                Channel(longname='reflection',                      shortname='rfl',    group='TRACE'),
                Channel(longname='reflection_depth',                shortname='rfd',    group='TRACE'),
                Channel(longname='refraction',                      shortname='rfr',    group='TRACE'),
                Channel(longname='subsurface',                      shortname='sss',    group='TRACE'),
                
                
                # TODO: Implement lightset support for collect_direct_shadow
                Channel(longname='collect_direct_shad',             shortname='cds',     group='SHAD', lightset=True,),
                Channel(longname='collect_indirect_shad',           shortname='cis',     group='SHAD'),
                
                
                # BTY
                Channel(longname='rgba',                component=False,    group='BTY',    defined=True),
                
                Channel(longname='facing_ratio',        auxiliary=True,     group='AUX',    code='-In.ShadingNormal(Nn) * premult'),
                Channel(longname='z_depth',             auxiliary=True,     group='AUX',    code='depth(P) * premult'),
                Channel(longname='xyz_camera',          auxiliary=True,     group='AUX',     code='color(comp(P, 0), comp(P, 1), comp(P, 2)) * premult'),
                Channel(longname='xyz_world',           auxiliary=True,     group='AUX',     code='color(transform("world", P)) * premult'),
                Channel(longname='xyz_object',          auxiliary=True,     group='AUX',     code='color(transform("object", P)) * premult'),
                Channel(longname='uv_coord',            auxiliary=True,     group='AUX',     code='color(s, t, 0) * premult'),
                Channel(longname='normal_world',        auxiliary=True,     group='AUX',     code='color(normalize(ntransform("world", N))) * premult'),                

                Channel(longname='alpha',               component=False,    group='MASK',    defined=True,   apitype='Float'),
                Channel(longname='opacity',             component=False,    group='MASK'),
                Channel(longname='lod_id',              auxiliary=True,     group='MASK',     code='color(0);attribute("user:lod_id", lod_id);lod_id *= premult'),
                Channel(longname='puzzle_1',            auxiliary=True,     group='MASK',     code='i_puzzle1; attribute("user:puzzle_1", puzzle_1);puzzle_1 *= premult'),                
                Channel(longname='puzzle_2',            auxiliary=True,     group='MASK',     code='i_puzzle2; attribute("user:puzzle_2", puzzle_2);puzzle_2 *= premult'),                
                Channel(longname='puzzle_3',            auxiliary=True,     group='MASK',     code='i_puzzle3; attribute("user:puzzle_3", puzzle_3);puzzle_3 *= premult'),                
                Channel(longname='puzzle_id',           auxiliary=True,     group='MASK',     code="""color(0);
    string hashString = "";
    attribute("user:delight_shortest_unique_name", hashString);
    attribute("user:puzzle_id_set", hashString);
    float hash = lm_hash(hashString);
    puzzle_id = cellnoise(hash) * premult;"""),
                    
                Channel(longname='layer_id',            auxiliary=True,     group='MASK',     code="""0;
    float i;
    for (i=0; i<arraylength(i_layerNames); i += 1) {
        color op = i_layerOpacities[i];
        float tolerance = .0001;
        if (op[0] > tolerance || op[1] > tolerance || op[2] > tolerance) {
            string layerName = i_layerNames[i];
            float hash = lm_hash(layerName);
            layer_id = cellnoise(hash);;
        }
    }"""),
            ]

    
#
def getDisplayChannelsParam(group, lightsetindex=None):    
    groupchannels = filter(lambda channel: channel.group == group, channels)
    return string.join(['%s%s'%(['%s '%channel.rsltype, ''][channel.defined], channel.getName(lightsetindex)) for channel in groupchannels], ', ')

#
def getChannelGroups():
    groups=[]
    for channel in channels:
        if channel.group and channel.group not in groups:
            groups.append(channel.group)
    return groups


    
    
