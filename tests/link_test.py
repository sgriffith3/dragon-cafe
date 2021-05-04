#!/usr/bin/env python3

import argparse
from bs4 import BeautifulSoup
import requests


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Link Scraping Utility")
    parser.add_argument('-s', '--site', default='http://127.0.0.1:2225', help="The site you wish to test links for")
    return parser.parse_args()


def test_scrape(site: str) -> list:
    r = requests.get(site)
    soup = BeautifulSoup(r.text, features="html.parser")
    results = []
    for link in set(soup.find_all('iframe')):
        spread = str(link).split(' ')
        for attr in spread:
            if "src=" in attr:
                href = attr.split('"')[1]
                if "http" in href:
                    r2 = requests.get(href)
                else:
                    r2 = requests.get(f"{site}{href}")
                print(f"GET {r2.status_code} {href}")

                if 200 <= r2.status_code < 400:
                    status = True
                else:
                    status = False
                results.append({"link": href, "response": r2.status_code, "pass": status})
                soup2 = BeautifulSoup(r2.text, features="html.parser")
                results2 = []
                for inner_link in set(soup2.find_all(['a', 'form'])):
                    sep = str(inner_link).split(' ')
                    for att in sep:
                        if "href" in att or "action" in att:
                            hr = att.split('"')[1]
                            if "http" in hr:
                                r3 = requests.get(hr)
                            else:
                                r3 = requests.get(f"{site}{hr}")
                            status_code = r3.status_code
                            req_type = "GET"
                            if 200 <= status_code < 400:
                                status = True
                            elif status_code == 405:
                                req_type = "POST"
                                r4 = requests.post(f"{site}{hr}", data={'name': 'awesome_tester_dude'})
                                if 200 <= r4.status_code <= 400:
                                    status = True
                                    status_code = r4.status_code
                                else:
                                    status = False
                            else:
                                status = False
                            print(f"   {req_type} {status_code} {hr}")
                            results.append({"link": hr, "response": status_code, "pass": status})
    return results


def grading(results: list) -> str:
    success = True
    for result in results:
        if not result['pass']:
            success = False
    if success:
        txt = """
        \nCongratulations!

        All of your links have passed the test!"""
    else:
        txt = f"""

        Uh-oh

        At least one of your links has failed.

        Please check the following output to see which failed:

        {results}"""
    return txt


def main():
    args = get_args()
    test_result = grading(test_scrape(args.site))
    print(test_result)


if __name__ == "__main__":
    main()