# DNSRecon: finish the sixth tool (not part of the repo)

Your module needs six tools, and the screenshots you sent cover five. This file lets you add DNSRecon in about ten minutes **without breaking any images**. Do not upload this file to the repo.

## 1. Run it (in Kali)

```bash
dnsrecon -d networkwalks.com
```

Use the default options only. Do **not** add `-t brt` or any brute-force option, because your authorization letter prohibits brute force.

Take a screenshot with the command and the results visible (`clear` first, zoom the terminal). If the output is long, take the screenshot of the part with the name servers, mail server, and TXT or SPF records.

## 2. Frame and save the screenshot

Save your raw screenshot as `dnsrecon-raw.png`, then from the repo root run:

```bash
sudo apt install -y python3-pil
python3 tools/frame_screenshot.py dnsrecon-raw.png screenshots/06-dnsrecon.png "kali@kali: ~  ·  dnsrecon -d networkwalks.com"
```

The result must be named exactly `screenshots/06-dnsrecon.png` (lowercase, no spaces). Do not upload `dnsrecon-raw.png`.

## 3. Paste this into README.md

Find this line in `README.md`:

```
<!-- DNSRECON: paste section 4.6 from dnsrecon-snippet.md here -->
```

Replace it with the block below, and replace every `[...]` with what **your** output actually shows. Delete any bullet your output does not support.

````markdown
### 4.6 DNSRecon

**Goal:** enumerate the domain's DNS records. The `-d` option sets the domain.

```bash
dnsrecon -d networkwalks.com
```

![DNSRecon output for networkwalks.com](screenshots/06-dnsrecon.png)
*Figure 5b. DNS record enumeration.*

**Observations**

- Name servers: [...]
- Mail server: [...]
- SPF / TXT record: [...]
- Service (SRV) records: [...]
- DNS software version disclosed: [...]

**Why it matters:** DNS data maps the mail and name-server setup and shows how hard it may be to spoof email from the domain.
````

## 4. Three small edits elsewhere in README.md

1. **Tools table (section 3):** add this row.
   ```
   | **DNSRecon** | Enumerate DNS records: name servers, mail servers, SPF/TXT, SRV |
   ```
2. **Command log (section 10):** add a row with the time you ran it, for example:
   ```
   | 16:45 | 1 | `dnsrecon -d networkwalks.com` | Figure 5b |
   ```
3. **Repository structure (bottom):** add `06-dnsrecon.png` to the screenshots list.

Optional: if DNSRecon shows something worth flagging (for example a soft-fail SPF record or a disclosed DNS software version), add a row to the risk table in section 6 using the same columns as the others.

## 5. Check before you push

From the repo root:

```bash
bash tools/check-images.sh
```

It must end with "All images found. Safe to push."
