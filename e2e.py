import requests
import json
from trm_token import aciat001_trm_token
from alias_creation import alias_creation
import time

subtask_affected_list = []
alias = alias_creation()
print(alias)
url = f"https://it-aciat001-trm.cfapps.sap.hana.ondemand.com/api/trm/v1/tenant-softwares/versions/{alias}/tenants"

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

response = json.loads(worker_update_response.text)
print(response)

# TODO -  GET worker update status

time.sleep(25)
worker_update_status = requests.request("GET", url, headers=headers, data=payload)
res_in_dict = json.loads(worker_update_status.text)  # converts string to dictionary
print(res_in_dict)
print("\n")
total_no_of_workers = (len(res_in_dict["tasks"]))
print(f"No of workers - {total_no_of_workers}\n")

start_time = time.time()

# TODO keep polling(every 60 sec))for status till the "inProgress" field is not equal to 0.
while res_in_dict["inProgress"] != 0:
    worker_update_status = requests.request("GET", url, headers=headers, data=payload)
    res_in_dict = json.loads(worker_update_status.text)  # converts string to dictionary
    print(json.dumps(res_in_dict, indent=4))
    # print(json.dumps(res_in_dict.json(), indent=4))
    time.sleep(60)
print("worker updates are completed")
# end_time = time.time()
# sec = end_time - start_time
# # print("total time taken this loop: ", sec)
# # # converts seconds to minutes.
# ty_res = time.gmtime(sec)
# total_time_taken = time.strftime("%H:%M:%S", ty_res)
# print(f"Total time taken to update {total_no_of_workers} workers is - {total_time_taken} mins")


# TODO - now look for any failed workers. if there are failed workers get the task ID of those workers if no failures only then print the final time taken for worker update


def list_of_failed_tasks(worker_update_status_dict):
    failed_tasks = []
    for task in range(0, len(res_in_dict["tasks"])):
        if (worker_update_status_dict["tasks"][task]["status"]) == "FAILED":
            failed_tasks.append((worker_update_status_dict["tasks"][task]["taskId"]))
        print(failed_tasks)
        return failed_tasks


def get_failed_subtask(failed_tasks):
    for taskId in failed_tasks:
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
        subtask_affected_list.append(subtask_affected)
    print(subtask_affected_list)
    return subtask_affected_list


if res_in_dict["failed"] > 0:
    # list_of_failed_tasks(worker_update_status_dict=res_in_dict)
    get_failed_subtask(failed_tasks=list_of_failed_tasks(worker_update_status_dict=res_in_dict))

    end_time = time.time()
    sec = end_time - start_time
    ty_res = time.gmtime(sec)
    total_time_taken = time.strftime("%H:%M:%S", ty_res)
    print(f"Total time taken to update '{total_no_of_workers}' workers is - {total_time_taken} mins")

else:
    end_time = time.time()
    sec = end_time - start_time
    ty_res = time.gmtime(sec)
    total_time_taken = time.strftime("%H:%M:%S", ty_res)
    print(f"Total time taken to update '{total_no_of_workers}' workers is - {total_time_taken} mins")
