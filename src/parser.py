"""
ICS XML Parser Class
"""
from typing import Optional, Generator, Union
from re import match
from xml.etree.ElementTree import ParseError, Element
import xml.etree.ElementTree as ET


class ICSXMLParser:
    """Class for creating ICS XML Parser Instances"""

    default_invalid_values = ['None', '-']
    root_attrib = {}

    def __init__(self, xml_file) -> None:

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
        """Sets the root element in XML for parsing"""
        self.root = self._xml_handle.getroot()

    def _get_namespace(self) -> Optional[str]:
        """Gets the namespace using QNAME class from lxml.etree module"""
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
        else:
            return self.namespace

    def _set_namespace(self) -> None:
        """Sets the XML NS value to the NS dict"""

        self.nsmap = {'': self.namespace}
        ICSXMLParser.root_attrib = {"xmlns": self.namespace} | {"xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"} | self.root.attrib


    def _findall(self, path: str) -> Generator:
        """XML Findall wrapper"""

        for elem in self.root.findall(path=path, namespaces=self.nsmap):
            yield elem


    def _find(self, path: str) -> Element:
        """XML Find wrapper that uses the default root"""

        return self.root.find(path=path, namespaces=self.nsmap)


    def _iterfind(self, path: str) -> Generator:
        """XML IterFind wrapper - passes namespace automatically for tags"""

        for elem in self.root.iterfind(path=path, namespaces=self.nsmap):
            yield elem


    def _handle_findall(self, path: str) -> Generator:
        """XML Findall wrapper (XML Handle)"""

        for elem in self._xml_handle.findall(path=path, namespaces=self.nsmap):
            yield elem


    def _handle_find(self, path: str) -> Element:
        """XML Find wrapper (XML handle)"""

        return self._xml_handle.find(path=path, namespaces=self.nsmap)


    def _handle_iterfind(self, path: str) -> Generator:
        """XML IterFind wrapper (XML Handle)"""

        for elem in self._xml_handle.iterfind(path=path, namespaces=self.nsmap):
            yield elem


    def _element_findall(self, element: Element, path: str) -> Generator:
        """XML Findall wrapper (Custom Element)"""

        for elem in element.findall(path=path, namespaces=self.nsmap):
            yield elem

    def _element_findall_values(self, element: Element, path: str) -> set:
        """XML Findall wrapper (Custom Element)"""

        return {elem.text for elem in element.findall(path=path, namespaces=self.nsmap)}


    def _element_find(self, element: Element, path: str) -> Element:
        """XML Find wrapper (Custom handle)"""

        return element.find(path=path, namespaces=self.nsmap)

    def _element_find_value(self, element: Element, path: str) -> Element:
        """XML Find wrapper to return TEXT value (Custom handle)"""

        return element.find(path=path, namespaces=self.nsmap).text


    def parse_element(
            self,
            path: str,
            allow_dups: bool = False,
            invalid_values: Optional[list] = None) -> Union[list, set]:
        """Returns the TEXT of the element (Uses the root findall method)"""

        invalid_values = ICSXMLParser.default_invalid_values if invalid_values is None else ICSXMLParser.default_invalid_values + invalid_values
        if allow_dups:  # List will be created to allow duplicates.
            return [elem.text for elem in self._findall(path=path)
                    if elem.text not in invalid_values]
        # Else SET will be created to disallow duplicates.
        return {elem.text for elem in self._findall(path=path)
                if elem.text not in invalid_values}


    def check_tree(self, tag: str) -> bool:
        """Checks the tag presence"""
        check = self._find(path=tag)
        # Returns ET.Element (True) if present.
        if isinstance(check, ET.Element):
            return True
        return False


    def _element_check_tree(self, element: Element, tag: str) -> bool:
        """Checks the tag presence"""
        check = self._element_find(element,path=tag)
        # Returns ET.Element (True) if present.
        if isinstance(check, ET.Element):
            return True
        return False


    def parse_element_dict(
            self,
            root_element: str,
            key: str,
            value: str,
            check_tree: Optional[str] = None,
            check_key: Optional[str] = None,
            check_value: Optional[str] = None) -> dict:
        """Parsing elements into dict"""

        if (check_tree and check_key and check_value):
            return {self._element_find(element, key).text:
            {elem.text for elem in self._element_findall(element, value)}
            for element in self._handle_iterfind(root_element)
            if self._element_check_tree(element, check_tree)
            if self._element_find(element, path=check_key).text == check_value}

        if (check_key and check_value):
            return {self._element_find(element, key).text:
            {elem.text for elem in self._element_findall(element, value)}
            for element in self._handle_iterfind(root_element)
            if self._element_find(element, path=check_key).text == check_value}

        if check_tree:
            return {self._element_find(element, key).text:
            {elem.text for elem in self._element_findall(element, value)}
            for element in self._handle_iterfind(root_element)
            if self._element_check_tree(element, check_tree)}

        return {self._element_find(element, key).text:
        {elem.text for elem in self._element_findall(element, value)}
        for element in self._handle_iterfind(root_element)}
