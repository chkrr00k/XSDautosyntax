import xml.etree.ElementTree as ET
import sys
import getopt
import collections


HELP_MESSAGE = """Help:
Create .XSD grammar file for a given .XML file.

-i, --ifile <file>            the input file. MUST be specified
-o, --ofile <file>            the output file. Is overriden by the field 
                              in the XML 
                              file if specified. Defaults to schema.xsd
-e, --xml-encoding <format>   the encoding formato of the xsd file.
                              Defaults at "utf-8"
-v, --xml-version <version>   the version of the xsd file. Defaults at "1.0"
-s, --xsd-schema-url <url>    the xsd schema url. 
                              Defaults at http://www.w3.org/2001/XMLSchema
-c, --console                 write on stdout instead than on 
                              the specified file.
--force-ofile-name            Avoid the override of the output file name by
                              the field on the XML.
                              A file output must be present for this
--force-xs-type <type>        force the use of a specific type for 
                              the type attribute
                              Defaults at "xs:string".
                              BE CAREFUL no type check is done on this
--force-inline                forces the use of inlines instead of the creation
                              of subtypes. DO NOT USE AS IT CAN PRODUCE WRONG
                              OUTPUTS, IT ALSO DOESN'T PRODUCE APPROPRIATE 
                              ATTRIBUTES SUPPORT AND MIXED ATTRIBUTES
-h, --help                    display this useful help
-l                            Shows the license
"""
LICENSE_MESSAGE="""
    #############################################################
    #                                                           #
    #   This program is relased in the GNU GPL v3.0 license     #
    #   you can modify/use this program as you wish. Please     #
    #   link the original distribution of this software. If     #
    #   you plan to redistribute your modified/copied copy      #
    #   you need to relased the in GNU GPL v3.0 licence too     #
    #   according to the overmentioned licence.                 #
    #                                                           #
    #   "PROUDLY" MADE BY chkrr00k (i'm not THAT proud tbh)     #
    #                                                           #
    #############################################################
    #                                                           #
    #                                                           #
    #                            YEE                            #
    #                                                           #
    #                                                           #
    #############################################################
    """
class StringBuffer:
    def __init__(self, input : str):
        self.storage = []
        self.storage.append(input)
    def append(self, input : str):
        self.storage.append(input)
    def toString(self) -> str:
        return "".join(self.storage)

def printLevel(input : str, level : int, sep="\t", end="\n"):
    buf.append((sep * level) + input + end)

def inspect(root : ET.Element, level : int):
    printLevel("<xs:element name=\"" + root.tag + "\"",level, end="")
    if len(root) > 0:
        printLevel(">", 0)
        printLevel("<xs:complexType>", level + 1)
        printLevel("<xs:sequence>", level + 1)
        for child in root:
            inspect(child, level + 2)
        printLevel("</xs:sequence>", level + 1)
        printLevel("</xs:complexType>", level + 1)
        printLevel("</xs:element>", level)
    else:
        printLevel(" type=\"xs:string\"/>", 0)
    
def getArguments(argv : list) -> dict:
    ofile = False
    result = {
        "inputFile" : None,
        "outputFile" : "schema.xsd",
        "encoding" : "utf-8",
        "xmlVersion" : "1.0",
        "xsSchemaUrl" : "http://www.w3.org/2001/XMLSchema",
        "console" : False,
        "inline" : False,
        "xsType" : "xs:string",
        "fileOverride" : False
        }

    try:
        opts, args = getopt.getopt(argv, "hi:o:e:v:s:cl", ["help", "ifile=", "ofile=", "xml-encoding=", "xml-version=", "xsd-schema-url=", "console", "force-inline", "force-xs-type=", "force-ofile-name"])
    except getopt.GetoptError:
        print("Error in arguments\n")
        print(HELP_MESSAGE)
        sys.exit(1)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(HELP_MESSAGE)
            sys.exit(0)
        elif opt in ("-l"):
            print(LICENSE_MESSAGE)
            sys.exit(0)
        elif opt in ("-i", "--ifile"):
            if arg.lower().endswith(".xml"):
                result["inputFile"] = arg
            else:
                sys.stderr.write("File must be a .xml file")
        elif opt in ("-o", "--ofile"):
            if arg.lower().endswith(".xsd"):
                result["outputFile"] = arg
                ofile = True
            else:
                sys.stderr.write("File must be a .xsd file")
        elif opt in ("-e", "--xml-encoding"):
            result["encoding"] = arg
        elif opt in ("-v", "--xml-version"):
            result["xmlVersion"] = arg
        elif opt in ("-s", "--xsd-schema-url"):
            result["xsSchemaUrl"] = arg
        elif opt in ("-c", "--console"):
            result["console"] = True
        elif opt in ("--force-inline"):
            result["inline"] = True
        elif opt in ("--force-xs-type"):
            result["xsType"] = arg
        elif opt in ("--force-ofile-name"):
            result["fileOverride"] = True

    if result["fileOverride"]:
        if not ofile:
            print(result["fileOverride"] , ofile)
            print("Error, you must specify the output file (option -o) with the --force-ofile-name\n")
            print(HELP_MESSAGE)
            sys.exit(3)
    return result

class XSDEl:
    def __init__(self, el : ET.Element, times : int = 1, obb : bool = True, mul : bool = True):
        self.times = times
        self.el = el
        self.tag = el.tag
        self.obb = obb
        self.mul = False
    def __eq__(self, other):
        return self.tag == other.tag
    def __str__(self):
        return self.tag + " " + str(self.times) + " " + str(self.obb)
    def __unicode__(self):
        return self.tag + " " + str(self.times) + " " + str(self.obb)
    def __repr__(self):
        return self.tag + " " + str(self.times) + " " + str(self.obb)

