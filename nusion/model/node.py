from nusion.model.nodes import nuke_to_fusion

class Node():
    """
    Node class to serve as an intermediate between Nuke and Fusion.
    """

    def __init__(self, software, effect, base_attribs, effect_attribs, resolution):
        self.software = software
        self.effect = effect
        self.base_attribs = base_attribs
        self.effect_attribs = effect_attribs
        self.resolution = resolution
        self.root_width = resolution["w"]
        self.root_height = resolution["h"]
        if self.software == "nuke":
            self.name = base_attribs["name"]

    def to_fusion(self):
        """
        Convert the nuke node class to a fusion node class.
        """
        if self.software != "nuke":
            raise ValueError("Expected node from 'nuke' got '{}' instead".format(self.software))

        self.base_attribs, self.effect_attribs = nuke_to_fusion.convert(self)
        self.software = "fusion"

    def output(self):
        """
        Get's the node class ready for output in relevant software.
        """
        if self.software == "fusion":
            output_effect_attribs = ""
            output_base_attribs = ""
            for i, effect in enumerate(self.effect_attribs):
                output_effect_attribs += f"{effect} = {self.effect_attribs[effect]},"
                if i != len(self.effect_attribs)-1: #Add newline character if this is not the last effect attribute.
                    output_effect_attribs += "\n"
            for i, attrib in enumerate(self.base_attribs):
                output_base_attribs += f"{self.base_attribs[attrib]},"
                if i != len(self.base_attribs)-1: #Add newline character if this is not the last base attribute.
                    output_base_attribs += "\n"

            node_output = f"{self.name} = {self.effect} {{\nInputs = {{\n{output_effect_attribs}\n}},\n{output_base_attribs}\n}}"
            return node_output

    @staticmethod
    def from_nuke(node_string, resolution):
        """
        Add a node with nuke script formatting.
        Assumes there may be extra data at the end of the node string and filters it out.

        Returns:
            Node class with all attributes from nuke string input.
        """
        node_raw = Node.extract_node_from_nuke(node_string)
        effect = node_raw[0].replace(" {", "")
        base_attribs, effect_attribs = Node.get_nuke_attribs(node_raw)
        return Node("nuke", effect, base_attribs, effect_attribs, resolution)

    @staticmethod
    def extract_node_from_nuke(node_string):
        """
        Parse nuke input to extract a single node.

        Returns:
            single_node (list)
        """
        single_node = []
        for line in node_string:
            single_node.append(line.strip())
            if line == "}\n":
                break
        return single_node

    @staticmethod
    def get_nuke_attribs(node_raw):
        """
        Extract and seperate node attributes into dicts from a raw node list.

        Returns:
            base_attribs (dict), effect_attribs (dict)
        """
        nuke_base_attributes = ["name", "disable", "xpos", "ypos"]
        nuke_ignore_attributes = ["selected"]
        base_attribs = {}
        effect_attribs = {}
        for item in node_raw[1:-1]:
            attrib = item.split(" ")[0]
            if attrib not in nuke_ignore_attributes:
                if attrib in nuke_base_attributes:
                    base_attribs[attrib] = item.replace(attrib, "").strip()
                else:
                    effect_attribs[attrib] = item.replace(attrib, "").strip()
        return base_attribs, effect_attribs
