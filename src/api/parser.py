"""
src.api.parser
~~~~~~~~~~~~~~
ICS XML Config Parser - wrapper for Python Stdlib ElementTree API.

"""

from typing import Optional, Generator, Union
from re import match
from xml.etree.ElementTree import ParseError, Element
import xml.etree.ElementTree as ET


class ICSXMLParser:
    """
    ICS XML Config Parser

    Wrapper class for loading and parsing the Ivanti Connect Secure (ICS) XML backup config file
    Handles automatic XML namespace handling, root setting, tag value extraction.

    Attributes:
        default_invalid_values: Ignorable value while parsing tag's text values.
        root_attrib: root element `configuration` attrib for generating XML delete configs (src.idelete.xcoperation)

        root: root element for the XML tree.
        namespace: XML namespace attrib used by the root element.
        nsmap: XML namespace used by etree API find, findall methods.

    """

    default_invalid_values = ['None', '-']
    root_attrib = {}

    def __init__(self, xml_file) -> None:
        """
        Initializes the instance with XML filepath.

        Args:
            xml_file: filepath of the XML backup file.
        
        Raises:
            FileNotFoundError: XML filepath is invalid or file not found.
            ParseError: XML structure is invalid/malformed.
            Exception: All other exceptions.
            
        """

        self.root = {}
        self.namespace = {}
        self.nsmap = {}

        try:
            with open(xml_file, encoding='utf-8') as file_handle:
                self._xml_handle = ET.parse(file_handle)

        except FileNotFoundError as fnotfound:
            raise SystemExit(f"""
            XML file not found.
            Filename - {fnotfound.filename}
            Exception type - {fnotfound.__class__.__name__}
            """) from None

        except ParseError as ferror:
            raise SystemExit(f"""
            XML Parsing failed. Please validate the XML structure and try again.
            Error details - {ferror.msg}
            Exception type - {ferror.__class__.__name__}
            """) from None

        except Exception as exc:  # Catching other generic Exceptions.
            raise SystemExit(f"{exc.__class__.__name__}: {exc}") from None

        # Pipelines the required methods = for autopopulating ns data.
        self._set_root()
        self._get_namespace()
        self._set_namespace()

    def _set_root(self) -> None:
        """Sets the root element in XML for parsing."""
        self.root = self._xml_handle.getroot()

    def _get_namespace(self) -> Optional[str]:
        """Returns the XMLNS attrib value from root element.

        Extracts the NS URI from XMLNS root attrib field and updates the attributes.
        These attributes are used for XML delete operations.
        
        Raises:
            AssertionError: Invalid XML backup file.
        """
        self.namespace = match(
            r'{(.*)}', self.root.tag).group(1)  # extracts the NS URI without {}
        setattr(self, "fnamespace", match(r'{(.*)}', self.root.tag).group(0))
        # creates NS with {} for iter root ops.
        # Gets the root attrib for XML creation.
        setattr(self, "attrib", self.root.attrib)
        try:
            assert 'xml.pulsesecure.net' in self.namespace
            # Deny if the XML file is not from ICS/PCS.
        except AssertionError as aerror:
            raise SystemExit(f"""
    XML Namespace validation failed. XMLNS not set to xml.pulsesecure.net
    Please check the XML export file and try again.
    Exception type - {aerror.__class__.__name__}
            """) from None
        # Parse the NS value between the braces.
        return self.namespace

    def _set_namespace(self) -> None:
        """Sets the XML NS value to the NS dict.
        Updates the root_attrib class instance attribute which is used by XML delete operation."""

        self.nsmap = {'': self.namespace}
        ICSXMLParser.root_attrib = {"xmlns": self.namespace} | {"xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"} | self.root.attrib

    def _findall(self, path: str) -> Generator:
        """XML Findall wrapper. See base method for more details."""

        for elem in self.root.findall(path=path, namespaces=self.nsmap):
            yield elem

    def _find(self, path: str) -> Element:
        """XML Find wrapper that uses the default root. See base method for more details."""

        return self.root.find(path=path, namespaces=self.nsmap)

    def _iterfind(self, path: str) -> Generator:
        """XML IterFind wrapper - passes namespace automatically for tags. See base method for more details."""

        for elem in self.root.iterfind(path=path, namespaces=self.nsmap):
            yield elem

    def _handle_findall(self, path: str) -> Generator:
        """XML Findall wrapper (XML Handle).
        Calls the method over the XML handle object instead of root"""

        for elem in self._xml_handle.findall(path=path, namespaces=self.nsmap):
            yield elem

    def _handle_find(self, path: str) -> Element:
        """XML Find wrapper (XML handle).
        Calls the method over the XML handle object instead of root"""

        return self._xml_handle.find(path=path, namespaces=self.nsmap)

    def _handle_iterfind(self, path: str) -> Generator:
        """XML IterFind wrapper (XML Handle).
        Calls the method over the XML handle object instead of root"""

        for elem in self._xml_handle.iterfind(path=path, namespaces=self.nsmap):
            yield elem

    def _element_findall(self, element: Element, path: str) -> Generator:
        """XML Findall wrapper (Custom Element).
        Calls the method over the custom Etree element object instead of root"""

        for elem in element.findall(path=path, namespaces=self.nsmap):
            yield elem

    def _element_findall_values(self, element: Element, path: str) -> set:
        """XML Findall wrapper (Custom Element).
        Calls the method over the custom Etree element object instead of root"""

        return {elem.text for elem in element.findall(path=path, namespaces=self.nsmap)}


    def _element_find(self, element: Element, path: str) -> Element:
        """XML Find wrapper (Custom handle).
        Calls the method over the custom Etree element object instead of root"""

        return element.find(path=path, namespaces=self.nsmap)

    def _element_find_value(self, element: Element, path: str) -> str:
        """XML Find wrapper to return TEXT value (Custom handle).
        Calls the method over the custom Etree element object instead of root"""

        return element.find(path=path, namespaces=self.nsmap).text

    def parse_element(
            self,
            path: str,
            allow_dups: bool = False,
            invalid_values: Optional[list] = None) -> Union[list, set]:
        """Returns the TEXT of the element (Uses the root findall method).
        
        Args:
            path: XPATH string.
            allow_dups: If set, duplicate text values will be allowed. Default - False.
            invalid_values: Values compared against the received text value.
        
        Returns:
            List - Contains XML tag text values if allow_dups is set to True.
            Set - Contains XML tag text values if allow_dups is set to False (default)"""

        invalid_values = ICSXMLParser.default_invalid_values if invalid_values is None else ICSXMLParser.default_invalid_values + invalid_values
        if allow_dups:  # List will be created to allow duplicates.
            return [elem.text for elem in self._findall(path=path)
                    if elem.text not in invalid_values]
        # Else SET will be created to disallow duplicates.
        return {elem.text for elem in self._findall(path=path)
                if elem.text not in invalid_values}


    def check_tree(self, tag: str) -> bool:
        """Checks for XML object presence and returns bool value.
        
        Method for checking the presence of provided tag object in the XML tree.
        This is used to do parsing operations & creating stores based on the result
        ,i.e., if this returns in False, then an empty result bucket is created
        *Employed by high-level API (src.iconfig.config.ICSIdleConfig)

        Args:
            tag: XPATH string.
        """

        check = self._find(path=tag)
        # Returns ET.Element (True) if present.
        if isinstance(check, ET.Element):
            return True
        return False


    def _element_check_tree(self, element: Element, tag: str) -> bool:
        """Checks for XML object presence and returns bool value.

        See check_tree method for more details.
        This method uses the custom XML Etree element for checking.
        
        Args:
            Element: Etree object.
            tag: XPATH string.
        """

        check = self._element_find(element,path=tag)
        # Returns ET.Element (True) if present.
        if isinstance(check, ET.Element):
            return True
        return False


    def _parse_element_dict(
            self,
            root_element: str,
            key: str,
            value: str,
            check_tree: Optional[str] = None,
            check_key: Optional[str] = None,
            check_value: Optional[str] = None) -> dict:
        """Parsing XML elements into key/value pairs
        
        Useful for parsing XML tree with conditional parsing enabled by providing
        custom root element, finding element and its value with all custom Etree
        element based APIs.
        
        Dictionary will be created based on the `text` attribute of the provided
        key and value data.

        Args:
            root_element: XML root element from where the tree is formed.
            key, value: XPATH string - tag name.
            check_tree, check_key, check_value: XPATH string - tag name (optional)

        Returns:
            Dictionary that contains the value of the provided key and value data.
        """

        return {self._element_find(element, key).text:
        {elem.text for elem in self._element_findall(element, value) if elem.text is not None}
        for element in self._handle_iterfind(root_element)
        if self._element_check_tree(element, check_tree)
        if self._element_find(element, path=check_key).text == check_value}
