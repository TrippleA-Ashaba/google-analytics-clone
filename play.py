from user_agents import parse
from faker import Faker

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
            "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_12_8) AppleWebKit/536.0 (KHTML, like Gecko) Chrome/41.0.846.0 Safari/536.0"
        )
    )
    # print(fake.user_agent())
