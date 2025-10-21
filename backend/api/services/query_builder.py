def build_tags(lat_min, lon_min, lat_max, lon_max, gen, sp, en):
    box = f"box:{lat_min},{lon_min},{lat_max},{lon_max}"
    gen = f"gen:{gen}"
    sp = f"sp:{sp}"
    en = f"en:{en}"
    return ["grp:birds", box, gen, sp, en]
