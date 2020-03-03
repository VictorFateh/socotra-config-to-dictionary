#!/usr/bin/env python
import argparse
import os
import csv
import json
import requests
import urllib3
urllib3.disable_warnings()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o',
                        help='Output CSV Path',
                        required=True)
    # Local product
    parser.add_argument('-l',
                        help='Flag to use local config instead of live instance',
                        default=False,
                        action='store_true')
    parser.add_argument('--product', '-r',
                        help='Product Path')

    # Online product
    parser.add_argument('--instance', '-i',
                        help='Hostname URL (ex. username-configeditor.co.sandbox.socotra.com)')
    parser.add_argument('--username', '-u',
                        help='Tenant username',
                        default='alice.lee')
    parser.add_argument('--password', '-p',
                        help='Tenant password',
                        default='socotra')
    parser.add_argument('--environment', '-e',
                        help='Environment',
                        default='api.sandbox')

    return parser.parse_args()


def local_config_to_csv(config_dir, output_path):
    product_name = config_dir.rsplit('/', 1)[-1]
    with open("{}/{}.csv".format(output_path, product_name), "a") as outfile:
        f = csv.writer(outfile)
        f.writerow(
            [
                "Details",
                "DEP - PASubmissionDTO Attribute",
                "Comments",
                "Field Name - Socotra Policy",
                "Field Title",
                "Field Type",
                "Required",
                "Socotra Config File Level",
                "Used for Rating (Inputs from DEP)"
            ]
        )
        for subdir, dirs, files in os.walk(r'{}/policy'.format(config_dir)):
            for filename in files:
                filepath = subdir + os.sep + filename
                if filepath.endswith(".json"):
                    with open(filepath) as infile:
                        json_file = json.loads(infile.read())
                        if 'name' in json_file:
                            f.writerow(
                                [
                                    '',
                                    '',
                                    '',
                                    json_file['name'],
                                    json_file['displayName'],
                                    'n/a',
                                    'n/a',
                                    filename,
                                    ''
                                ]
                            )
                        if 'fields' in json_file:
                            for field in json_file['fields']:
                                f.writerow(
                                    [
                                        '',
                                        '',
                                        '',
                                        field['name'],
                                        field['title'],
                                        field['type'],
                                        not field['optional'],
                                        filename,
                                        ''
                                    ]
                                )
    print("Local product generated")


def get_auth_token(hostname, username, password, env):
    post_data = {"username": username, "password": password, "hostName": hostname}
    try:
        r = requests.post('https://{}.socotra.com/account/authenticate'.format(env), json=post_data, verify=False)
        json_resp = r.json()
        return json_resp["authorizationToken"]
    except requests.exceptions.RequestException as e:
        print(e)


def tenant_config_to_csv(hostname, username, password, output_path, environment):
    token = get_auth_token(hostname, username, password, environment)

    # Use products API to programmatically loop through tenants product info
    # https://docs.socotra.com/production/api/product.html

    print("Online product generated")


if __name__ == '__main__':
    args = parse_args()
    if args.l:
        local_config_to_csv(args.product, args.output)
    else:
        tenant_config_to_csv(args.instance, args.username, args.password, args.output, args.environment)
