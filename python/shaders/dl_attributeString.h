#ifndef __dl_attributeString_h
#define __dl_attributeString_h

/*
begin inputs
	uniform string inputValue
	uniform string attributeName
end inputs

begin outputs
	uniform string outputValue
	float attributeExists
end outputs

*/

void
maya_dl_attributeString(
	// Inputs
	//
	uniform string i_inputValue;
	uniform string i_attributeName;
	// Outputs
	//
	output uniform string o_outputValue;
	output float o_attributeExists;
	)
{

    o_attributeExists = attribute(i_attributeName, o_outputValue);
    if(o_attributeExists == 0){ 
        o_outputValue = i_inputValue;
    }
}

#endif /* __dl_attributeString_h */
