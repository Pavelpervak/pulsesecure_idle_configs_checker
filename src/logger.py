"""
Logger messages

:::NOTE:::

Misc log events were recorded as part of the methods itself.

"""
import logging

# Console Logging handler.
logging.getLogger(__name__).addHandler(logging.StreamHandler())
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

LOGGER = {

    'auth_servers': {
        'success': "SUCCESS: Authentication servers data found.",
        'fail': "ERROR: Authentication server data not found. Results would be inaccurate!"
    },

    'signin_urls': {
        'success': "SUCCESS: SignIn URL data found.",
        'fail': "ERROR: SignIn URL data not found. Results would be inaccurate!"
    },

    'user_realms': {
        'success': "SUCCESS: User realms data found.",
        'fail': "ERROR: User realms data not found. Results would be inaccurate!"
    },

    'admin_realms': {
        'success': "SUCCESS: Admin realms data found.",
        'fail': "ERROR: Admin realms data not found. Results would be inaccurate!"
    },

    'user_roles': {
        'success': "SUCCESS: User roles data found.",
        'fail': "ERROR: User roles data not found. Results would be inaccurate!"
    },

    'admin_roles': {
        'success': "SUCCESS: Admin roles data found.",
        'fail': "ERROR: Admin roles data not found. Results would be inaccurate!"
    },

    'web_policies': {
        'success': "SUCCESS: Web policies data found.",
        'fail': "ERROR: Web policies data not found."
    },

    'file_policies': {
        'success': "SUCCESS: File policies data found.",
        'fail': "ERROR: File policies data not found."
    },

    'sam_policies': {
        'success': "SUCCESS: SAM policies data found.",
        'fail': "ERROR: SAM policies data not found."
    },

    'termserv_policies': {
        'success': "SUCCESS: TermServ policies data found.",
        'fail': "ERROR: TermServ policies data not found."
    },

    'html5_policies': {
        'success': "SUCCESS: HTML5 policies data found.",
        'fail': "ERROR: HTML5 policies data not found."
    },

    'vpntunnel_policies': {
        'success': "SUCCESS: VPN Tunnel policies data found.",
        'fail': "ERROR: VPN Tunnel policies data not found."
    },

    'web_profiles': {
        'success': "SUCCESS: Web profiles data found.",
        'fail': "ERROR: Web profiles data not found."
    },

    'file_profiles': {
        'success': "SUCCESS: File profiles data found.",
        'fail': "ERROR: File profiles data not found."
    },

    'sam_profiles': {
        'success': "SUCCESS: SAM profiles data found.",
        'fail': "ERROR: SAM profiles data not found."
    },

    'termserv_profiles': {
        'success': "SUCCESS: TermServ profiles data found.",
        'fail': "ERROR: TermServ profiles data not found."
    },
	
    'vdi_profiles': {
        'success': "SUCCESS: VDI profiles data found.",
        'fail': "ERROR: VDI profiles data not found."
    },

    'html5_profiles': {
        'success': "SUCCESS: HTML5 profiles data found.",
        'fail': "ERROR: HTML5 profiles data not found."
    }
}
