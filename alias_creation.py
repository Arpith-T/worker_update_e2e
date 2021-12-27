import json

import requests

# alias_name = input("Enter teh Alias Name you want - ")
import trm_token

aciat001_base_url = "https://it-aciat001-trm.cfapps.sap.hana.ondemand.com/api/trm/v1"
worker_version = "6.21.3"


def alias_creation(alias_name=input("Enter the Alias Name you want - ")):
    # print(f"my name is {alias_name}")
    url = f"{aciat001_base_url}/tenant-softwares/versions"

    payload = json.dumps({
        "alias-name": f"{alias_name}",
        "sw-version": f"{worker_version}",
        "repositoryLocation": f"cf://worker-{worker_version}",
        "isCurrent": False,
        "isActive": True,
        "swType": "WORKER",
        "swImgType": "JAR_CF",
        "preScript": "<Update-plan-license-in-configuration: configurationUpdate --feature-tag=Update-plan-license-in-configuration  --parameters=\"{\"configurationParameters\":[{\"entity\":\"PROV_CONFIG\",\"key\":\"cpiLicenses\",\"values\":[\"CPI_LICENSE_KEY_UPDATE\"],\"operationType\":\"Update\",\"opMode\":\"Append\"}]}\" || XsuaaService-update-credentialtypes: updateXsuaaService --feature-tag=XsuaaService-update-credentialtypes --credential-types=binding-secret,instance-secret --skip-rollback=true || FileStorageService-rename-service: renameService --feature-tag=FileStorageService-rename-old-instance --old-service-name=it-fs.#TENANT_NAME# --new-service-name=it-fs-old.#TENANT_NAME#  || HeapDumpService-rename-service: renameService --feature-tag=HeapDumpService-rename-old-instance --old-service-name=heap-dump-#TENANT_NAME# --new-service-name=heap-dump-old-#TENANT_NAME#> && <IDPBasicAuth-create-saasregistry-service: createService --feature-tag=IDPBasicAuth-create-saasregistry-service --plan-name=service --service-name=saas-registry --instance-name=it-rt-saas-registry.#TENANT_NAME# --parameters=\"{\"xsappname\":\"it-rt-#TENANT_NAME#\", \"appName\":\"itrt#TENANT_NAME#\"}\" || IDPBasicAuth-persist-uaa-xsappname: persistXSAppName --feature-tag=IDPBasicAuth-persist-xsuaa-xsappname --service-name=xsuaa --instance-name=it-uaa-rt.#TENANT_NAME# --service-key-name=RoleManagementAccess || DestinationService-create-service: createService --feature-tag=DestinationService-create-service --plan-name=lite --service-name=destination --instance-name=it-destination.#TENANT_NAME# --bind-to-worker=true --service-key-name=it-destination.#TENANT_NAME# --persist-xsappname=true || ConnectivityService-create-service: createService --feature-tag=ConnectivityService-create-service --plan-name=lite --service-name=connectivity --instance-name=it-connectivity.#TENANT_NAME# --bind-to-worker=true --service-key-name=it-connectivity.#TENANT_NAME# --persist-xsappname=true || FileStorageService-create-service: createService --feature-tag=FileStorageService-recreate-new-instance --plan-name=custom --service-name=fs-storage --instance-name=it-fs.#TENANT_NAME# --parameters=\"{\"size\":2}\" --bind-to-worker=true --persist-xsappname=false || HeapDumpService-create-service: createService --feature-tag=HeapDumpService-recreate-new-instance --plan-name=custom --service-name=fs-storage --instance-name=heap-dump-#TENANT_NAME# --parameters=\"{\"size\":10}\" --bind-to-worker=true --persist-xsappname=false || LoggingService-create-service: createService --feature-tag=Worker-Specific-App-Logs --plan-name=#WORKER_LOG_DEF_PLAN# --service-name=application-logs --instance-name=it-logs.#TENANT_NAME# --bind-to-worker=true --persist-xsappname=false || MeteringService-sharedsecret-incredstore: StoreCredentialInCredStore --feature-tag=MeteringService-sharedsecret-incredstore --cred-type-in-credstore=pwd --name-of-cred-key=TENANT_ISOLATION_KEY --namespace-for-cred=i_#TENANT_NAME#> && Common-update-dependency: updateDependency --feature-tag=IDPBasicAuth-update-dependency,DestinationService-update-dependency,ConnectivityService-update-dependency,DestinationService-mtms-update-dependency",
        "postScript": "<FileStorageService-unbind-and-delete-old-instance: unbindAndDeleteService --feature-tag=FileStorageService-unbind-and-delete-old-instance --instance-name=it-fs-old.#TENANT_NAME# || HeapDumpService-unbind-and-delete-old-instance: unbindAndDeleteService --feature-tag=HeapDumpService-unbind-and-delete-old-instance --instance-name=heap-dump-old-#TENANT_NAME# || KafkaTaskLogs-update-advertisement: updateAdvertisement --feature-tag=KafkaTaskLogs-update-advertisement --topic-name=#IT_SYSTEM_ID#.co.log --permissions=[\"produce\"] --skipRollback=true> && <KafkaMetering-update-advertisement: updateAdvertisement --feature-tag=KafkaMetering-update-advertisement --topic-name=#IT_SYSTEM_ID#.message.metric.notification --permissions=[\"produce\"]> && <KafkaConfigGlobal-update-advertisement: updateAdvertisement --feature-tag=KafkaConfigGlobal-update-advertisement --topic-name=#IT_SYSTEM_ID#.config-global --permissions=[\"consume\"]>",
        "defaultRoutePaths": [
            ""
        ],
        "workerConfiguration": "{  \"applicationProperties\": {    \"timeout\": \"240\",    \"health-check-type\": \"http\",    \"health-check-http-endpoint\": \"/health\",    \"buildpacks\": [      \"sap_java_buildpack\"    ]  },  \"environmentVariables\": {    \"JBP_CONFIG_JAVA_OPTS\": \"[from_environment: false, java_opts: -Djava.security.properties=./etc/jre.tls.disabledAlgorithms.enabled.properties -Darchiving.feature.active=true -Djava.endorsed.dirs=.:lib/endorsed -Djava.ext.dirs='.:lib/ext:META-INF/.sap_java_buildpack/sapjvm/lib/ext:lib/ext/' -Dkaraf.base=. -Dkaraf.home=. -Dkaraf.log=data/log -Dkaraf.etc=etc -Dkaraf.startRemoteShell=true -Dorg.apache.camel.jmx.disabled=true -DSAPJVM_EXTENSION_COMMAND_HANDLER=com.sap.it.util.loglevel.logback.LogLevelListener -DDB_HIKARI_REGISTER_MBEANS=true -Dgreeting='howdy-doo!']\",    \"MEMORY_CALCULATOR_V1\": \"true\",    \"JBP_CONFIG_SAPJVM_MEMORY_WEIGHTS\": \"heap:13,stack:1,metaspace:2,native:1\",    \"JBP_CONFIG_DEBUG\": \"{enabled: true}\",    \"KARAF_HOME\": \"/app\",    \"JAVA_HOME\": \"/app/META-INF/.sap_java_buildpack/sapjvm\"  }}"
    })
    headers = {
        'Authorization': f'Bearer {trm_token.aciat001_trm_token()}',
        'Content-Type': 'application/json',
        'Cookie': 'JTENANTSESSIONID_kr19bxkapa=9iw0jy5xm%2FKXJ70RU4L5Z7hdMi5twfkpG0i8ImA3QgU%3D'
    }

    alias_creation_response = requests.request("POST", url, headers=headers, data=payload)

    print(alias_creation_response.text)

    return alias_name
    # alias_created = requests.request("GET", url, headers=headers)
    # print(f"Alias created is \n{alias_created.text}")


# alias_creation()


