# vRealize Automation Bulk VM Creation Example

This is a simple example of how to use a CVS file to bulk-create a set of virtual machines. It requires a CSV-file with
the following layout:

```
<name>,<cloud template>,<image (vSphere template)>,<# CPUs>,<Memory in MB>,<Disk in GB>
```

Example:
```csv
mickey,Generic vSphere VM,demo-1,1,1024,30
minnie,Generic vSphere VM,demo-2,2,1024,30
donald,Generic vSphere VM,demo-1,2,2048,30
goofy,Generic vSphere VM,demo-2,1,1024,30
```

You can find a sample input file [here](vms.csv).

## Authentication
This tool relies on API token-based authentication. You can obtain an API token for a user as follows. Notice that
there are different procedures for cloud (SaaS) ans on-premises installations.

#### Cloud (SaaS)
1. Go drop down the menu from your user name displayed towards the top-right corner.
2. Click on "My Account"
3. Select the API Tokens tab
4. Click "Generate Token"
5. Enter a token name and an expiration time (default is 6 months)
6. Select the desired products and roles
7. Click "Generate"
8. Copy the token and store it in a safe place. You will not be able to see it again in the UI!

### On-premises
1. Issue the following curl-command:
```
curl --location --request POST 'https://<vRA8.1-URL>/csp/gateway/am/api/login?access_token' \
--header 'Content-Type: application/json' \
--data-raw '{
	"username": "<username>",
	"password": "<password>",
	"domain": "System Domain | AD Domain"
}'
```

Replace the username and password and enter an AD domain if you are using AD-based authentication. The result will look
similar to this:

```json
{
    "scope": "some scope",
    "access_tokeen": "a very long string of random characters"
    "refresh_token": "abcdefghijklmnopqrstuvxyz123"
}
```

Copy the text after the "refresh_token" tag (exclude any quotes). This is your API token.

## How to run

```bash
$ python3 bulkdeploy.py -u https://api.mgmt.cloud.vmware.com -f vms.csv -t token -p myProj
```

## Sample Cloud Template
The [blueprint.yaml](blueprint.yaml) file contains a sample Cloud Template. This cloud templates allows you to refer to an
arbitrary image (e.g. AMI or vSphere Template).