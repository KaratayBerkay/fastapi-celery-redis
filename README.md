# data_gatherer_study_case
Data Gatherer Study Case

> This is a study case of a gathers data that collects data from Io devices and stores it in a database.

# How to run
Run compose yaml
```bash
docker-compose up --build
```

Click on the link below to access to openapi documentation
```bash
http://0.0.0.0:40111
 ```

# How to test api endpoints

Login with superuser credentials from post /authentication/login endpoint | Click on Try it out button
```bash
{
  "email": "admin@admin.com",
  "password": "admin"
}
```
> Get your access token from response body and copy it to Authorize button on the top right corner of the page
You are now logged in as superuser

Create one or multiple devices from post /devices/create endpoint | Click on Try it out button
```bash
{
  "device_name": "Device 1",
  "device_type": "GPS",
  "device_model": "Yummy",
  "device_status": "OPEN"
}
```
> You have created a device

Check your device from get /devices endpoint | Click on Try it out button
query parameters
```bash
device_model=Yummy&device_type=GPS
```
Don't forget to copy your <device_id> to use it in the next steps

Check device location history from get /devices/{device_id}/locations endpoint | Click on Try it out button
paste your <device_id> to the path parameter
```bash
{
  "device_id": "<device_id>"
}
```

Or go to /devices/locations/last endpoint to get the last location of all devices without any query parameters


Run dummy device to send random location info
```bash
docker exec -it dummy_device_container python
```

Copy python script to send location from dummy device
```python
from socket_connector import iter_device_location
iter_device_location(host="gatherer_service", port=44111, r= 1, device_id="63bdab69-a026-4167-a207-a2d949d7b1bc")
```
Congratulations! You have send location from dummy device to TCP gatherer service.

Recheck device location history from get /devices/{device_id}/locations endpoint | Click on Try it out button
paste your <device_id> to the path parameter if you want to limit last history give limit parameter
```bash
{
  "device_id": "<device_id>",
  "limit": 10
}
```