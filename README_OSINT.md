# OSINT Email Discovery Tool

A comprehensive OSINT (Open Source Intelligence) tool for discovering emails and online profiles linked to a primary email address.

## Features

- **Data Breach Checking**: Queries HaveIBeenPwned API to check if the email has been compromised
- **Email Pattern Generation**: Creates common email variations based on name parsing
- **Domain Email Discovery**: Uses Hunter.io API to find other emails on the same domain (optional)
- **Social Media Profile Discovery**: Generates potential social media profile URLs
- **Google Dorking**: Provides Google search queries for manual investigation
- **DNS Record Analysis**: Checks DNS TXT records for verification emails
- **Comprehensive Reporting**: Generates detailed JSON reports of findings

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage (No API Key)
```bash
python3 osint_email_discovery.py chris.barker@futureforesight.com
```

### With Hunter.io API Key
```bash
python3 osint_email_discovery.py chris.barker@futureforesight.com --hunter-api-key YOUR_API_KEY
```

## OSINT Techniques Employed

1. **HaveIBeenPwned Integration**
   - Checks against 600+ data breaches
   - Shows breach dates and exposed data types
   - No API key required (rate limited)

2. **Email Pattern Analysis**
   - Generates variations: firstname.lastname, f.lastname, firstnamelastname
   - Tests across common email providers (Gmail, Outlook, Yahoo)
   - Based on common corporate email patterns

3. **Domain Intelligence**
   - DNS TXT record analysis
   - Domain-based email enumeration
   - WHOIS information (when available)

4. **Social Media Footprint**
   - LinkedIn, Twitter/X, GitHub profiles
   - Medium, Dev.to, Reddit accounts
   - Based on username and name patterns

5. **Google Dorking**
   - Automated generation of search queries
   - Site-specific searches
   - Email enumeration queries

## Output

The tool generates:
- Console output with real-time discoveries
- JSON report file: `osint_report_<username>_<timestamp>.json`

## API Keys (Optional)

### Hunter.io
- Free tier: 25 searches/month
- Sign up at: https://hunter.io/
- Provides verified email addresses from public sources

## Ethical Use

This tool is designed for:
- Personal security audits
- Investigating your own online presence
- Authorized security assessments
- Educational purposes

**Do not use this tool for:**
- Harassment or stalking
- Unauthorized access attempts
- Spamming or phishing
- Any illegal activities

## Legal Notice

Always ensure you have permission to investigate the target email address. Use responsibly and in compliance with applicable laws and regulations.

## Example Output

```
======================================================================
OSINT Email Discovery Tool
Target: chris.barker@futureforesight.com
======================================================================

[*] Checking HaveIBeenPwned for breaches...
[+] Found 2 breaches!
    - LinkedIn (2012-05-05)
    - Adobe (2013-10-04)

[*] Generating email pattern variations...
[+] Generated 24 potential email variations
    - chris.barker@gmail.com
    - c.barker@futureforesight.com
    - chrisbarker@gmail.com
    ...

[*] Searching for social media profiles...
    - LinkedIn: https://www.linkedin.com/search/results/people/?keywords=chris+barker
    - GitHub: https://github.com/chris.barker
    ...

[+] Full report saved to: osint_report_chris.barker_20250114_120000.json
```

## Dependencies

- **requests**: HTTP library for API calls
- **dnspython**: DNS toolkit for record queries

## Author

Chris Barker (chris.barker@futureforesight.com)

## License

Use responsibly for authorized purposes only.
