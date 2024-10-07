# influxdb-ais
A simple client that receives AIS data and publishes it to influxdb


# Setup
1. **Install (Windows)**. Download and extract [influxdb v2.x](https://docs.influxdata.com/influxdb/v2/install/) to `<your path>/influxdata/`.

2. **Start InfluxDB**. In terminal, navigate into `<your path>/influxdata/` and run `./influxd`.

3. Open `localhost:8086` and register a user. **Save your token** in a secure place.

4. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

5. Create an `.env` file with the following variables:
   ```
   INFLUX_TOKEN=<YOUR TOKEN>
   INFLUX_ORG=<YOUR ORG>
   INFLUX_HOST=http://<YOUR IP>:<YOUR PORT>
   ```

   If you are unsure about your variables, check the Getting Started Python Tutorial in the influx dashboard `localhost:8086`.

6. Modify the following in `client.py` based on your needs:
   - `APP_NAME = 'Test/TestApp'`
   - `TOPIC = 'vessels-v2/#'`
   - `BUCKET = "digitraffic-api"`
   - `SENSOR = "ais"`

7. Run `client.py` to start writing AIS data.


# Run as docker container
Requires:
1. influxdb is running 
2. env variables are specified in `.env` file that is located in same directory as docker-compose.yml
3. client.py is adjusted according to users needs

Start docker in background:
```docker compose up -d```
