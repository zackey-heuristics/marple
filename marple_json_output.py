"""
This module is used to output the results of the Marple analysis in JSON format.

Usage:
    python marple_json_output.py [name] [-o OUTPUT_FILE]

Example:
    python marple_json_output.py soxoj
    python marple_json_output.py soxoj -o result.json
"""
import argparse
import asyncio
import json
import os
import pathlib
import sys

from marple import *


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Output the results of the Marple analysis in JSON format."
    )
    parser.add_argument(
        'name',
        help='Target username or first/lastname to search by.',
    )
    parser.add_argument(
        '--username',
        help='Target username',
    )
    parser.add_argument(
        '--firstname',
        help='Target firstname, e.g. Jon',
    )
    parser.add_argument(
        '--lastname',
        help='Target lastname/surname, e.g. Snow',
    )
    parser.add_argument(
        '--middlename',
        help='Target middlename/patronymic/avonymic/matronymic, e.g. Snow',
    )
    parser.add_argument(
        '--birthdate',
        help='Target date of birth an any format, e.g. 02/17/2009',
    )
    parser.add_argument(
        '--country',
        help='Target country any format, e.g. UK',
    )
    parser.add_argument(
        '-t',
        '--threshold',
        action='store',
        type=int,
        default=300,
        help='Threshold to discard junk search results',
    )
    parser.add_argument(
        '--results-count',
        action='store',
        type=int,
        default=1000,
        help='Count of results parsed from each search engine',
    )
    parser.add_argument(
        '--no-url-filter',
        action='store_false',
        dest='url_filter',
        default=True,
        help='Disable filtering results by usernames in URLs',
    )
    parser.add_argument(
        '--engines',
        dest='engines',
        nargs='+',
        choices=get_engines_names(),
        help='Engines to run (you can choose more than one)',
    )

    # parser.add_argument(
    #     '--plugins',
    #     dest='plugins',
    #     nargs='+',
    #     default='',
    #     choices={'maigret', 'socid_extractor', 'metadata'},
    #     help='Additional plugins to analyze links',
    # )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        default=False,
        help='Display junk score for each result',
    )
    parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        default=False,
        help='Display all the results from sources and debug messages',
    )
    # parser.add_argument(
    #     '-l',
    #     '--list',
    #     action='store_true',
    #     default=False,
    #     help='Display only list of all the URLs',
    # )
    parser.add_argument(
        '--proxy',
        type=str,
        default="",
        help="Proxy string (e.g. https://user:pass@1.2.3.4:8080)",
    )
    parser.add_argument(
        '--csv',
        type=str,
        default="",
        help="Save results to the CSV file",
    )
    parser.add_argument(
        "-o", "--output", 
        help="The output file to save the results."
    )
    args = parser.parse_args()
    
    username = args.name
    output = args.output
    
    # result json
    result_dict = {
        "username": username,
        "results": [],
        "pdf_results": [],
        "status": None,
    }

    
    # If the username is not provided, try to construct it from the first and last names 
    if " " in username:
        print("Warning: search by firstname+lastname is not fully supported at the moment!", file=sys.stderr)
    
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    result = loop.run_until_complete(
        marple(
            username,
            args.results_count,
            args.url_filter,
            is_debug=args.debug,
            proxy=args.proxy,
            custom_engines=args.engines
        )
    )
    
    total_collected_count = len(result.all_links)
    unique_count = len(result.unique_links)
    
    displayed_count = 0
    
    def is_likely_profile(r):
        return r.is_it_likely_username_profile() and r.junk_score <= args.threshold and not r.filtered

    # reliable links section
    for r in result.unique_links:
        if is_likely_profile(r):
            displayed_count += 1
            
            result_dict["results"].append({
                "source": r.source,
                "url": r.url,
                "title": r.title,
                "junk_score": r.junk_score,
            })

    pdf_count = 0
    
    def is_pdf_file(url):
        return url.endswith('pdf') or '-pdf.' in url

    # pdf files section
    for r in result.unique_links:
        if is_pdf_file(r.url):
            pdf_count += 1
            
            result_dict["pdf_results"].append({
                "source": r.source,
                "url": r.url,
                "title": r.title,
                "junk_score": r.junk_score,
            })
    
    result_dict["status"] = {
        "total_collected_count": total_collected_count,
        "unique_count": unique_count,
        "displayed_count": displayed_count,
        "pdf_count": pdf_count,
    }

    # print the results for json output
    if output:
        with open(output, "w") as f:
            json.dump(result_dict, f, indent=4, ensure_ascii=False)
        print(f"{pathlib.Path(output).resolve()}")
    else:
        print(json.dumps(result_dict, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    main()

