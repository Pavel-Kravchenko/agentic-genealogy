# Sources and databases

Every observation is dated: sites change. Reach classes:

- `open page`: a public page reached without a login. An agent reads it only if the site's terms of use and
  robots rules allow automated reading, one request at a time; otherwise treat the site as `own browser`.
- `own browser`: used by the researcher personally in a browser: it needs a login or a subscription, or it
  does not serve automated requests.
- `human only`: a captcha, a payment, a letter or a visit.
- `dead`: the site is gone or the domain no longer belongs to the institution.

| site or archive | what it holds | what it does not index | reach | how a refusal looks | true zero looks like | traps | last checked |
|---|---|---|---|---|---|---|---|