class XSDCo:
    def __init__(self, tag : str, attrib : dict):
        self.tag = tag
        self.storage = collections.OrderedDict()
        self.attrib = attrib
    def append(self, el : XSDEl):
        if el.tag not in self.storage:
            self.storage[el.tag] = el
        else:
            self.storage[el.tag].times += 1
            self.storage[el.tag].el.attrib.update(el.el.attrib)
    def __eq__(self, other):
        return self.tag == other.tag
    def __hash__(self):
        return hash((self.tag))
    def __str__(self):
        return self.tag + " " + str(self.storage)
    def __unicode__(self):
        return self.tag + " " + str(self.storage)
    def __repr__(self):
        return self.tag + " " + str(self.storage)

def generateTree(root : ET.Element):
    result = list()
    tmp = XSDCo(root.tag, root.attrib)
    for child in root:
        tmp.append(XSDEl(child))
        result += generateTree(child)

    result.append(tmp)
    return result

def subType(root : ET.Element, xsType : str):
    tree = generateTree(root)
    complex = [el for el in tree if len(el.storage) > 0]
    newcomp = list()

    for part in complex:
        tmp = [el for el in complex if el.tag == part.tag]
        if tmp not in newcomp:
            newcomp.append(tmp)

    els = collections.OrderedDict()
    for elements in newcomp:
        for part in elements:
            if part.tag not in els:
                els[part.tag] = XSDCo(part.tag, part.attrib)
                for a in part.storage:
                    els[part.tag].append(part.storage[a])
            else:
                for a in part.storage:
                    els[part.tag].append(part.storage[a])

        for name, field in els[part.tag].storage.items():
            if field.times < len(elements):
                field.obb = False
            elif field.times > len(elements):
                field.mul = True
    complex = [t.tag for t in complex]

    for tag, datas in els.items():
        
        printLevel("<xs:complexType name=\"" + tag + "Type\">", 1)
        printLevel("<xs:sequence>", 2)

        for sub in datas.storage:

            if sub not in complex:
                if datas.storage[sub].el.text is not None:
                    type = " type=\"" + xsType + "\""
                else:
                    type = ""
            else:
                type = " type=\"" + sub + "Type\""

            obb = " minOccurs=\"0\"" if not datas.storage[sub].obb else ""
            mul = ""
            if datas.storage[sub].mul:
                mul = " maxOccurs=\"" + str(datas.storage[sub].times) + "\""

            if len(datas.storage[sub].el.attrib) > 0 and sub not in complex:
                if datas.storage[sub].el.text is None:
                    printLevel("<xs:element name=\"" + sub + "\"" + obb + mul +  ">", 3)
                    printLevel("<xs:complexType>", 4)
                    for at in datas.storage[sub].el.attrib:
                        printLevel("<xs:attribute name=\"" + at + "\" type=\"" + xsType + "\"/>", 5)
                    printLevel("</xs:complexType>", 4)
                    printLevel("</xs:element>", 3)
                else:
                    printLevel("<xs:element name=\"" + sub + "\"" + obb + mul +  ">", 3)
                    printLevel("<xs:complexType>", 4)
                    printLevel("<xs:simpleContent>", 5)
                    printLevel("<xs:extension base=\"" + xsType + "\">", 6)
                    for at in datas.storage[sub].el.attrib:
                        printLevel("<xs:attribute name=\"" + at + "\" type=\"" + xsType + "\"/>", 7)
                    printLevel("</xs:extension>", 6)
                    printLevel("</xs:simpleContent>", 5)
                    printLevel("</xs:complexType>", 4)
                    printLevel("</xs:element>", 3)
            else:
                printLevel("<xs:element name=\"" + sub + "\"" + type + obb + mul + "/>", 3)
      
        printLevel("</xs:sequence>", 2)

        for name in datas.attrib:
            if not name.find("NamespaceSchemaLocation") > 0:
                printLevel("<xs:attribute name=\"" + name + "\" type=\"" + xsType + "\"/>", 2)

        printLevel("</xs:complexType>", 1)

    printLevel("<xs:element name=\"" + root.tag + "\" type=\"" + root.tag + "Type\"/>", 1)

def main(argv):
    global buf 

    args = getArguments(argv)
    if args["inputFile"] is None:
        print("Error, you must specify the input file (option -i)\n")
        print(HELP_MESSAGE)
        sys.exit(3)
    buf = StringBuffer("<?xml version=\"" + args["xmlVersion"] +"\" encoding=\"" + args["encoding"] + "\"?>\n")
    buf.append("<xs:schema xmlns:xs=\"" + args["xsSchemaUrl"] + "\">\n")
    try:
        tree = ET.parse(args["inputFile"])
    except FileNotFoundError as err:
        sys.stderr.write("The inserted file doesn't exist or have problems: " + str(err))
        sys.exit(2)
    root = tree.getroot()
    if args["fileOverride"]:
        fileName = args["outputFile"]
    else:
        try:
            fileName = root.get(list(filter(lambda x:x.find("NamespaceSchemaLocation"), root.attrib))[0], args["outputFile"])
        except:
            fileName = args["outputFile"]

    if args["inline"]:
        print("WARNING THIS OPTION IS DEPRECATED AND IT'S SUGGESTED TO NOT USE BECAUSE OF IT'S INCORRECTED RESULTS\n(See the --help to know more)\n\n")
        inspect(root, 1)
    else:
        subType(root, args["xsType"])
    buf.append("</xs:schema>\n")

    if args["console"]:
        print(buf.toString())
    else:
        with(open(fileName, "w+")) as f:
            f.write(buf.toString())

if __name__ == "__main__":
    main(sys.argv[1:])
