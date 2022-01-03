import requests
import json
from trm_token import aciat001_trm_token
from alias_creation import alias_creation
import time
from get_failed_tasks import failed_tasks
from influxdb import InfluxDBClient

def read_config():
    with open('config.json') as f:
        conf = json.load(f)
    return conf

config = read_config()

alias = alias_creation()


# def initiate_poll_worker_update(alias):
#     url = f"https://it-aciat001-trm.cfapps.sap.hana.ondemand.com/api/trm/v1/tenant-softwares/versions/{alias}/tenants"
#
#     print(url)
#
#     payload = json.dumps(
#     #     {
#     #     "softwareUpdateOperationType": "SCHEDULE",
#     #     "scheduledUtc": "",
#     #     "completeSystem": True,
#     # }
#         {
#             "softwareUpdateOperationType": "SCHEDULE",
#             "scheduledUtc": "",
#             "completeSystem": False,
#             "tenants": [
#                 {
#                     "tenantId": "mc101",
#                     "pin": False
#                 }
#             ]
#         }
#     )
#
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': f'Bearer {aciat001_trm_token()}',
#         'Cookie': 'JTENANTSESSIONID_kr19bxkapa=9iw0jy5xm%2FKXJ70RU4L5Z7hdMi5twfkpG0i8ImA3QgU%3D'
#     }
#
#     worker_update_response = requests.request("PUT", url, headers=headers, data=payload)
#
#     print(f"Worker Updates triggered for {alias}")
#     # response = worker_update_response.json()
#     # res_in_dict = json.dumps(response, indent=4)
#
#     print(json.dumps(worker_update_response.json(), indent=4))
#     # response = worker_update_response.text
#     # print(response)
#
#     time.sleep(25)
#     worker_update_status = requests.request("GET", url, headers=headers, data=payload)
#     # print(worker_update_status.text)
#     # print(type(worker_update_status.text))
#     res_in_dict = json.loads(worker_update_status.text)  # converts string to dictionary
#     print(res_in_dict)
#     print("\n")
#     total_no_of_workers = (len(res_in_dict["tasks"]))
#
#     # for task in range(0, len(res_in_dict)):
#     start_time = time.time()
#     while res_in_dict["inProgress"] != 0:
#         worker_update_status = requests.request("GET", url, headers=headers, data=payload)
#         res_in_dict = json.loads(worker_update_status.text)  # converts string to dictionary
#         print(json.dumps(res_in_dict, indent=4))
#         # print(json.dumps(res_in_dict.json(), indent=4))
#         time.sleep(60)
#     print("worker updates are completed")
#     end_time = time.time()
#     sec = end_time - start_time
#     # print("total time taken this loop: ", sec)
#     # # converts seconds to minutes.
#     #
#     # ty_res = time.gmtime(sec)
#     # total_time_taken = time.strftime("%H:%M:%S", ty_res)
#     # print(f"Total time taken to update {total_no_of_workers} workers is -  {total_time_taken} mins")
#     worker_update_status = requests.request("GET", url, headers=headers, data=payload)
#     # res_in_dict = json.loads(worker_update_status.text)
#     res_in_dict = json.loads(worker_update_status.text)
#     # print(f"the type of this is -  {res_in_dict}")
#     # print(f"length of {len(res_in_dict)}")
#
#     in_json = worker_update_status.json()
#     with open("worker_update.json", "w") as data_file:
#         json.dump(in_json, data_file)
#
#     time.sleep(20)
#
#     if res_in_dict["failed"] > 0:
#         failed_tasks(worker_update_file=res_in_dict)
#         end_time = time.time()
#         sec = end_time - start_time
#         ty_res = time.gmtime(sec)
#         total_time_taken = time.strftime("%H:%M:%S", ty_res)
#         print(f"Total time taken to update '{total_no_of_workers}' workers is -  {total_time_taken} mins")
#     else:
#         end_time = time.time()
#         sec = end_time - start_time
#         ty_res = time.gmtime(sec)
#         total_time_taken = time.strftime("%H:%M:%S", ty_res)
#         print(f"Total time taken to update '{total_no_of_workers}' workers is -  {total_time_taken} mins")
#
#     res_in_dict["total_time_taken"] = total_time_taken
#     res_in_dict["alias"] = alias
#
#     print(res_in_dict)
#
#     return res_in_dict


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
        res_in_dict[task] = failed_tasks
        return failed_tasks


