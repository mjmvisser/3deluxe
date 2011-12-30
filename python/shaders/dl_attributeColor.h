#ifndef __dl_attributeColor_h
#define __dl_attributeColor_h

/*
begin inputs
	color inputValue
	uniform string attributeName
end inputs

begin outputs
	color outputValue
	float attributeExists
end outputs

*/

void
maya_dl_attributeColor(
	// Inputs
	//
	color i_inputValue;
	uniform string i_attributeName;
	// Outputs
	//
	output color o_outputValue;
	output float o_attributeExists;
	)
{

    o_attributeExists = attribute(i_attributeName, o_outputValue);
    if(o_attributeExists == 0){ 
        o_outputValue = i_inputValue;
    }
}

#endif /* __dl_attributeColor_h */
