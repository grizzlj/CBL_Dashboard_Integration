from pylti1p3.tool_config import ToolConfDict
from pylti1p3.message_launch import MessageLaunch
from fastapi import Request
import os

# Dummy Tool Configuration (we'll adjust later)
TOOL_CONFIG = {
    "https://canvas.instructure.com": {
        "client_id": os.getenv("LTI_CLIENT_ID", "your_client_id_here"),
        "auth_login_url": os.getenv("LTI_AUTH_LOGIN_URL", "your_auth_login_url_here"),
        "auth_token_url": os.getenv("LTI_AUTH_TOKEN_URL", "your_auth_token_url_here"),
        "key_set_url": os.getenv("LTI_KEY_SET_URL", "your_key_set_url_here"),
        "private_key_file": "private_key.pem"  # We can adjust this later
    }
}

tool_conf = ToolConfDict(TOOL_CONFIG)

class LTIMessageLaunch:
    @staticmethod
    async def from_request(request: Request):
        body = await request.form()
        launch = MessageLaunch(request, tool_conf)
        return launch.validate_registration() \
                     .validate_launch()
    
    @staticmethod
    def get_user_id(launch):
        return launch.get_launch_data().get("sub", "Unknown")

    @staticmethod
    def get_course_id(launch):
        context = launch.get_launch_data().get("https://purl.imsglobal.org/spec/lti/claim/context", {})
        return context.get("id", "Unknown")
