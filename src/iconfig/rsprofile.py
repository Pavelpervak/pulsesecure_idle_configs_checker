"""
Resource profiles parser
"""
from ..api import ICSXMLParser, logger, LOGGER
from ..xpath.rsprofile import *

class ICSRSProfile(ICSXMLParser):
    """Base class for RS Profile parsing"""

    def __init__(self, xml_file) -> None:
        self.web_profiles_ = []
        self.file_profiles_ = []
        self.sam_profiles_capp_ = []
        self.sam_profiles_dest_ = []
        self.termsrv_profiles_ = []
        self.vdi_profiles_ = []
        self.html5_profiles_ = []
        self.log_object = ''
        super().__init__(xml_file)
    
    def rs_profiles(self):
        """Pipeline method to run all methods"""
        self.web_profiles()
        self.file_profiles()
        self.sam_profiles()
        self.termserv_profiles()
        self.vdi_profiles()
        self.html5_profiles()

    def idle_resource_profiles(
        self,
        rsprofile_root: str,
        rsprofile_path: str):
        """Parsing resource profiles"""
        if self.check_tree(rsprofile_root):
            logger.info(LOGGER[self.log_object]['success'])
            return [self._element_find_value(profile, "name")
                for profile in self._handle_iterfind(rsprofile_path)
                if self._element_find(profile, "roles").text is None]

        logger.warning(LOGGER[self.log_object]['fail'])
        return []

    def web_profiles(self):
        """Web resource profiles"""
        self.log_object = self.web_profiles.__name__
        self.web_profiles_ = self.idle_resource_profiles(WEB_PROF_ROOT, WEB_PROF)

    def file_profiles(self):
        """Files resource profiles"""
        self.log_object = self.file_profiles.__name__
        self.file_profiles_ = self.idle_resource_profiles(FILE_PROF_ROOT, FILE_PROF)

    def sam_profiles(self):
        """SAM resource profiles"""
        self.log_object = self.sam_profiles.__name__
        self.sam_profiles_capp_ = self.idle_resource_profiles(SAM_PROF_ROOT, SAM_PROF_CAPP)
        self.sam_profiles_dest_ = self.idle_resource_profiles(SAM_PROF_ROOT, SAM_PROF_DEST)

    def termserv_profiles(self):
        """TermSrv profiles"""
        self.log_object = self.termserv_profiles.__name__
        self.termsrv_profiles_ = self.idle_resource_profiles(TERMSERV_PROF_ROOT, TERMSERV_PROF)

    def html5_profiles(self):
        """HTML5 profiles"""
        self.log_object = self.html5_profiles.__name__
        self.html5_profiles_ = self.idle_resource_profiles(HTML5_PROF_ROOT, HTML5_PROF)

    def vdi_profiles(self):
        """VDI profiles"""
        self.log_object = self.vdi_profiles.__name__
        self.vdi_profiles_ = self.idle_resource_profiles(VDI_PROF_ROOT, VDI_PROF)
