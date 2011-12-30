#ifndef __dl_axisProject_h
#define __dl_axisProject_h

/*
begin inputs
	vector scale
	uniform string coordsys
end inputs

begin outputs
	init={ss,tt} float2 xst
	init={ss,tt} float2 yst
	init={ss,tt} float2 zst
end outputs

*/

void
maya_dl_axisProject(
	// Inputs
	//
	vector i_scale;
	uniform string i_coordsys;
	// Outputs
	//
	output float o_xst[2];
	output float o_yst[2];
	output float o_zst[2];
	)
{

    extern point P;
    string coordsys = i_coordsys == "" ? "world" : i_coordsys;
    point Pw = transform(coordsys, P)/i_scale;

    o_xst[0] = (Pw[1] + 1)/2;
    o_xst[1] = (Pw[2] + 1)/2;
    o_yst[0] = (Pw[0] + 1)/2;
    o_yst[1] = (Pw[2] + 1)/2;
    o_zst[0] = (Pw[0] + 1)/2;
    o_zst[1] = (Pw[1] + 1)/2;
    

}

#endif /* __dl_axisProject_h */
