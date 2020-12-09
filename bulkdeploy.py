from vraclient import VraClient
import sys
import getopt

# Field indexes (column numbers) within the CSV file.
NAME_FIELD = 0
BP_NAME_FIELD = 1
IMAGE_FIELD = 2
CPU_FIELD = 3
MEM_FIELD = 4
DISK_FIELD = 5

PROGRAM = "bulkdeploy.py"
USAGE = PROGRAM + '-f <input file> -u <url> -t <API token> -p <project name>'

url = ''
token = ''
project = ''
file = ''

try:
    opts, args = getopt.getopt(sys.argv[1:], "hu:t:p:f:", ["url=", "token=", "project=", "file="])
except getopt.GetoptError:
    print(USAGE)
    exit(2)
for opt, arg in opts:
    if opt == '-h':
        print(USAGE)
        exit(1)
    elif opt in ("-u", "--url"):
        url = arg
    elif opt in ("-t", "--token"):
        token = arg
    elif opt in ("-p", "--project"):
        project = arg
    elif opt in ("-f", "--file"):
        file = arg

if file == '' or project == '' or url == '' or token == '':
    print("File, URL, API token and project must be specified")
    exit(1)

# Connect to vRA and lookup the specified project
v = VraClient(url, token)
p = v.lookup_project(project)
if len(p["content"]) == 0:
    print("Project %s was not found" % project)
    exit(1)
p = p["content"][0]

# Read input file and submit a deployment request for each line
with open(file) as f:
    for line in f:
        line = line.strip()
        if line[0] == "#":
            continue
        fields = line.split(",")
        inputs = {
            "memMB": fields[MEM_FIELD],
            "cpuCount": fields[CPU_FIELD],
            "diskGB": fields[DISK_FIELD],
            "image": fields[IMAGE_FIELD]
        }
        v.deploy(fields[BP_NAME_FIELD], fields[NAME_FIELD], p["id"], inputs)
