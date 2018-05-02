# XSDautosyntax
This program create am XSD grammar from an XML file.
Simply call this program with proper arguments and it will generate a new file with the appropriate syntax.
Keep in mind that it *can't* understand the xs:types of each tag. Defaults are xs:string, so you could have to manually modify those.

## Usage


### Examples:  
`XSDautosyntax -i filein.xml -o fileout.xsd` to convert filein.xml into fileout.xsd if a field is not specified  
`XSDautosyntax -i filein.xml -o fileout.xsd --force-ofile-name` to force the name  
`XSDautosyntax -i filein.xml` to convert filein.xml into schema.xsd  
`XSDautosyntax -i filein.xml -c` to convert filein.xml to stdout  

### Help:  
`-i, --ifile <file>`            the input file. MUST be specified  
`-o, --ofile <file>`            the output file. Is overriden by the field in the XML file if specified. Defaults to schema.xsd  
`-e, --xml-encoding <format>`   the encoding formato of the xsd file. Defaults at "utf-8"  
`-v, --xml-version <version>`   the version of the xsd file. Defaults at "1.0"  
`-s, --xsd-schema-url <url>`    the xsd schema url. Defaults at http://www.w3.org/2001/XMLSchema  
`-c, --console`                 write on stdout instead than on the specified file.  
`--force-ofile-name`            Avoid the override of the output file name by the field on the XML. A file output must be present for this  
`--force-xs-type <type>`        force the use of a specific type for the type attribute. Defaults at "xs:string". **BE CAREFUL** no type check is done on this  
`--force-inline`                forces the use of inlines instead of the creation of subtypes. **DO NOT USE AS IT CAN PRODUCE WRONG OUTPUTS, IT ALSO DOESN'T PRODUCE APPROPRIATE ATTRIBUTES SUPPORT AND MIXED ATTRIBUTES**  
`-h, --help`                    display this useful help  
`-l`                            Shows the license  

## License
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
