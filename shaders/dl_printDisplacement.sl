surface dl_printDisplacement (
    float clrScale = 1;
    float outputDisp = 1;
) {
    varying point Porig = P;
    displacement("__Porig", Porig);
    point PorigW = transform("world", Porig);
    point Pw = transform("world", P);
    vector Pdiff =Pw - PorigW;
    string uniqueName = "UNNAMED";
    attribute("user:delight_shortest_unique_name", uniqueName);
    if (outputDisp > 0) 
        printf ("\ndispBound,%s,%06.2f,\n", uniqueName, length(Pdiff));

    Ci = .5 + .5 * (color Pdiff) * clrScale;

}
