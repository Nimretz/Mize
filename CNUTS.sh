#!/bin/bash

#query for a record (if not present, www. subdomain) ns records and whois containing keywords.
while read -r line; do
    echo "$line, "
    a_record=$(dig +short a "$line")
    if [[ -z "$a_record" ]]; then
        echo "No A record found for $line, trying www.$line"
        a_record=$(dig +short a "www.$line")
    fi
    if [[ -n "$a_record" ]]; then
        echo "A record found: $a_record"
    else
        echo "No A record found for $line or www.$line"
    fi
    ns_record=$(dig +short ns "$line")
    if [[ -n "$ns_record" ]]; then
        echo "NS record found: $ns_record"
    else
        echo "No NS record found for $line"
    fi
    #edit word1|word2|word4|gandi|word3 or change in the future for user input
    whois_output=$(whois -H "$line" | grep -Ei 'word1|word2|word4|gandi|word3')
    if [[ -n "$whois_output" ]]; then
        echo "Whois output found:"
        echo "$whois_output"
    else
        echo "No whois output found for $line"
    fi
done < everydomainsofar
