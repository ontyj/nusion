
def convert(node):
    """ Convert Nuke common effect attributes to Fusion

    Returns:
        dict with fusion formatted common attributes.
    """
    
    nuke_effect_attribs = node.effect_attribs
    fusion_effect_attribs = {}
    
    for knob in nuke_effect_attribs:
        value = nuke_effect_attribs[knob]

        if knob == "mix":
            fusion_effect_attribs["Blend"] = f"Input {{ Value = {value}, }}"

        if knob == "channels":
            if value == "all":
                #Fusion only supports RGBA channel processing
                #TODO: Flag to user if there are any extra channels in the pipe.
                pass
            if value == "rgb":
                fusion_effect_attribs["ProcessAlpha"] = "Input {Value = 0, }"
            if value == "alpha":
                fusion_effect_attribs["ProcessRed"] = "Input {Value = 0, }"
                fusion_effect_attribs["ProcessGreen"] = "Input {Value = 0, }"
                fusion_effect_attribs["ProcessBlue"] = "Input {Value = 0, }"
            if value.startswith("{"): #individual channels selected
                if "-rgba.red" in value:
                    fusion_effect_attribs["ProcessRed"] = "Input {Value = 0, }"
                if "-rgba.green" in value:
                    fusion_effect_attribs["ProcessGreen"] = "Input {Value = 0, }"
                if "-rgba.blue" in value:
                    fusion_effect_attribs["ProcessBlue"] = "Input {Value = 0, }"
                if "-rgba.alpha" in value:
                    fusion_effect_attribs["ProcessAlpha"] = "Input {Value = 0, }"


    return fusion_effect_attribs

if __name__ == '__main__':
    help(convert)
