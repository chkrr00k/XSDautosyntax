# XSDautosyntax
This program create am XSD grammar from an XML file.
Simply call this program with proper arguments and it will generate a new file with the appropriate syntax.
Keep in mind that it *can't* understand the xs:types of each tag. Defaults are xs:string, so you could have to manually modify those.

## XXX
CURRENTLY ATTRIBUTES AREN'T SUPPORTED

Examples:  
`XSDautosyntax -i filein.xml -o fileout.xsd` to convert filein.xml into fileout.xsd   
`XSDautosyntax -i filein.xml` to convert filein.xml into schema.xsd  
`XSDautosyntax -i filein.xml -c` to convert filein.xml to stdout  

Use:  
`-i, --ifile`    the input file. MUST be specified  
`-o, --ofile`               the output file. Is overriden by the field in the XML file if specified. Defaults to schema.xsd  
`-e, --xml-encoding`        the encoding formato of the xsd file. Defaults at "utf-8"  
`-v, --xml-version`         the version of the xsd file. Defaults at "1.0"  
`-s, --xsd-schema-url`      the xsd schema url. Defaults at http://www.w3.org/2001/XMLSchema  
`-c, --console`          write on stdout instead than on the specified file.  
`--force-inline`          forces the use of inlines instead of the creation of subtypes.  
`-h, --help`              display this useful help  
