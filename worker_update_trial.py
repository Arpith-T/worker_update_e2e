import requests
import json
from trm_token import aciat001_trm_token
from alias_creation import alias_creation
import time

alias = alias_creation()


def list_of_failed_tasks(worker_update_file):
    with open(worker_update_file) as datafile:
        worker_update_status = json.loads(datafile.read())
        # print(worker_update_status)
        # print(type(worker_update_status))
        failed_tasks = []
        for task in range(0, len(worker_update_status["tasks"])):
            if (worker_update_status["tasks"][task]["status"]) == "FAILED":
                failed_tasks.append((worker_update_status["tasks"][task]["taskId"]))
        print(failed_tasks)
        return failed_tasks


url = f"https://it-aciat001-trm.cfapps.sap.hana.ondemand.com/api/trm/v1/tenant-softwares/versions/{alias}/tenants"

print(url)

payload = json.dumps({
    "softwareUpdateOperationType": "SCHEDULE",
    "scheduledUtc": "",
    "completeSystem": True,
})
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {aciat001_trm_token()}',
    'Cookie': 'JTENANTSESSIONID_kr19bxkapa=9iw0jy5xm%2FKXJ70RU4L5Z7hdMi5twfkpG0i8ImA3QgU%3D'
}

worker_update_response = requests.request("PUT", url, headers=headers, data=payload)

# response = worker_update_response.json()
# res_in_dict = json.dumps(response, indent=4)


print(json.dumps(worker_update_response.json(), indent=4))
# response = worker_update_response.text
# print(response)

time.sleep(25)
worker_update_status = requests.request("GET", url, headers=headers, data=payload)
# print(worker_update_status.text)
# print(type(worker_update_status.text))
res_in_dict = json.loads(worker_update_status.text)  # converts string to dictionary
print(res_in_dict)
print("\n")
total_no_of_workers = (len(res_in_dict["tasks"]))

# for task in range(0, len(res_in_dict)):
start_time = time.time()
while res_in_dict["inProgress"] != 0:
    worker_update_status = requests.request("GET", url, headers=headers, data=payload)
    res_in_dict = json.loads(worker_update_status.text)  # converts string to dictionary
    print(json.dumps(res_in_dict, indent=4))
    # print(json.dumps(res_in_dict.json(), indent=4))
    time.sleep(60)
print("worker updates are completed")
end_time = time.time()
sec = end_time - start_time
print("total time taken this loop: ", sec)
# # converts seconds to minutes.
#
ty_res = time.gmtime(sec)
res = time.strftime("%H:%M:%S", ty_res)
print(f"Total time taken to update {total_no_of_workers} workers is -  {res} mins")
worker_update_status = requests.request("GET", url, headers=headers, data=payload)
# res_in_dict = json.loads(worker_update_status.text)
res_in_dict = worker_update_status.json()
print(f"the type of this is -  {res_in_dict}")
print(f"length of {len(res_in_dict)}")

in_json = worker_update_status.json()
with open("worker_update.json", "w") as data_file:
    json.dump(in_json, data_file)

time.sleep(20)
if res_in_dict["failed"] > 0:
    for taskId in list_of_failed_tasks("worker_update.json"):
        url = f"https://it-aciat001-trm.cfapps.sap.hana.ondemand.com/api/trm/v1/tasks/{taskId}/subtasks"

        # print(url)

        payload = {}
        headers = {
            'Authorization': f'Bearer {aciat001_trm_token()}'
        }

        subtasks = requests.request("GET", url, headers=headers, data=payload)
        response_in_dict = json.loads(subtasks.text)

        # print(json.dumps(response_in_dict, indent=4))

        retrycount_list = []
        for subtask in range(0, len(response_in_dict)):
            list_value = int((response_in_dict[subtask]["retryCount"]))
            retrycount_list.append(list_value)
        print(f"max retry count is {max(retrycount_list)}")

        for subtask in range(0, len(response_in_dict)):
            # print("test")
            if (response_in_dict[subtask]["retryCount"]) == max(retrycount_list):
                # print(response_in_dict[subtask])
                subtask_affected = json.dumps(response_in_dict[subtask], indent=4)
        print(f"subtask affected is - \n {subtask_affected}")
        end_time = time.time()
        sec = end_time - start_time
        ty_res = time.gmtime(sec)
        res = time.strftime("%H:%M:%S", ty_res)
        print(f"Total time taken to update '{total_no_of_workers}' workers is -  {res} mins")
else:
    end_time = time.time()
    sec = end_time - start_time
    ty_res = time.gmtime(sec)
    res = time.strftime("%H:%M:%S", ty_res)
    print(f"Total time taken to update '{total_no_of_workers}' workers is -  {res} mins")


