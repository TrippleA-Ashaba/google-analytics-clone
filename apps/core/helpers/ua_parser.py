from user_agents import parse


def parse_user_agent(user_agent):
    ua = parse(user_agent)

    browser = ua.browser.family if ua.browser.family else "Unknown Browser"
    operating_system = ua.os.family if ua.os.family else "Unknown OS"
    device = ua.device.family if ua.device.family else "Unknown Device"

    return browser, operating_system, device
