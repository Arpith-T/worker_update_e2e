import json
import time
import requests
from requests.auth import HTTPBasicAuth
from influxdb import InfluxDBClient

# InfluxDBUrl = "https://hci-rit-prism-sel.cpis.c.eu-de-2.cloud.sap"
# # influxdb_username = "" #influx DB userna
# influxdb_password = "" #influx DB passwrod

dev_client = InfluxDBClient('hci-rit-prism-sel.cpis.c.eu-de-2.cloud.sap', 8086, 'arpdb')
# dev_client._InfluxDBClient__baseurl = InfluxDBUrl
dev_client.switch_database('arpdb')


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
    if dev_client.write_points(overall_status_dict, protocol='json'):
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

        if dev_client.write_points(worker_update_dict, protocol='json'):
            print("Data Insertion success")
            pass
        else:
            print("Dev-Data Insertion Failed")
            print(worker_update_dict)


def main():
    worker_update_data = open("worker-update.json", "r")
    worker_update_status = json.loads(worker_update_data.read())
    worker_update_data.close()
    push_overall_status(worker_update_status)
    push_worker_update_status(worker_update_status)


if __name__ == "__main__":
    main()
