import requests
import json
import urllib

class VraClient:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    def __init__(self, url, refresh_token):
        payload = {
            "refreshToken": refresh_token
        }
        if not url.endswith("/"):
            url += "/"
        response = requests.post(url + "iaas/api/login", json.dumps(payload),
                                 headers=self.headers)
        self.headers["Authorization"] = "Bearer " + response.json()["token"]

        self.url = url

    def request(self, urn, method, payload):
        r = requests.request(method, self.url + urn, data=payload, headers=self.headers)
        if r.status_code < 200 or r.status_code > 203:
            raise Exception("HTTP error: " + str(r.status_code) + r.content.decode("UTF-8"))
        return r

    def lookup_project(self, proj_name):
        return self.request("/iaas/api/projects?$filter=name eq '%s'" % proj_name, "GET", "").json()


    def deploy(self, bp_name, dep_name, proj_id, inputs):
        # Translate BP name to BP id
        r = self.request("blueprint/api/blueprints?name=" + urllib.parse.quote_plus(bp_name), "GET", "")
        bp = r.json()["content"][0]
        bp_id = bp["id"]

        # Request BP
        rq = {
            "blueprintId": bp_id,
            "deploymentName": dep_name,
            "inputs": inputs,
            "projectId": proj_id,
        }
        r = self.request("blueprint/api/blueprint-requests", "POST", json.dumps(rq))
        print("Deployment request for %s was successfully submitted with id %s" % (dep_name, r.json()["id"]))