def push_overall_status(worker_update_status):

    update_status_total = (worker_update_status["total"])
    update_status_updated = (worker_update_status["updated"])
    update_status_failed = (worker_update_status["failed"])
    update_status_time_taken = (worker_update_status["total_time_taken"])
    alias = (worker_update_status["alias"])

    overall_status_dict = [
        {
            "measurement": "worker_update_overall_status",
            "tags": {
                "alias": alias
            },
            "fields": {
                "total": update_status_total,
                "updated": update_status_updated,
                "failed": update_status_failed,
                "time_taken": update_status_time_taken
            }
        }
    ]
    print(overall_status_dict)
    if infra_client.write_points(overall_status_dict, protocol='json'):
        print("Data Insertion success")
        pass
    else:
        print("Dev-Data Insertion Failed")
        print(overall_status_dict)


def push_worker_update_status(worker_update_status):

    alias = (worker_update_status["alias"])

    for data in worker_update_status["tasks"]:

        taskId = data["taskId"]
        tenantName = data["tenantName"]
        status = data["status"]
        errorDescription = data["errorDescription"]
        worker_update_dict = [
            {
                "measurement": "worker_update_status",
                "tags": {
                    "alias": alias
                },
                "fields": {
                    "taskId": taskId,
                    "tenantName": tenantName,
                    "status": status,
                    "error": errorDescription
                }
            }
        ]
        print(worker_update_dict)

        if infra_client.write_points(worker_update_dict, protocol='json'):
            print("Data Insertion success")
            pass
        else:
            print("Dev-Data Insertion Failed")
            print(worker_update_dict)


url = f"{config['base_url']}/api/trm/v1/tenant-softwares/versions/{alias}/tenants"

print(url)

payload = json.dumps(config["payload"])
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {aciat001_trm_token()}',
    'Cookie': 'JTENANTSESSIONID_kr19bxkapa=9iw0jy5xm%2FKXJ70RU4L5Z7hdMi5twfkpG0i8ImA3QgU%3D'
}

worker_update_response = requests.request("PUT", url, headers=headers, data=payload)
worker_update_response.raise_for_status()
print(f"Worker Updates triggered for {alias}")
# response = worker_update_response.json()
# res_in_dict = json.dumps(response, indent=4)
# time.sleep(60)

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
    time.sleep(60)
print("worker updates are completed")
end_time = time.time()
sec = end_time - start_time

worker_update_status = requests.request("GET", url, headers=headers, data=payload)
# res_in_dict = json.loads(worker_update_status.text)
res_in_dict = worker_update_status.json()
# print(f"the type of this is -  {res_in_dict}")
# print(f"length of {len(res_in_dict)}")

in_json = worker_update_status.json()
with open("worker_update.json", "w") as data_file:
    json.dump(in_json, data_file)

time.sleep(20)

if res_in_dict["failed"] > 0:
    failed_tasks(worker_update_file=res_in_dict)
    end_time = time.time()
    sec = end_time - start_time
    ty_res = time.gmtime(sec)
    total_time_taken = time.strftime("%H:%M:%S", ty_res)
    print(f"Total time taken to update '{total_no_of_workers}' workers is -  {total_time_taken} mins")
else:
    end_time = time.time()
    sec = end_time - start_time
    ty_res = time.gmtime(sec)
    total_time_taken = time.strftime("%H:%M:%S", ty_res)
    print(f"Total time taken to update '{total_no_of_workers}' workers is -  {total_time_taken} mins")

res_in_dict["total_time_taken"] = total_time_taken
res_in_dict["alias"] = alias

print(res_in_dict)
#
infra_client = InfluxDBClient('hci-rit-prism-sel.cpis.c.eu-de-2.cloud.sap', 8086, 'arpdb')

infra_client.switch_database('arpdb')

push_overall_status(worker_update_status=res_in_dict)
push_worker_update_status(worker_update_status=res_in_dict)


# def main():
#     alias = alias_creation()
#     worker_update_status = initiate_poll_worker_update(alias=alias)
#     print(worker_update_status)
#     time.sleep(25)
#     # infra_client = InfluxDBClient('hci-rit-prism-sel.cpis.c.eu-de-2.cloud.sap', 8086, 'arpdb')
#     # infra_client.switch_database('arpdb')
#     push_overall_status(worker_update_status=worker_update_status)
#     push_worker_update_status(worker_update_status=worker_update_status)
#
# if __name__ == "__main__":
#     main()