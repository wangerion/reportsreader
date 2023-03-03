from bs4 import BeautifulSoup


# Splitting the list as usually the server have only 5 columns with data in them
def split(list_a, chunk):
    # Some lists contain over 20 items, and we only need 5 of those for each mountpoint
    # In our case chunk is the actual number of columns that we see in the report
    for i in range(0, len(list_a), chunk):
        # yield is used here because we are generating another list
        yield list_a[i:i + chunk]


with open("ngncdio.html") as fp:
    soup = BeautifulSoup(fp, 'lxml')
# Finding all tr that contain the required data in our report
tableuptime = soup.find('table', id="tableUptime").find("tbody").find_all("tr")
for row in tableuptime:
    cells = row.find_all('td')
    # Because the output looks like this ['11:12,', 'Days']
    uptime = cells[1].text.split()
    # A simple check to see if the list that we create using the table data has at least 2 items in it.
    if len(uptime) == 2:
        # If the uptime is in 24hours format it's not going to be considered a digit.
        if uptime[0].isdigit() and int(uptime[0]) >= 4:
            pass
        else:
            print(f"Server: {cells[0].text} has the following uptime: {cells[1].text}")
    else:
        print(f"Server: {cells[0].text} has the following uptime: {cells[1].text}")

tableping = soup.find('table', id="tableMonitoredHosts").find("tbody").find_all("tr")
for row in tableping:
    cells = row.find_all("td")
    pingable = cells[2].text
    # Output looking like <td>True</td> that's why we check it like this.
    if pingable != 'True':
        print(f"Serverul: {cells[0].text} are pingable status de: {cells[2].text}")

# In the report provided all tha table have different id's but the same class name so we find them
tableusage = soup.find_all("table", class_="DiskUsage")
for row in tableusage:
    cells = row.find_all("td")

    # The split used here is the actual function created at the top of this script
    # This for is only used to iterate over every list as this has created a list in list
    for data in list(split(cells, 5)):
        # print(data[4].text)
        if float(data[4].text.strip('%')) >= 85:
            print(f"Mountpoint: {data[0].text} is at: {data[4].text}")
