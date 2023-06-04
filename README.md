# CAIC Classic ID to New ID Converter (clscidapi)

In the 2021-2022 season, the CAIC website was redesigned. Along with this change, a number of old references to the "classic" CAIC website's Field Reports were broken. This tool attempts to fix that by implementing a lookup service that provides several helpful ways to pivot from a classic Field Report's `obs_id` to a new CAIC Field Report or a working classic Field Report.

The lookup service is backed by a simple [JSON file](https://github.com/gormaniac/clscidapi/blob/main/data/clsc_ids.json) that was created with the help of [caicpy](https://github.com/gormaniac/caicpy). See the [script](https://github.com/gormaniac/co-avy-research/blob/main/scripts/classic-enum.sh) that helped generate this file in my [co-avy-research](https://github.com/gormaniac/co-avy-research) repo.

Currently the lookup service only supports classic IDs back to 2010. This is a limitation with the data available via the CAIC's new APIs. Further research needs to be done to enumerate older classic IDs. Manually browse to older "classic" Field Reports by adding the classic ID to the end of the URL `http://classic.avalanche.state.co.us/caic/obs/obs_report.php?obs_id=`.

Eventually this service will be running as a hosted app somewhere - the location is currently TBD.

## API Usage

The API has a single endpoint, `clscid-lookup`.

This endpoint only accepts GET requests and accepts arguments in the form of URL parameters. All URL parameters have a descriptive long name and a single letter short name alias.

The `q/query` parameter is the only required parameter. The value can either be a single classic ID, or an entire CAIC classic URL that has the ID stored in the `obs_id` URL parameter.

By default, the endpoint takes the given query parameter, tries to find a corresponding new ID, and returns a JSON object containing the Field Report's new CAIC URL in the `data` key.

There are several modifications to default behavior that can be controlled via boolean URL parameters:

- `r/redirect`: Tells the endpoint to initiate an HTTP redirect to the newly generated URL instead of returning a JSON object.
- `u/url`: Tells the endpoint to return a full URL instead of just the new Field Report ID. This is true by defualt and can only be set to false.
- `c/classic`: Redirect to or return the CAIC classic Field Report URL instead of the new Field Report URL. This is helpful as older Field Reports do not display fully on the new webpage.
