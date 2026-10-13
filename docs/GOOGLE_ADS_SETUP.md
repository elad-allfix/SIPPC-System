# Connecting a Google Ads account (read-only)

AllFix reads Google Ads accounts. It never changes them in this version: the only endpoints it can
call are the OAuth token endpoint, `customers:listAccessibleCustomers` and `googleAds:search` /
`searchStream`. Anything else is refused in code before it leaves the machine
(`backend/allfix/connectivity/transport.py`).

Every Google request, including the sign-in token exchange, goes through the Stage 01 route check:
PIA must report "Connected", at least two outside IP services must see the same IP as PIA, and that
IP must be in the project's required country. If any check fails, nothing is sent.

Checked against Google's documentation on 2026-10-13. Google changes this area often, so if a screen
looks different, follow the
[access levels page](https://developers.google.com/google-ads/api/docs/api-policy/access-levels).

## 1. PIA on the PC

1. In the PIA app, open Settings > Privacy and set **VPN Kill Switch** to **Always**. This is the
   real protection: with it on, Windows blocks all traffic when the tunnel drops. AllFix's own check
   is a second layer.
2. Leave **Split Tunnel** off, or make sure Python is not excluded from the VPN.
3. Connect to the region you want (for example a US Texas server).
4. Test it once. Disconnect PIA, open Stage 01 in AllFix and press **Verify route**. It must say
   "Blocked". Reconnect, press it again, and it must pass.

AllFix finds `piactl` on PATH or in `C:\Program Files\Private Internet Access\`. If it is somewhere
else, set `PIACTL_PATH` in `.env`.

## 2. Google Cloud project (once)

1. Go to [console.cloud.google.com](https://console.cloud.google.com), create a project (for example
   "AllFix"), and enable the **Google Ads API**. That gives the project **Test** access, which only
   works with test accounts.
2. In the Google Ads API **Overview** page in the Cloud console, open **Upgrade access level** and
   **Apply for access** to move to **Explorer**. Explorer can read real accounts, up to 2,880
   operations a day. That is plenty: one AllFix import uses 7.
3. Explorer does **not** include Keyword Planner. That needs **Basic**, which requires brand
   verification of the Cloud project first. AllFix doesn't call Keyword Planner yet.
4. Developer tokens were retired on 2026-09-09. You don't need one. Access comes from the Cloud
   project.

## 3. OAuth client (once)

1. In the Cloud console, go to **Google Auth Platform** (or **APIs & Services > OAuth consent
   screen** on older screens). Set up the consent screen as **External**. Add your own Google account
   as a **test user** while the app is in testing.
2. Under **Clients** (or **Credentials**), create an OAuth client of type **Desktop app**.
3. Put its ID and secret in `.env` on the PC:

   ```
   GOOGLE_OAUTH_CLIENT_ID=...
   GOOGLE_OAUTH_CLIENT_SECRET=...
   ```

   These stay on your PC. Never paste them into a chat.

Note: while the consent screen is in "Testing", Google expires refresh tokens after about 7 days.
Run `ads-login` again when imports start failing with `invalid_grant`, or publish the consent
screen to production.

## 4. Sign in

With PIA connected, run this in the AllFix folder:

```
python -m allfix ads-login --country US
```

1. It runs the route check first and stops if anything fails.
2. It opens your browser. Sign in with the Google account that can see the Ads account and allow
   access. Google only offers one Ads permission, "manage your AdWords campaigns". AllFix itself can
   only read.
3. It writes `ADS_REFRESH_TOKEN` to `.env`. Restart AllFix.

## 5. Use it

In the project, open **Stage 01 · Secure connectivity**:

1. Fill in the required country, the Google Ads customer ID (`123-456-7890`), and the manager (MCC)
   ID if you reach the account through a manager account. Save.
2. Press **Verify route**. It must pass.
3. Press **Import account (read-only)**. This takes the last 90 days: customer settings, campaigns,
   ad groups, keywords, search terms, conversion actions and daily totals.
4. Ask the strategist to review it. It can also run its own read-only queries (`ads_query`). Those go
   through the same route check.

## When something fails

| Message | Meaning |
|---|---|
| `Blocked by Stage 01: ...` | The route check failed. The checklist in Stage 01 says which part. |
| `Google Ads access is not set up` | One of the three `.env` values above is missing. |
| `Google Ads API error 403 ... not enabled / permission` | The signed-in Google user can't see that customer ID, the MCC ID is wrong, or the Cloud project is still at Test access. |
| `invalid_grant` | The refresh token expired or was revoked. Run `ads-login` again. |
