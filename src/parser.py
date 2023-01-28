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

    def findall(self, path: str) -> Generator:
        """XML Findall wrapper"""
        for elem in self.root.findall(path=path, namespaces=self.nsmap):
            yield elem

    def _find_root_override(self, root: Element, path: str) -> Generator:
        """XML Find wrapper"""
        return root.find(path=path, namespaces=self.nsmap)

    def find_element(self, path: str) -> Element:
        """XML Find wrapper that uses the default root"""
        return self.root.find(path=path, namespaces=self.nsmap)

    def iterfind(self, path: str) -> Generator:
        """XML IterFind wrapper - passes namespace automatically for tags"""
        for elem in self.root.iterfind(path=path, namespaces=self.nsmap):
            yield elem

    def iter(self, path: str) -> Generator:
        """XML Iter wrapper - passes namespace automatically for tags"""
        for elem in self.root.iter(tag=path):
            yield elem

    def parse_element(
            self,
            path: str,
            allow_dups: bool = False,
            invalid_values: Optional[list] = None) -> Union[list, set]:
        """Returns the TEXT of the element"""

        invalid_values = ICSXMLParser.default_invalid_values if invalid_values is None else ICSXMLParser.default_invalid_values + invalid_values
        if allow_dups:  # List will be created to allow duplicates.
            return [elem.text for elem in self.root.findall(path=path, namespaces=self.nsmap)
                    if elem.text not in invalid_values]
        # Else SET will be created to disallow duplicates.
        return {elem.text for elem in self.root.findall(path=path, namespaces=self.nsmap)
                if elem.text not in invalid_values}

    def check_tree(self, tag: str) -> bool:
        """Checks the tag presence"""
        check = self.root.find(path=tag, namespaces=self.nsmap)
        # Returns ET.Element (True) if present.
        if isinstance(check, ET.Element):
            return True
        return False

    def parse_element_dict(
            self,
            root_element: str,
            child_element: str) -> dict:
        """Parsing elements into dict"""
        results_dict = {}
        for element in self.findall(path=root_element):
            element: Element
            results_dict[child_element] = [
                child.text for child in element.find(path=child_element)]
        return results_dict
