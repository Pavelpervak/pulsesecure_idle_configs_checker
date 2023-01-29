"""
Module for XC operations
"""
from .parser import ET, Element, ICSXMLParser
from. parser import Union

class ICSXCOperation:
    """XC operation for XML config creation"""

    def __init__(self, xpath: str) -> None:
        self.xpath = xpath
        self.root_attrib = ICSXMLParser.root_attrib
        self.root = ''
        self.subelem = ''
        self.create_xml_model()


    def create_xml_model(self) -> None:
        """XML Model creator with XPATH"""
        if isinstance(self.xpath, str):
            xpath_list: list = self.xpath.split('/')
        else:
            raise SystemExit()

        if len(xpath_list) == 1:
            self.root: Element = ET.Element(xpath_list[0], attrib=self.root_attrib)

        self.root: Element = ET.Element(xpath_list[0], attrib=self.root_attrib)
        xpath_list.pop(0)
        parent = self.root

        for child in xpath_list:
            self.subelem = ET.SubElement(parent, child)
            parent = self.subelem


    def _delete(self, xc_element: str, child: str, value: str) -> None:
        """Setting the XC operation delete"""

        xc_delete = ET.SubElement(
            self.subelem, # End of static XML tree (don't override self.subelem after this point)
            xc_element,
            attrib={"xc:operation": "delete"})

        subelem = ET.SubElement(xc_delete, child)
        subelem.text = value


    def write_xml(self, file) -> None:
        """Writes the generated Idle XML delete config to a file"""

        ET.indent(self.root)
        etree = ET.ElementTree(self.root, file=None)
        with open(file, mode='w', encoding='utf') as fhandle:
            etree.write(
                fhandle,
                encoding='unicode',
                short_empty_elements=False,
                xml_declaration=False)


    def dump(self) -> None:
        """Indents and dumps XML tree to stdout"""
        ET.indent(self.root)
        ET.dump(self.root)


    def signin_url_delete(self, value: Union[str,set]) -> None:
        """Idle SignIn URL delete XML generation"""

        if isinstance(value, str):
            self._delete(xc_element="access-url",child="url-pattern",value=value)
        else:
            for val in value:
                self._delete(xc_element="access-url",child="url-pattern",value=val)


    def realms_delete(self, value: Union[str,set]) -> None:
        """Realms delete XML generation"""

        if isinstance(value, str):
            self._delete(xc_element="realm",child="name",value=value)
        else:
            for val in value:
                self._delete(xc_element="realm",child="name",value=val)


    def auth_servers_delete(self, value: Union[str,set]) -> None:
        """Auth Servers delete XML generation"""

        if isinstance(value, str):
            self._delete(xc_element="auth-server",child="name",value=value)
        else:
            for val in value:
                self._delete(xc_element="auth-server",child="name",value=val)


    def admin_role_delete(self, value: Union[str,set]) -> None:
        """Auth Servers delete XML generation"""

        if isinstance(value, str):
            self._delete(xc_element="admin-role",child="name",value=value)
        else:
            for val in value:
                self._delete(xc_element="admin-role",child="name",value=val)
                