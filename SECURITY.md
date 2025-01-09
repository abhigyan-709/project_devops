# Security Policy

## Supported Versions

Use this section to tell people about which versions of your project are currently being supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 5.1.x   | :white_check_mark: |
| 5.0.x   | :x:                |
| 4.0.x   | :white_check_mark: |
| < 4.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it as soon as possible. We take security very seriously and aim to address vulnerabilities quickly.

### Steps to Report:
1. **Email**: Send an email to `abhigyan709@gmail.com` with the details of the vulnerability.
2. **Provide Information**: Include as much detail as possible, including:
   - Steps to reproduce the issue
   - Potential impact of the vulnerability
   - Any other relevant details (e.g., affected versions, configurations, etc.)
3. **Confidentiality**: Please refrain from publicly disclosing the vulnerability until it has been addressed.

### What to Expect:
- **Acknowledgement**: We will acknowledge receipt of your report within 48 hours.
- **Assessment**: Our security team will assess the issue and determine its severity.
- **Updates**: You will receive updates on the status of the vulnerability fix.
- **Resolution**: Once a fix is available, we will provide a patch or mitigation steps.
- **Public Disclosure**: If the vulnerability is confirmed, we will publicly disclose it once it is resolved, along with a summary of the fix.

### Security Process:
- **Severity Levels**: We classify vulnerabilities based on their severity (Critical, High, Medium, Low).
- **Patch Timeline**: Critical and High severity issues will be addressed as quickly as possible, usually within 1-2 weeks.
- **Deprecation**: Older versions that no longer receive security updates will be deprecated and marked as unsupported.

## Security Best Practices

- **Authentication**: Ensure that your application uses strong authentication methods (e.g., OAuth, JWT).
- **Encryption**: Use encryption for sensitive data both in transit (e.g., TLS/SSL) and at rest (e.g., AES-256).
- **Access Control**: Implement role-based access control (RBAC) and the principle of least privilege for all users and services.
- **Regular Updates**: Keep dependencies and system packages up to date with the latest security patches.
- **Monitoring**: Enable logging and monitoring to detect and respond to security incidents in real time.

## Known Vulnerabilities

If there are any known vulnerabilities in the current or past versions of the project, list them here along with their status (e.g., fixed, under investigation).

| Version | Vulnerability | Status          |
| ------- | ------------- | --------------- |
| 5.1.x   | CVE-2024-1234 | Fixed in 5.1.1   |
| 4.0.x   | CVE-2023-5678 | Under Investigation |
