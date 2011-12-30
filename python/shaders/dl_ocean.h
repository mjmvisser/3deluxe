#ifndef __dl_ocean_h
#define __dl_ocean_h

/*
begin inputs
	float globalScale
	uniform float gridResolution
	float oceanSize
	float windSpeed
	float waveHeigth
	float shortestWave
	float windDirection
	float dampReflections
	float windAlign
	float oceanDepth
	float chopAmount
	uniform float doNormal
	uniform float doEigen
	float time
	uniform float seed
end inputs

begin outputs
	color outColor
	float outAlpha
	color outNormal
	float outJMinus
	float outJPlus
	color outEMinus
	color outEPlus
end outputs

begin shader_extra_parameters Pref_param
	varying point Pref = point (0, 0, 0);
end shader_extra_parameters

*/

void
maya_dl_ocean(
	// Inputs
	//
	float i_globalScale;
	uniform float i_gridResolution;
	float i_oceanSize;
	float i_windSpeed;
	float i_waveHeigth;
	float i_shortestWave;
	float i_windDirection;
	float i_dampReflections;
	float i_windAlign;
	float i_oceanDepth;
	float i_chopAmount;
	uniform float i_doNormal;
	uniform float i_doEigen;
	float i_time;
	uniform float i_seed;
	// Outputs
	//
	output color o_outColor;
	output float o_outAlpha;
	output color o_outNormal;
	output float o_outJMinus;
	output float o_outJPlus;
	output color o_outEMinus;
	output color o_outEPlus;
	)
{

extern varying point P;
extern varying point Pref;

point PP = P;
if(Pref != point(0))
    PP = Pref;

PP = transform("object", PP);

float ss = PP[0] * 1.0/i_globalScale;
float tt = PP[2] * 1.0/i_globalScale;;

float doChop = 1;
if(i_chopAmount == 0)
    doChop = 0;
    
vector disp = 1, eminus=1, eplus = 1;
normal nml = 1;
float jminus=1, jplus = 1;
ocean_eval( ss, tt, i_time, i_waveHeigth,
            doChop, i_chopAmount, disp,
            i_doNormal, nml,
            i_doEigen, jminus, jplus, eminus, eplus,
            i_gridResolution, i_oceanSize, i_windSpeed, i_shortestWave,
            i_windDirection, i_dampReflections, i_windAlign, i_oceanDepth, i_seed);
          
disp = transform("current", disp);
disp *= i_globalScale;
o_outColor = color(disp);
o_outAlpha = length(disp);

nml = ntransform("current", nml);    
o_outNormal = color(nml);
o_outJMinus = jminus;
o_outJPlus = jplus;
o_outEMinus = color(eminus);
o_outEPlus = color(eplus);
}

#endif /* __dl_ocean_h */
