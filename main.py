from bitalino import BITalino

macAddress = "98:D3:31:B1:84:2C"

batteryThreshold = 30
acqChannels = [0, 3]
samplingRate = 1000
nSamples = 10
digitalOutput = [0, 0, 1, 1]

# Connect to BITalino
device = BITalino(macAddress)

# Set battery threshold
device.battery(batteryThreshold)

# Read BITalino version
print(device.version())

# Start Acquisition
device.start(samplingRate, acqChannels)

# Read samples
print(device.read(nSamples))

# Turn BITalino led on
device.trigger(digitalOutput)

# Stop acquisition
device.stop()

# Close connection
device.close()