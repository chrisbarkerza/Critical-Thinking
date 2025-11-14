#!/usr/bin/env python3
"""
OSINT Email Discovery Tool
Discovers emails linked to a primary email address using various OSINT techniques
Author: Chris Barker
"""

import requests
import json
import re
import time
from urllib.parse import quote
from typing import List, Dict, Set
import argparse
from datetime import datetime

class OSINTEmailDiscovery:
    def __init__(self, primary_email: str):
        self.primary_email = primary_email
        self.discovered_emails = set()
        self.results = {
            'primary_email': primary_email,
            'timestamp': datetime.now().isoformat(),
            'discovered_emails': [],
            'breach_info': [],
            'social_profiles': [],
            'domain_emails': [],
            'patterns': []
        }

        # Extract domain and username
        self.username, self.domain = primary_email.split('@')
        self.first_name, self.last_name = self._parse_name(self.username)

    def _parse_name(self, username: str) -> tuple:
        """Parse first and last name from email username"""
        # Handle common patterns: firstname.lastname, firstnamelastname, etc.
        if '.' in username:
            parts = username.split('.')
            return parts[0], parts[-1] if len(parts) > 1 else ''
        elif '_' in username:
            parts = username.split('_')
            return parts[0], parts[-1] if len(parts) > 1 else ''
        else:
            # Try to split camelCase
            return username, ''

    def check_haveibeenpwned(self):
        """Check HaveIBeenPwned for data breaches"""
        print(f"\n[*] Checking HaveIBeenPwned for breaches...")

        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{quote(self.primary_email)}"
        headers = {
            'User-Agent': 'OSINT-Email-Discovery-Tool',
            'api-version': '3'
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                breaches = response.json()
                print(f"[+] Found {len(breaches)} breaches!")
                for breach in breaches:
                    breach_info = {
                        'name': breach.get('Name'),
                        'domain': breach.get('Domain'),
                        'breach_date': breach.get('BreachDate'),
                        'data_classes': breach.get('DataClasses', [])
                    }
                    self.results['breach_info'].append(breach_info)
                    print(f"    - {breach['Name']} ({breach.get('BreachDate')})")
            elif response.status_code == 404:
                print("[+] No breaches found (good news!)")
            elif response.status_code == 429:
                print("[-] Rate limited by HaveIBeenPwned API")
            else:
                print(f"[-] Error: HTTP {response.status_code}")
        except Exception as e:
            print(f"[-] Error checking HaveIBeenPwned: {e}")

    def generate_email_patterns(self) -> List[str]:
        """Generate common email pattern variations"""
        print(f"\n[*] Generating email pattern variations...")

        patterns = []
        first = self.first_name.lower()
        last = self.last_name.lower()

        if first and last:
            # Common patterns
            patterns.extend([
                f"{first}.{last}@{self.domain}",
                f"{first}_{last}@{self.domain}",
                f"{first}{last}@{self.domain}",
                f"{first[0]}{last}@{self.domain}",
                f"{first}.{last[0]}@{self.domain}",
                f"{last}.{first}@{self.domain}",
                f"{first}@{self.domain}",
                f"{last}@{self.domain}",
            ])

            # Try with different domains
            common_domains = ['gmail.com', 'outlook.com', 'yahoo.com', 'hotmail.com', 'protonmail.com']
            for domain in common_domains:
                patterns.extend([
                    f"{first}.{last}@{domain}",
                    f"{first}{last}@{domain}",
                    f"{first[0]}{last}@{domain}",
                ])

        # Remove duplicates and the primary email
        patterns = list(set(patterns))
        if self.primary_email in patterns:
            patterns.remove(self.primary_email)

        self.results['patterns'] = patterns[:20]  # Limit to top 20
        print(f"[+] Generated {len(patterns)} potential email variations")
        for pattern in patterns[:10]:
            print(f"    - {pattern}")

        return patterns

    def check_hunter_io(self, api_key: str = None):
        """Check Hunter.io for domain emails (requires API key)"""
        if not api_key:
            print("\n[*] Skipping Hunter.io (no API key provided)")
            return

        print(f"\n[*] Checking Hunter.io for {self.domain}...")

        url = f"https://api.hunter.io/v2/domain-search"
        params = {
            'domain': self.domain,
            'api_key': api_key
        }

        try:
            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                emails = data.get('data', {}).get('emails', [])
                print(f"[+] Found {len(emails)} emails on domain {self.domain}")

                for email_data in emails:
                    email = email_data.get('value')
                    if email and email != self.primary_email:
                        self.discovered_emails.add(email)
                        self.results['domain_emails'].append({
                            'email': email,
                            'type': email_data.get('type'),
                            'confidence': email_data.get('confidence')
                        })
                        print(f"    - {email}")
            else:
                print(f"[-] Hunter.io error: HTTP {response.status_code}")
        except Exception as e:
            print(f"[-] Error with Hunter.io: {e}")

    def search_social_profiles(self):
        """Search for social media profiles"""
        print(f"\n[*] Searching for social media profiles...")

        # Common social media platforms
        platforms = {
            'LinkedIn': f"https://www.linkedin.com/search/results/people/?keywords={self.first_name}+{self.last_name}",
            'Twitter/X': f"https://twitter.com/{self.username}",
            'GitHub': f"https://github.com/{self.username}",
            'Medium': f"https://medium.com/@{self.primary_email}",
            'Dev.to': f"https://dev.to/{self.username}",
            'Reddit': f"https://www.reddit.com/user/{self.username}",
        }

        for platform, url in platforms.items():
            self.results['social_profiles'].append({
                'platform': platform,
                'potential_url': url
            })
            print(f"    - {platform}: {url}")

    def google_dork_search(self):
        """Generate Google dork queries for email discovery"""
        print(f"\n[*] Generating Google dork queries...")

        dorks = [
            f'"{self.primary_email}"',
            f'"{self.first_name} {self.last_name}" email',
            f'site:{self.domain} "{self.first_name} {self.last_name}"',
            f'intext:"{self.primary_email}"',
            f'"{self.first_name}.{self.last_name}@" OR "{self.first_name}@"',
        ]

        print("[+] Google dork queries to try manually:")
        for dork in dorks:
            print(f"    - {dork}")
            print(f"      https://www.google.com/search?q={quote(dork)}")

        self.results['google_dorks'] = dorks

    def check_domain_info(self):
        """Check domain WHOIS and DNS information"""
        print(f"\n[*] Checking domain information for {self.domain}...")

        try:
            # Try to get DNS TXT records (sometimes contain verification emails)
            import dns.resolver

            try:
                txt_records = dns.resolver.resolve(self.domain, 'TXT')
                print(f"[+] Found TXT records for {self.domain}")
                for record in txt_records:
                    txt = str(record)
                    # Look for emails in TXT records
                    emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', txt)
                    for email in emails:
                        if email not in self.discovered_emails:
                            self.discovered_emails.add(email)
                            print(f"    - Found in DNS: {email}")
            except:
                print("[-] Could not retrieve DNS records")
        except ImportError:
            print("[-] dnspython not installed, skipping DNS checks")

    def run_comprehensive_search(self, hunter_api_key: str = None):
        """Run all OSINT techniques"""
        print("="*70)
        print(f"OSINT Email Discovery Tool")
        print(f"Target: {self.primary_email}")
        print("="*70)

        # Run all checks
        self.check_haveibeenpwned()
        time.sleep(2)  # Be respectful with rate limits

        self.generate_email_patterns()
        self.search_social_profiles()
        self.google_dork_search()

        if hunter_api_key:
            self.check_hunter_io(hunter_api_key)

        # Compile all discovered emails
        all_emails = list(self.discovered_emails)
        self.results['discovered_emails'] = all_emails

        # Generate report
        self.generate_report()

    def generate_report(self):
        """Generate comprehensive report"""
        print("\n" + "="*70)
        print("OSINT DISCOVERY REPORT")
        print("="*70)

        print(f"\nPrimary Email: {self.primary_email}")
        print(f"Name Parsed: {self.first_name.title()} {self.last_name.title()}")
        print(f"Domain: {self.domain}")

        print(f"\n[BREACH INFORMATION]")
        if self.results['breach_info']:
            print(f"Found in {len(self.results['breach_info'])} data breaches:")
            for breach in self.results['breach_info']:
                print(f"  - {breach['name']} ({breach['breach_date']})")
                print(f"    Data exposed: {', '.join(breach['data_classes'][:5])}")
        else:
            print("No breaches found")

        print(f"\n[DISCOVERED EMAILS]")
        if self.results['domain_emails']:
            print(f"Found {len(self.results['domain_emails'])} emails on domain:")
            for email_data in self.results['domain_emails']:
                print(f"  - {email_data['email']} (confidence: {email_data.get('confidence', 'N/A')})")
        else:
            print("No additional emails discovered via API")

        print(f"\n[EMAIL PATTERNS]")
        print(f"Generated {len(self.results['patterns'])} potential variations:")
        for pattern in self.results['patterns'][:10]:
            print(f"  - {pattern}")

        print(f"\n[SOCIAL MEDIA PROFILES]")
        for profile in self.results['social_profiles']:
            print(f"  - {profile['platform']}: {profile['potential_url']}")

        # Save to JSON
        report_file = f"osint_report_{self.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)

        print(f"\n[+] Full report saved to: {report_file}")
        print("="*70)

def main():
    parser = argparse.ArgumentParser(description='OSINT Email Discovery Tool')
    parser.add_argument('email', help='Primary email address to investigate')
    parser.add_argument('--hunter-api-key', help='Hunter.io API key (optional)', default=None)

    args = parser.parse_args()

    # Validate email format
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', args.email):
        print("[!] Invalid email format")
        return

    # Run OSINT discovery
    osint = OSINTEmailDiscovery(args.email)
    osint.run_comprehensive_search(hunter_api_key=args.hunter_api_key)

if __name__ == "__main__":
    main()
