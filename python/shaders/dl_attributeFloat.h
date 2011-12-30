#ifndef __dl_attributeFloat_h
#define __dl_attributeFloat_h

/*
begin inputs
	float inputValue
	uniform string attributeName
end inputs

begin outputs
	float outputValue
	float attributeExists
end outputs

*/

void
maya_dl_attributeFloat(
	// Inputs
	//
	float i_inputValue;
	uniform string i_attributeName;
	// Outputs
	//
	output float o_outputValue;
	output float o_attributeExists;
	)
{

    o_attributeExists = attribute(i_attributeName, o_outputValue);
    if(o_attributeExists == 0){ 
        o_outputValue = i_inputValue;
    }
}

#endif /* __dl_attributeFloat_h */
