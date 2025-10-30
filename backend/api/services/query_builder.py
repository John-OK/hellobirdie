from decimal import Decimal, ROUND_FLOOR, ROUND_CEILING


def round_coordinate_outwards(coordinate, round_direction):
    # NOTE: round_direction should be either ROUND_FLOOR or ROUND_CEILING
    coordinate_decimal = Decimal(str(coordinate))
    coordinate_rounded_outwards = coordinate_decimal.quantize(
        Decimal("0.01"), rounding=round_direction
    )
    return str(coordinate_rounded_outwards)


def normalize_filter_value(tag):
    if tag is not None:
        if tag.strip() == "":
            tag = None
        else:
            tag = " ".join(tag.split())
    return tag


def build_tags(lat_min, lon_min, lat_max, lon_max, gen=None, sp=None, en=None):
    tags = ["grp:birds"]
    lat_min_rounded = round_coordinate_outwards(lat_min, ROUND_FLOOR)
    lon_min_rounded = round_coordinate_outwards(lon_min, ROUND_FLOOR)
    lat_max_rounded = round_coordinate_outwards(lat_max, ROUND_CEILING)
    lon_max_rounded = round_coordinate_outwards(lon_max, ROUND_CEILING)

    box = f"box:{lat_min_rounded},{lon_min_rounded},{lat_max_rounded},{lon_max_rounded}"
    tags.append(box)

    gen = normalize_filter_value(gen)
    if gen is not None:
        gen = f"gen:{gen}"
        tags.append(gen)

    sp = normalize_filter_value(sp)
    if sp is not None:
        sp = f"sp:{sp}"
        tags.append(sp)

    en = normalize_filter_value(en)
    if en is not None:
        en = f"en:{en}"
        tags.append(en)

    return tags
