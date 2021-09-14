# distance_to_mkad

Its a simple flask application to calculate the distance between a passed address and MKAD.

# Start app

After cloning the repo, add your Google API KEY to the .env file and then run the following command:

```
bash start.sh
```

The Docker container will be created and started on port :5000.

# Making a request

In this url you can pass the address:

```
http://localhost:5000/getdistance/getaddress?address=Moscow
```
The 'address' variables accepts string, lat/lng and plus code. You can read more aboute here:
https://developers.google.com/maps/documentation/geocoding/overview

### Thats it :)
