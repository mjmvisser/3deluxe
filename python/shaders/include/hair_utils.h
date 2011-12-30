#ifndef __hair_utils_h
#define __hair_utils_h

normal
getHairNormal
(
		normal skin_normal,
		float shade_as_skin
)
{
	extern vector dPdv;

	vector T = normalize(dPdv);

	// obtain a normal perpendicular to the tangent and the skin normal
	normal Nh = T ^ (skin_normal ^ T);

	// hair is parallel to surface -> Ns = skin_normal
	// hair is perpendicular to surface -> Ns = Nh
	float blend = clamp(skin_normal . T, 0, 1);
	normal Ns = mix(Nh, skin_normal, blend);

	// user control: shade_as_skin = 0 -> Nf = Nh
	//               shade_as_skin = 1 -> Nf = Ns
	return mix(Nh, Ns, shade_as_skin);
}
