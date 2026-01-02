
def count_logs(logs):
    count={}

    for log in logs:
        logsplit=log.split(':')[0]


        if logsplit in count:
            count[logsplit]+=1

        else:
            count[logsplit]=1


    return(count)
    

logs=[
    "INFO: User logged in", "ERROR: Connection failed", "INFO: Upload complete"
]
print(count_logs(logs))


