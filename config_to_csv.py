#!/usr/bin/env python
import argparse
import os
import csv
import json


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--product', '-p',
                        help='Product Path',
                        required=True)
    parser.add_argument('--output', '-o',
                        help='Output CSV Path',
                        required=True)
    return parser.parse_args()


def config_to_csv(config_dir, output_path):
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
                "Type",
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
                                        filename,
                                        ''
                                    ]
                                )


if __name__ == '__main__':
    config_to_csv(parse_args().product, parse_args().output)
