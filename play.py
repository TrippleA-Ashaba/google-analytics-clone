from faker import Faker
from user_agents import parse

fake = Faker()


def parse_user_agent(user_agent):
    ua = parse(user_agent)

    browser = ua.browser.family if ua.browser.family else "Unknown Browser"
    operating_system = ua.os.family if ua.os.family else "Unknown OS"
    device = ua.device.family if ua.device.family else "Unknown Device"

    return browser, operating_system, device


if __name__ == "__main__":
    print(
        parse_user_agent(
            "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_1 like Mac OS X; ig-NG) AppleWebKit/531.47.4 (KHTML, like Gecko) Version/4.0.5 Mobile/8B111 Safari/6531.47.4"
        )
    )
    # print(fake.user_agent())
