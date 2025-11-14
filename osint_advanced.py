#!/usr/bin/env python3
"""
Advanced OSINT Email Discovery Tool
Additional techniques for discovering emails and online presence
Author: Chris Barker
"""

import requests
import hashlib
import json
from urllib.parse import quote
import argparse
from typing import List, Dict
import re

class AdvancedOSINT:
    def __init__(self, email: str):
        self.email = email
        self.username, self.domain = email.split('@')
        self.results = {
            'email': email,
            'gravatar_profiles': [],
            'clearbit_info': {},
            'email_reputation': {},
            'domain_analysis': {},
            'additional_searches': []
        }

    def check_gravatar(self):
        """Check Gravatar for profile information"""
        print(f"\n[*] Checking Gravatar for {self.email}...")

        # Create MD5 hash of email (Gravatar uses MD5)
        email_hash = hashlib.md5(self.email.lower().encode()).hexdigest()

        # Check if Gravatar profile exists
        gravatar_url = f"https://www.gravatar.com/{email_hash}.json"

        try:
            response = requests.get(gravatar_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"[+] Gravatar profile found!")

                if 'entry' in data:
                    for entry in data['entry']:
                        profile = {
                            'display_name': entry.get('displayName'),
                            'profile_url': entry.get('profileUrl'),
                            'thumbnail': entry.get('thumbnailUrl'),
                            'accounts': []
                        }

                        # Extract social accounts
                        if 'accounts' in entry:
                            for account in entry['accounts']:
                                profile['accounts'].append({
                                    'type': account.get('shortname'),
                                    'url': account.get('url')
                                })
                                print(f"    - {account.get('shortname')}: {account.get('url')}")

                        self.results['gravatar_profiles'].append(profile)
            else:
                print("[-] No Gravatar profile found")

        except Exception as e:
            print(f"[-] Error checking Gravatar: {e}")

    def check_clearbit(self):
        """Check Clearbit for company/person information (free tier)"""
        print(f"\n[*] Checking Clearbit for {self.email}...")

        # Clearbit logo API (free)
        logo_url = f"https://logo.clearbit.com/{self.domain}"
        print(f"[+] Company logo URL: {logo_url}")

        self.results['clearbit_info']['logo_url'] = logo_url

        # Try to get enrichment data (may require API key for full access)
        try:
            enrichment_url = f"https://person.clearbit.com/v2/combined/find?email={self.email}"
            response = requests.get(enrichment_url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                print(f"[+] Clearbit data found!")
                self.results['clearbit_info']['enrichment'] = data
            else:
                print("[-] No Clearbit enrichment data (may require API key)")

        except Exception as e:
            print(f"[-] Clearbit enrichment check failed: {e}")

    def check_email_reputation(self):
        """Check email reputation and validation"""
        print(f"\n[*] Checking email reputation for {self.email}...")

        # EmailRep.io - free email reputation API
        try:
            url = f"https://emailrep.io/{self.email}"
            headers = {
                'User-Agent': 'OSINT-Email-Discovery-Tool',
            }

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                print(f"[+] Email reputation data found!")

                reputation = {
                    'reputation': data.get('reputation'),
                    'suspicious': data.get('suspicious'),
                    'references': data.get('references'),
                    'details': data.get('details', {})
                }

                self.results['email_reputation'] = reputation

                print(f"    - Reputation: {reputation['reputation']}")
                print(f"    - Suspicious: {reputation['suspicious']}")
                print(f"    - References: {reputation['references']}")

                if 'profiles' in data.get('details', {}):
                    print(f"    - Associated profiles: {', '.join(data['details']['profiles'])}")

            else:
                print("[-] No email reputation data found")

        except Exception as e:
            print(f"[-] Error checking email reputation: {e}")

    def analyze_domain(self):
        """Perform domain analysis"""
        print(f"\n[*] Analyzing domain {self.domain}...")

        domain_info = {
            'domain': self.domain,
            'mx_records': [],
            'txt_records': [],
            'spf_record': None,
            'dmarc_record': None
        }

        try:
            import dns.resolver

            # Get MX records
            try:
                mx_records = dns.resolver.resolve(self.domain, 'MX')
                print(f"[+] MX Records found:")
                for mx in mx_records:
                    mx_str = str(mx.exchange)
                    domain_info['mx_records'].append(mx_str)
                    print(f"    - {mx_str}")
            except:
                print("[-] No MX records found")

            # Get TXT records (SPF, DMARC, etc.)
            try:
                txt_records = dns.resolver.resolve(self.domain, 'TXT')
                print(f"[+] TXT Records found:")
                for txt in txt_records:
                    txt_str = str(txt)
                    domain_info['txt_records'].append(txt_str)

                    if 'v=spf1' in txt_str:
                        domain_info['spf_record'] = txt_str
                        print(f"    - SPF: {txt_str[:100]}...")

            except:
                print("[-] No TXT records found")

            # Check DMARC
            try:
                dmarc_records = dns.resolver.resolve(f'_dmarc.{self.domain}', 'TXT')
                for record in dmarc_records:
                    domain_info['dmarc_record'] = str(record)
                    print(f"[+] DMARC: {str(record)[:100]}...")
            except:
                print("[-] No DMARC record found")

            self.results['domain_analysis'] = domain_info

        except ImportError:
            print("[-] dnspython not available for DNS analysis")
        except Exception as e:
            print(f"[-] Error analyzing domain: {e}")

    def check_github(self):
        """Search GitHub for email mentions"""
        print(f"\n[*] Checking GitHub for {self.email}...")

        # GitHub search (no API key required for basic search)
        search_url = f"https://github.com/search?q={quote(self.email)}&type=code"
        print(f"[+] GitHub code search: {search_url}")

        search_url_users = f"https://github.com/search?q={quote(self.email)}&type=users"
        print(f"[+] GitHub users search: {search_url_users}")

        self.results['additional_searches'].append({
            'platform': 'GitHub Code',
            'url': search_url
        })

        self.results['additional_searches'].append({
            'platform': 'GitHub Users',
            'url': search_url_users
        })

    def check_pipl(self):
        """Generate Pipl search URL (requires manual verification)"""
        print(f"\n[*] Generating Pipl search for {self.email}...")

        # Pipl search URL
        pipl_url = f"https://pipl.com/search/?q={quote(self.email)}"
        print(f"[+] Pipl search: {pipl_url}")

        self.results['additional_searches'].append({
            'platform': 'Pipl',
            'url': pipl_url
        })

    def check_paste_sites(self):
        """Check if email appears in paste sites"""
        print(f"\n[*] Checking paste sites for {self.email}...")

        # Psbdmp (Pastebin dump)
        psbdmp_url = f"https://psbdmp.ws/?q={quote(self.email)}"
        print(f"[+] Pastebin dumps: {psbdmp_url}")

        self.results['additional_searches'].append({
            'platform': 'Pastebin Dumps',
            'url': psbdmp_url
        })

    def check_verification_services(self):
        """Generate URLs for email verification services"""
        print(f"\n[*] Email verification service URLs...")

        services = {
            'EmailHippo': f"https://tools.emailhippo.com/email/{quote(self.email)}",
            'Verify Email': f"https://verify-email.org/",
            'Hunter Email Verifier': f"https://hunter.io/email-verifier/{quote(self.email)}"
        }

        for service, url in services.items():
            print(f"[+] {service}: {url}")
            self.results['additional_searches'].append({
                'platform': service,
                'url': url
            })

    def generate_intelligence_queries(self):
        """Generate OSINT platform search queries"""
        print(f"\n[*] Generating intelligence platform queries...")

        queries = {
            'Maltego Transform': f"Email: {self.email}",
            'Shodan': f"hostname:{self.domain}",
            'Censys': f"{self.domain}",
            'SpyOnWeb': f"https://spyonweb.com/{self.domain}",
            'ViewDNS': f"https://viewdns.info/reversewhois/?q={quote(self.email)}",
        }

        for platform, query in queries.items():
            print(f"[+] {platform}: {query}")

    def run_advanced_search(self):
        """Run all advanced OSINT techniques"""
        print("="*70)
        print(f"Advanced OSINT Email Discovery")
        print(f"Target: {self.email}")
        print("="*70)

        self.check_gravatar()
        self.check_clearbit()
        self.check_email_reputation()
        self.analyze_domain()
        self.check_github()
        self.check_pipl()
        self.check_paste_sites()
        self.check_verification_services()
        self.generate_intelligence_queries()

        # Save results
        self.save_report()

    def save_report(self):
        """Save comprehensive report"""
        print("\n" + "="*70)
        print("ADVANCED OSINT REPORT")
        print("="*70)

        report_file = f"osint_advanced_{self.username.replace('.', '_')}.json"

        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)

        print(f"\n[+] Advanced report saved to: {report_file}")
        print("="*70)

        # Print summary
        print(f"\nSummary:")
        print(f"  - Gravatar profiles: {len(self.results['gravatar_profiles'])}")
        print(f"  - Additional search URLs: {len(self.results['additional_searches'])}")
        print(f"  - Domain MX records: {len(self.results['domain_analysis'].get('mx_records', []))}")

def main():
    parser = argparse.ArgumentParser(description='Advanced OSINT Email Discovery')
    parser.add_argument('email', help='Email address to investigate')

    args = parser.parse_args()

    # Validate email
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', args.email):
        print("[!] Invalid email format")
        return

    # Run advanced OSINT
    osint = AdvancedOSINT(args.email)
    osint.run_advanced_search()

if __name__ == "__main__":
    main()
