surface dl_ptcDensity(
    string pointcloud = "";
    float mult = 1;
) {
    float _area;
    float got = texture3d(pointcloud, P, N, "_area", _area );
    _area = 1/_area;
    Ci = _area * mult * .0001;
    Oi = 1;
}
