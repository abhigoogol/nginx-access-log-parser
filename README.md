# nginx-access-log-parser
nginx access log parser program that analyses logs and produces statistics.
- Number of log entries processed
- Processing failures
- Number Log entries by HTTP status code
- URLs and pageviews
- URLs and unique visitors

Unique visitors:
HTTP requests possessing the same IP, the same date, and the same agent are considered as a unique visit. It includes web crawlers/spiders.

Pageviews:
All requests with HTTP status 200 are counted as pageviews. A important consideration that same path request by same IP and same user agent within N seconds span is counted as one pageview. This N seconds should be configurable.
