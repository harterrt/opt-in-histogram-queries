import csv
import json
import re

def get_optin_hists():
    """Get names of all opt-in histograms

    Histograms.json can be found here:
    https://hg.mozilla.org/releases/mozilla-release/raw-file/tip/toolkit/components/telemetry/Histograms.json
    """
    with open('Histograms.json', 'r') as infile:
        histograms = json.loads(infile.read())

    optin = filter(lambda h: "releaseChannelCollection" not in h[1].keys(),
                   histograms.items())

    return map(lambda o: o[0], optin)

def get_queries():
    """Get all longitudinal queries in re:dash

    Longitudinal_Queries_2016_11_16.csv can be found here:
    https://sql.telemetry.mozilla.org/api/queries/1693/results/600787.csv
    """
    with open("Longitudinal_Queries_2016_11_16.csv", 'r') as infile:
        query_csv = csv.reader(infile)
        headers = query_csv.next()
        rows = [row for row in query_csv]

    return [dict(zip(headers, row)) for row in rows]

def contains_optin(query, optins):
    return any([optin.lower() in query.decode('utf8').lower() for optin in optins])

def format_query(query):
    return (
        query['name'],
        "https://sql.telemetry.mozilla.org/queries/{0}/source".format(query['id'])
    )

def main():
    optin = get_optin_hists()
    queries = get_queries()

    hits = filter(lambda q: contains_optin(q["query"], optin), queries)

    out = map(format_query, hits)

    with open("opt_in_hist_queries.csv", 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(out)

    print set(map(lambda x: x[0], out))
