/*
Compile simply like so:
    shaderdl dl_lod.sl
*/
surface dl_lod(){
    color lod_id = 0;
    attribute("user:lod_id", lod_id);
    Ci = lod_id;
    Oi = 1;
}

