data = []


for client in clients:
    client_obj = clients[client]

    for job in client_obj['jobs']:
        job_obj = client_obj['jobs'][job]

        for file in client_obj['jobs'][job]['files']:
            print(file)
            file_obj = ''

        rowobj = {
            'client': client,
            'project': job,
            'material': '',
            'file_name': '',
            'file_size': '',
            'file_path': '',
            'qty': '',
        }
