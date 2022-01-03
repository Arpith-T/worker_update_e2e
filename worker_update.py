import requests
import json
from trm_token import aciat001_trm_token
from alias_creation import alias_creation
import time

alias = alias_creation()

url = f"https://it-aciat001-trm.cfapps.sap.hana.ondemand.com/api/trm/v1/tenant-softwares/versions/{alias}/tenants"

payload = json.dumps({
    "softwareUpdateOperationType": "SCHEDULE",
    "scheduledUtc": "",
    "completeSystem": False,
    "tenants": [
        {
            "tenantId": "cig-dev-gov-cpi-test",
            "pin": False
        }
    ]
})
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {aciat001_trm_token()}',
    'Cookie': 'JTENANTSESSIONID_kr19bxkapa=9iw0jy5xm%2FKXJ70RU4L5Z7hdMi5twfkpG0i8ImA3QgU%3D'
}

worker_update_response = requests.request("PUT", url, headers=headers, data=payload)

response = json.loads(worker_update_response.text)
print(response)
# print(type(response))
update_status = (response[0]["status"])

# jsonstr = json.dumps(response, indent=4)
# print(type(jsonstr))


# t_end = time.time() + 60 * 5
# while time.time() < t_end:
#     worker_update_status = requests.request("GET", url, headers=headers, data=payload)
#     print(worker_update_status.text)
#     time.sleep(30)

start_time = time.time()
# print(start_time)

while update_status != "SUCCESS":

    worker_update_status = requests.request("GET", url, headers=headers, data=payload)
    # print(json.dumps(worker_update_status.json(), indent=4))
    # worker_update_status = requests.request("GET", url, headers=headers, data=payload)
    response = worker_update_status.text
    # print(response)
    res_in_dict = json.loads(response)  # converts string to dictionary
    update_status = (res_in_dict["tasks"][0]["status"])
    # print(update_status)
    time.sleep(30)
else:
    print("worker Update completed")
    worker_update_status = requests.request("GET", url, headers=headers, data=payload)
    print(json.dumps(worker_update_status.json(), indent=4))
    # in_json = worker_update_status.json()
    worker_update_status_dict = json.loads(worker_update_status.text)
    # print(type(worker_update_status_dict))
    # with open("worker_update.json", "w") as data_file:
    #     json.dump(worker_update_status_dict, data_file)

end_time = time.time()
sec = end_time - start_time
# print("total time taken this loop: ", sec)
# converts seconds to minutes.

ty_res = time.gmtime(sec)
res = time.strftime("%H:%M:%S", ty_res)
print(f"Total time taken to update {res}")


# TODO add 2 more dictionaries to that file 1) alias 2) Time_taken

# worker_update_status_dict["time_taken"] = total_time_taken
# worker_update_status_dict["alias"] = alias

worker_update_status_dict.update({"time_taken": res, "alias": alias})

# time_taken = {"time_taken": total_time_taken}
# alias_in_dict = {"alias": alias}
# # print(f"For {alias_in_dict} worker update time is {time_taken}")
with open("worker_update.json", "w") as data_file:
    json.dump(worker_update_status_dict, data_file)

