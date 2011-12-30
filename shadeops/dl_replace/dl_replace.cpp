#include <shadeop.h>
#include <string>
#include <string>
#include <algorithm>
using namespace std;

string replace_all_copy(const string& haystack, const string& needle, const string& replacement)
{
    if (needle.empty())
    {
        return haystack;
    }

    string result;
    for (string::const_iterator substart = haystack.begin(), subend; ; )
    {
        subend = search(substart, haystack.end(), needle.begin(), needle.end());
        copy(substart, subend, back_inserter(result));
        if (subend == haystack.end())
        {
            break;
        }
        copy(replacement.begin(), replacement.end(), back_inserter(result));
        substart = subend + needle.size();
    }
    return result;
}

extern "C"
{

SHADEOP_TABLE(lm_replace) = {
		{ "string lm_replace(string, string, string)", "lm_replace_init", "lm_replace_cleanup" },
		{ "" }
};

SHADEOP_INIT(lm_replace_init)
{
	return 0x0; /* No init data */
}

SHADEOP( lm_replace )
{
	char **result = (char **)(argv[0]);
	const char **haystack = (const char **)(argv[1]);
	const char **needle = (const char **)(argv[2]);
	const char **replacement = (const char **)(argv[3]);

	string product = replace_all_copy(string(*haystack), string(*needle), string(*replacement));

	ASSIGN_STRING(*result, product.c_str());

	return 0;
}

SHADEOP_CLEANUP( lm_replace_cleanup )
{
	/* Nothing to do */
}

}
