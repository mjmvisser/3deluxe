#include <shadeop.h>

// djb2 hash by dan bernstein
// http://www.cse.yorku.ca/~oz/hash.html

int stringHash(const char *str)
{
    int hash = 5381;
    int c;

    while (c = (const unsigned char)(*str++))
    hash = ((hash << 5) + hash) + c; // hash * 33 + c

    return hash;
}


// 32-bit hash by thomas wang
// http://www.concentric.net/~Ttwang/tech/inthash.htm

int hash32shift(int key)
{
  key = ~key + (key << 15); // key = (key << 15) - key - 1;
  key = key ^ (key >> 12);
  key = key + (key << 2);
  key = key ^ (key >> 4);
  key = key * 2057; // key = (key + (key << 3)) + (key << 11);
  key = key ^ (key >> 16);
  return key;
}

extern "C" {

SHADEOP_TABLE(dl_hash) = {
		{ "float dl_hash(string)", "dl_hash_init", "dl_hash_cleanup" },
		{ "" }
};

SHADEOP_INIT(dl_hash_init)
{
	return 0x0; /* No init data */
}

SHADEOP( dl_hash )
{
	float *result = (float *)(argv[0]);
	const char **str = (const char **)(argv[1]);
    result[0] = hash32shift(stringHash(*str));

	return 0;
}

SHADEOP_CLEANUP( dl_hash_cleanup )
{
	/* Nothing to do */
}

}
